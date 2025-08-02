# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# lines on local machine
from dotenv import load_dotenv
load_dotenv('/Users/shreyastaware/Desktop/ai_fitness_coach/app/.env')

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("MY_TWILIO_PHONE_NUMBER")

print(twilio_number)

def text_to_speech(text: str):
    """
    Converts text to speech using a text-to-speech service.
    (Placeholder for ElevenLabs or other TTS integration)
    """
    # In this setup, we are using Twilio's built-in TTS via the Say verb.
    # This function is a placeholder for if you switch to a different provider.
    pass


def call_someone_using_twilio_number(country_id, phone_number):
    client = Client(account_sid, auth_token)

    call = client.calls.create(
    # url="http://demo.twilio.com/docs/voice.xml",
    url = "https://handler.twilio.com/twiml/EHb03d0a5b07e6a2373f037d8c42719a37",
    # twiml="<Response><Say>Hello! I am SORA, your AI fitness agent. How can I help you today?</Say></Response>",
    to=f"+{country_id}{phone_number}",
    from_=twilio_number
    )

    print(call)

    print()

if __name__ == "__main__":
    call_someone_using_twilio_number(91, 9881039025)