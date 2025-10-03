import asyncio
import base64
import json
import logging
import os
import audioop
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import websockets
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Connect, Say
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv("/Users/shreyastaware/Desktop/ai_fitness_coach/app/.env")

# Server configuration
HTTP_SERVER_PORT = 8080
WEBSOCKET_SERVER_PORT = 8081
NGROK_WEBSOCKET_URL = os.getenv("NGROK_WEBSOCKET_URL")

# Set up logging
logging.basicConfig(level=logging.INFO)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

DEEPGRAM_URL = (
    "wss://api.deepgram.com/v1/listen"
    "?encoding=mulaw&sample_rate=8000&channels=1"
    "&punctuate=true&interim_results=true"
    "&endpointing=true&utterance_end_ms=2000" # End utterance after 2s of silence (as requested)
)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# ElevenLabs Voice ID
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL" # Example: Sarah

# ElevenLabs real-time TTS endpoint
ELEVENLABS_URL = (
    f"wss://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/"
    "stream-input?model_id=eleven_turbo_v2&output_format=pcm_16000"
)

# A queue to hold the user's transcribed text
transcript_queue = asyncio.Queue()

# Global state management
tts_task = None
bot_is_speaking = False
last_audio_time = 0
SILENCE_THRESHOLD = 2.0  # 2 seconds of silence before considering speech ended (as requested)
AUDIO_VOLUME_THRESHOLD = 100  # minimum audio level to consider as speech
speech_lock = asyncio.Lock()  # Prevent race conditions

def pcm_to_mulaw(pcm_data, sample_rate_in=16000, sample_rate_out=8000):
    """Convert PCM audio to mu-law format for Twilio."""
    try:
        # Ensure we have valid PCM data
        if not pcm_data or len(pcm_data) == 0:
            return b''
            
        # Downsample from 16kHz to 8kHz if needed
        if sample_rate_in != sample_rate_out:
            # Simple downsampling by taking every other sample (assumes 16-bit samples)
            if len(pcm_data) % 2 == 0:
                # Convert bytes to 16-bit samples, downsample, then back to bytes
                samples = []
                for i in range(0, len(pcm_data), 4):  # Every other 16-bit sample
                    if i + 1 < len(pcm_data):
                        samples.extend([pcm_data[i], pcm_data[i + 1]])
                pcm_data = bytes(samples)
            else:
                pcm_data = pcm_data[::2]
        
        # Convert to mu-law (assuming 16-bit PCM input)
        mulaw_data = audioop.lin2ulaw(pcm_data, 2)  # 2 = 16-bit samples
        return mulaw_data
        
    except Exception as e:
        logging.error(f"Error converting PCM to mu-law: {e}")
        return b''

def calculate_audio_volume(audio_data):
    """Calculate a simple volume metric from audio data."""
    if not audio_data:
        return 0
    
    # Simple RMS calculation for mu-law audio
    total = sum(abs(byte - 127) for byte in audio_data)  # mu-law is offset by 127
    return total / len(audio_data) if audio_data else 0

async def get_openai_response(text):
    """Sends text to OpenAI and returns the response."""
    logging.info(f"Sending to OpenAI: {text}")
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful conversational assistant. Keep your responses concise and to the point."},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            max_tokens=150,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now."

