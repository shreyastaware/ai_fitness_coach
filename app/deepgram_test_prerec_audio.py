# main.py (python example)

import sys
print('sys modeule')
print(sys.executable)
print()
print(sys.path)

import os
print('OS MOdule')
print(os.getcwd())

import logging
from deepgram.utils import verboselogs


from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
)

AUDIO_URL = {
    "url": "https://dpgr.am/bueller.wav"
}

from dotenv import load_dotenv
load_dotenv('/Users/shreyastaware/Desktop/ai_fitness_coach/app/.env')

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

def main():
    try:
        # STEP 1 Create a Deepgram client using the DEEPGRAM_API_KEY from your environment variables
        deepgram: DeepgramClient = DeepgramClient(DEEPGRAM_API_KEY)

        # STEP 2 Call the transcribe_url method on the rest class
        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-3",
            smart_format=True,
        )
        response = deepgram.listen.rest.v("1").transcribe_url(AUDIO_URL, options)
        # print(f"response: {response}\n\n")

        print(f'Output: {response["results"]["channels"][0]["alternatives"][0]["transcript"]}')

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
