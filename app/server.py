import asyncio
import base64
import json
import logging
import os
import threading
import wave
from http.server import BaseHTTPRequestHandler, HTTPServer

import numpy as np
import websockets
from twilio.rest import Client
from fastapi import FastAPI, WebSocket
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect

from dotenv import load_dotenv
load_dotenv('/Users/shreyastaware/Desktop/ai_fitness_coach/app/.env')

# Server configuration
HTTP_SERVER_PORT = 8080
WEBSOCKET_SERVER_PORT = 8081
# This should be your ngrok forwarding URL for the WebSocket server
# e.g., "wss://your-ngrok-subdomain.ngrok.io"
NGROK_WEBSOCKET_URL = "wss://63e5763bef49.ngrok-free.app"

# Set up logging
logging.basicConfig(level=logging.INFO)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# DEEPGRAM_URL = "wss://api.deepgram.com/v1/listen"
DEEPGRAM_URL = "wss://api.deepgram.com/v1/listen?encoding=mulaw&sample_rate=8000&channels=1&punctuate=true"

# app = Fas

# --- WebSocket Server ---
async def websocket_handler(twilio_ws):
    """Handles WebSocket connections from Twilio."""
    logging.info("WebSocket connection established.")
    try:
        """
        Handles the WebSocket connection from Twilio and proxies audio to Deepgram.
        """
        logging.info("Twilio WebSocket connection established.")
        
        extra_headers = {'Authorization': f'Token {DEEPGRAM_API_KEY}'}
        
        async with websockets.connect(DEEPGRAM_URL, additional_headers=extra_headers) as deepgram_ws:
            logging.info("Successfully connected to Deepgram.")

            # Event to signal that the call has ended and we should shut down.
            shutdown_event = asyncio.Event()

            async def twilio_receiver(twilio_ws, deepgram_ws, shutdown_event):
                """Receives audio from Twilio and sends it to Deepgram."""
                try:
                    async for message in twilio_ws:
                        data = json.loads(message)
                        
                        if data['event'] == 'media':
                            payload = data['media']['payload']
                            # The audio is already in mu-law format, just need to decode from base64
                            chunk = base64.b64decode(payload)
                            await deepgram_ws.send(chunk)
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
                """Receives transcriptions from Deepgram and prints them."""
                while not shutdown_event.is_set():
                    try:
                        # Wait for a message from Deepgram or a shutdown signal.
                        deepgram_task = asyncio.create_task(deepgram_ws.recv())
                        shutdown_task = asyncio.create_task(shutdown_event.wait())

                        done, pending = await asyncio.wait(
                            [deepgram_task, shutdown_task],
                            return_when=asyncio.FIRST_COMPLETED
                        )
                        
                        # Cancel any pending tasks to avoid them running in the background.
                        for task in pending:
                            task.cancel()

                        if deepgram_task in done:
                            message = deepgram_task.result()
                            data = json.loads(message)
                            if data.get('is_final') and data['channel']['alternatives'][0]['transcript']:
                                transcript = data['channel']['alternatives'][0]['transcript']
                                logging.info(f"TRANSCRIPT: {transcript}")
                        else:
                            # Shutdown event was triggered
                            break
                    except websockets.exceptions.ConnectionClosed:
                        logging.info("Deepgram connection closed by server.")
                        break
            # Run both receivers concurrently
            await asyncio.gather(
                twilio_receiver(twilio_ws, deepgram_ws, shutdown_event),
                deepgram_receiver(deepgram_ws, shutdown_event)
            )
            
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
        response.say("Connecting you to the audio stream.")
        connect = Connect()
        connect.stream(url=f"{NGROK_WEBSOCKET_URL}")
        response.append(connect)

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