async def stream_elevenlabs_to_twilio(text, twilio_ws, stream_sid):
    """Streams text to ElevenLabs and the resulting audio back to Twilio."""
    global tts_task, bot_is_speaking
    logging.info(f"Streaming to ElevenLabs: {text}")
    
    try:
        async with speech_lock:
            bot_is_speaking = True
            
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        async with websockets.connect(ELEVENLABS_URL, additional_headers=headers) as elevenlabs_ws:
            # Send the initial configuration message to ElevenLabs
            await elevenlabs_ws.send(json.dumps({
                "text": " ",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                "generation_config": {
                    "chunk_length_schedule": [120, 160, 250, 290]
                }
            }))
            
            # Send the text to be synthesized
            await elevenlabs_ws.send(json.dumps({
                "text": text + " ", 
                "try_trigger_generation": True
            }))
            
            # Send the end-of-stream message
            await elevenlabs_ws.send(json.dumps({"text": ""}))

            # Receive audio data and stream it to Twilio
            async for message in elevenlabs_ws:
                # Check if we've been cancelled (user interrupted)
                if not bot_is_speaking:
                    logging.info("Bot speech interrupted by user")
                    break
                    
                data = json.loads(message)
                if data.get("audio"):
                    audio_chunk = base64.b64decode(data["audio"])

                    # Convert PCM to mu-law for Twilio
                    mulaw_audio = pcm_to_mulaw(audio_chunk)
                    
                    # Twilio media message format
                    media_message = {
                        "event": "media",
                        "streamSid": stream_sid,
                        "media": {"payload": base64.b64encode(mulaw_audio).decode('utf-8')}
                    }
                    
                    try:
                        await twilio_ws.send(json.dumps(media_message))
                    except websockets.exceptions.ConnectionClosed:
                        logging.warning("Twilio connection closed while sending audio")
                        break
                        
                elif data.get("isFinal"):
                    logging.info("ElevenLabs finished generating audio")
                    break

    except asyncio.CancelledError:
        logging.info("ElevenLabs TTS stream was cancelled (interrupted).")
        raise
    except Exception as e:
        logging.error(f"ElevenLabs error: {e}")
        raise
    finally:
        async with speech_lock:
            bot_is_speaking = False
        tts_task = None
        logging.info("ElevenLabs stream finished.")


