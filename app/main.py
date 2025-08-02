from fastapi import FastAPI, Form, Response, Request
from twilio.twiml.voice_response import VoiceResponse, Gather

# Import other modules
# from . import ai_agent, stt, tts

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    app.run()