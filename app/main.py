from fastapi import FastAPI, Form, Response, Request
from twilio.twiml.voice_response import VoiceResponse, Gather

# Import other modules
from . import ai_agent, stt, tts

app = FastAPI()

@app.post("/voice")
async def voice(request: Request):
    """Respond to incoming phone calls with a welcome message and gather user input."""
    response = VoiceResponse()
    
    # Greet the user
    response.say("Hello, welcome to the AI Fitness Coach. How can I help you today?")

    # Use Gather to collect speech and send it to /handle_speech
    gather = Gather(input='speech', action='/handle_speech', speechTimeout='auto')
    response.append(gather)

    # If the user doesn't say anything, redirect to listen again
    response.redirect('/voice')

    return Response(content=str(response), media_type="application/xml")


@app.post("/handle_speech")
async def handle_speech(request: Request, SpeechResult: str = Form(...)):
    """
    Handle the speech input from the user, process it, and respond.
    """
    response = VoiceResponse()

    # Get the user's speech from the form data
    user_input = SpeechResult

    # 1. (Future) Transcribe if using a different STT provider. With Twilio, it's automatic.
    # transcribed_text = stt.transcribe_audio(audio_stream) 

    # 2. Get a response from the AI agent
    ai_response_text = ai_agent.get_response(user_input)

    # 3. (Future) Convert the AI's text response to speech audio
    # audio_url = tts.text_to_speech(ai_response_text)
    # For now, we'll use Twilio's built-in TTS
    response.say(ai_response_text)
    
    # 4. Play the audio back to the user
    # response.play(audio_url)

    # Redirect to the main voice loop to continue the conversation
    response.redirect('/voice')

    return Response(content=str(response), media_type="application/xml")


@app.get("/")
def read_root():
    return {"Hello": "World"}