# --- WebSocket Server ---
async def websocket_handler(twilio_ws):
    """The main WebSocket handler for the entire conversation flow."""
    global tts_task, transcript_queue, bot_is_speaking, last_audio_time    
    """Handles WebSocket connections from Twilio."""
    logging.info("Twilio WebSocket connection established.")
    try:
        """
        Handles the WebSocket connection from Twilio and proxies audio to Deepgram.
        """
        logging.info("Twilio WebSocket connection established.")
        
        extra_headers = {'Authorization': f'Token {DEEPGRAM_API_KEY}'}
        
        async with websockets.connect(DEEPGRAM_URL, additional_headers=extra_headers) as deepgram_ws:
            logging.info("Successfully connected to Deepgram.")

            stream_sid = None
            # Event to signal that the call has ended and we should shut down.
            shutdown_event = asyncio.Event()
            user_is_speaking = False
            speech_buffer = []  # Buffer to accumulate speech for interruption detection

            async def twilio_receiver(twilio_ws, deepgram_ws, shutdown_event):
                """Receives audio from Twilio, handles interruptions, and forwards to Deepgram."""
                nonlocal stream_sid, user_is_speaking
                global tts_task, bot_is_speaking, last_audio_time 
                try:
                    async for message in twilio_ws:
                        data = json.loads(message)
                        if data['event'] == 'start':
                            stream_sid = data['start']['streamSid']
                            logging.info(f"Twilio stream started (SID: {stream_sid})")

                        elif data['event'] == 'media':
                            payload = data['media']['payload']
                            chunk = base64.b64decode(payload)
                            current_time = time.time()
                            
                            # Calculate audio volume to detect speech
                            volume = calculate_audio_volume(chunk)                            
                            
                            # Check if this is likely user speech (above threshold)
                            if volume > AUDIO_VOLUME_THRESHOLD:
                                last_audio_time = current_time
                                
                                # If bot is speaking and we detect user speech, interrupt
                                if bot_is_speaking:
                                    logging.info("User interruption detected - stopping bot speech")
                                    async with speech_lock:
                                        bot_is_speaking = False
                                    
                                    if tts_task and not tts_task.done():
                                        # Send clear message to stop Twilio playback
                                        try:
                                            await twilio_ws.send(json.dumps({
                                                "event": "clear", 
                                                "streamSid": stream_sid
                                            }))
                                        except Exception as e:
                                            logging.error(f"Error sending clear message: {e}")
                                        
                                        tts_task.cancel()
                                        try:
                                            await tts_task
                                        except asyncio.CancelledError:
                                            pass
                                        tts_task = None
                                
                                user_is_speaking = True
                                # Always forward user audio to Deepgram when they're speaking
                                try:
                                    await deepgram_ws.send(chunk)
                                except websockets.exceptions.ConnectionClosed:
                                    logging.warning("Deepgram connection closed")
                                    break
                            
                            else:
                                # Low volume - check if user has stopped speaking
                                if (user_is_speaking and 
                                    current_time - last_audio_time > SILENCE_THRESHOLD):
                                    user_is_speaking = False
                                    logging.info("User finished speaking")
                                
                                # Still forward low-volume audio to maintain connection
                                try:
                                    await deepgram_ws.send(chunk)
                                except websockets.exceptions.ConnectionClosed:
                                    logging.warning("Deepgram connection closed")
                                    break                          

                        elif data['event'] == 'stop':
                            logging.info("Twilio has stopped the stream.")
                            break
                except websockets.exceptions.ConnectionClosed as e:
                    logging.warning(f"Twilio connection closed unexpectedly: {e}")
                except Exception as e:
                    logging.error(f"Error in Twilio receiver: {e}", exc_info=True)
                finally:
                    # When the loop is broken (call ends), signal for shutdown.
                    shutdown_event.set()
                    logging.info("Shutdown event set.")

            async def deepgram_receiver(deepgram_ws, shutdown_event):
                """
                Receives transcriptions from Deepgram, puts final utterances in a queue,
                and listens for the shutdown signal. Only processes contiguous sentences without 2+ second gaps.
                """
                full_transcript = []
                last_speech_time = time.time()
                
                while not shutdown_event.is_set():
                    try:
                        # Wait for a message from Deepgram with a timeout to allow checking the shutdown event
                        message = await asyncio.wait_for(deepgram_ws.recv(), timeout=0.1)
                        data = json.loads(message)

                        # Robustly check for a valid transcript message
                        if (data.get('type') == 'Results' and 
                        data.get('channel', {}).get('alternatives', [{}])[0].get('transcript')):

                            transcript = data['channel']['alternatives'][0]['transcript'].strip()
                            current_time = time.time()
                        
                            if transcript and data.get('is_final'):
                                # Check if there's been a gap of more than 2 seconds
                                if current_time - last_speech_time > 2.0 and full_transcript:
                                    # Gap detected, reset transcript buffer
                                    logging.info("Speech gap detected, resetting transcript buffer")
                                    full_transcript = []
                                
                                full_transcript.append(transcript)
                                last_speech_time = current_time

                            if data.get('speech_final'):
                                final_text = " ".join(full_transcript).strip()
                                if final_text and not bot_is_speaking:
                                    logging.info(f"Final Utterance: {final_text}")
                                    await transcript_queue.put(final_text)
                                else:
                                    logging.info(f"Discarding utterance (bot speaking or empty): {final_text}")
                                full_transcript = []

                    except asyncio.TimeoutError:
                        # This is expected. It just allows the while loop to check the shutdown_event.
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        logging.info("Deepgram connection closed by server.")
                        break # Exit the loop if the connection is closed
                    except Exception as e:
                        logging.error(f"Error in deepgram_receiver: {e}")
                        break

            async def response_manager(shutdown_event):
                """
                Manages getting responses from OpenAI and streaming them back.
                Also listens for the shutdown signal.
                """
                nonlocal stream_sid # stream_sid is defined in the parent scope
                global tts_task, bot_is_speaking

                while not shutdown_event.is_set():
                    try:
                        # Create tasks to wait for a new transcript or a shutdown signal
                        get_transcript_task = asyncio.create_task(transcript_queue.get())
                        wait_shutdown_task = asyncio.create_task(shutdown_event.wait())

                        # Wait for whichever task completes first
                        done, pending = await asyncio.wait(
                            [get_transcript_task, wait_shutdown_task],
                            return_when=asyncio.FIRST_COMPLETED
                        )

                        # Cancel any pending tasks to clean up
                        for task in pending:
                            task.cancel()

                        # If the shutdown event was triggered, exit the loop
                        if wait_shutdown_task in done:
                            logging.info("Response manager shutting down.")
                            break

                        # If a new transcript was received, process it
                        if get_transcript_task in done:
                            user_text = get_transcript_task.result()

                            # Only respond if bot is not currently speaking
                            if not bot_is_speaking and stream_sid:
                                logging.info(f"Processing user input: {user_text}")
                                ai_response_text = await get_openai_response(user_text)

                                # Double-check bot isn't speaking before starting TTS
                                if ai_response_text and not bot_is_speaking:
                                    try:
                                        tts_task = asyncio.create_task(
                                            stream_elevenlabs_to_twilio(ai_response_text, twilio_ws, stream_sid)
                                        )
                                        await tts_task
                                    except asyncio.CancelledError:
                                        logging.info("TTS task was cancelled due to user interruption")
                                    except Exception as e:
                                        logging.error(f"Error in TTS task: {e}")
                                    finally:
                                        tts_task = None
                            else:
                                logging.info(f"Bot is speaking or no stream_sid, discarding user input: {user_text}")

                    except asyncio.CancelledError:
                        logging.info("Response manager task cancelled.")
                        break

            try:
                await asyncio.gather(
                    twilio_receiver(twilio_ws, deepgram_ws, shutdown_event),
                    deepgram_receiver(deepgram_ws, shutdown_event),
                    response_manager(shutdown_event)
                )
            except websockets.exceptions.ConnectionClosed as e:
                logging.warning(f"A WebSocket connection closed: {e}")
            except Exception as e:
                logging.error(f"Main handler error: {e}", exc_info=True)
            finally:
                logging.info("Closing all connections.")
                if tts_task and not tts_task.done():
                    tts_task.cancel()

                # Once the Twilio stream is done, we can close the Deepgram connection gracefully
                # await deepgram_ws.send(json.dumps({'type': 'CloseStream'}))
                # Proactively close the Deepgram connection
                await deepgram_ws.close()

                logging.info("Gracefully closing Deepgram connection.")
    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"WebSocket connection closed: {e}")
    except Exception as e:
        logging.error(f"Error in WebSocket handler: {e}")

