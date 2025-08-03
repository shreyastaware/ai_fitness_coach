import os
import logging

from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv('/Users/shreyastaware/Desktop/ai_fitness_coach/app/.env')

# Set up logging
logging.basicConfig(level=logging.INFO)

# --- Configuration ---
# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER") # Your Twilio phone number
RECIPIENT_PHONE_NUMBER = os.environ.get("RECIPIENT_PHONE_NUMBER") # The number to call
HTTPS_WEBSOCKET_URL = os.environ.get("HTTPS_WEBSOCKET_URL")

# --- Main Application ---
def make_call():
    """Makes an outbound call using Twilio."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER]):
        logging.error("Twilio credentials are not set. Please set the environment variables.")
        return

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        call = client.calls.create(
            to=RECIPIENT_PHONE_NUMBER,
            # to="+918809779946",
            from_=TWILIO_PHONE_NUMBER,
            url=HTTPS_WEBSOCKET_URL
        )
        logging.info(f"Call initiated with SID: {call.sid}")
    except Exception as e:
        logging.error(f"Error making call: {e}")


if __name__ == "__main__":
    # Make the call
    make_call()