async def start_websocket_server_async():
    """Sets up and runs the WebSocket server forever."""
    # websockets.serve is an async context manager that handles server startup and shutdown.
    ip_add = "127.0.0.1" # "0.0.0.0"
    async with websockets.serve(websocket_handler, ip_add, WEBSOCKET_SERVER_PORT):
        logging.info(f"WebSocket server running on port {WEBSOCKET_SERVER_PORT}")
        await asyncio.Future()  # This runs the server indefinitely.

def run_websocket_server():
    """Initializes the asyncio event loop and runs the server in the current thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # This runs the 'start_websocket_server_async' coroutine until it's complete.
        # Since it runs forever, this will block and keep the server alive.
        loop.run_until_complete(start_websocket_server_async())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
        logging.info("WebSocket server loop closed.")

# --- HTTP Server for TwiML ---
class TwiMLHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests to serve TwiML."""
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()

        response = VoiceResponse()
        response.say(
            voice="Polly.Joanna-Neural",
            message="Hello! I'm SORA, your AI Fitness Coach. How can I help you today?"
        )

        connect = Connect()
        connect.stream(url=f"{NGROK_WEBSOCKET_URL}")
        response.append(connect)
        response.pause(length=2)

        self.wfile.write(str(response).encode('utf-8'))

def run_http_server():
    """Runs the HTTP server."""
    server_address = ('', HTTP_SERVER_PORT)
    httpd = HTTPServer(server_address, TwiMLHandler)
    logging.info(f"HTTP server running on port {HTTP_SERVER_PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Start servers in separate threads
    http_thread = threading.Thread(target=run_http_server)
    websocket_thread = threading.Thread(target=run_websocket_server)

    http_thread.daemon = True
    websocket_thread.daemon = True

    http_thread.start()
    websocket_thread.start()

    # Give servers a moment to start up
    import time
    time.sleep(2)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down.")
