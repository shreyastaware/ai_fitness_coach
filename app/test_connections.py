#!/usr/bin/env python3
"""
Test script to verify all API connections work properly
"""
import asyncio
import json
import logging
import os
import websockets
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

async def test_deepgram():
    """Test Deepgram connection"""
    print("Testing Deepgram connection...")
    try:
        url = "wss://api.deepgram.com/v1/listen?encoding=mulaw&sample_rate=8000&channels=1"
        headers = {'Authorization': f'Token {DEEPGRAM_API_KEY}'}
        
        async with websockets.connect(url, extra_headers=headers) as ws:
            print("✅ Deepgram connection successful")
            return True
    except Exception as e:
        print(f"❌ Deepgram connection failed: {e}")
        return False

async def test_openai():
    """Test OpenAI connection"""
    print("Testing OpenAI connection...")
    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ OpenAI connection successful")
        return True
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

async def test_elevenlabs():
    """Test ElevenLabs connection"""
    print("Testing ElevenLabs connection...")
    try:
        voice_id = "EXAVITQu4vr4xnSDxMaL"
        url = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_turbo_v2&output_format=pcm_16000"
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        
        async with websockets.connect(url, extra_headers=headers) as ws:
            # Send initial config
            await ws.send(json.dumps({
                "text": " ",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
            }))
            print("✅ ElevenLabs connection successful")
            return True
    except Exception as e:
        print(f"❌ ElevenLabs connection failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("Running API connection tests...\n")
    
    results = await asyncio.gather(
        test_deepgram(),
        test_openai(),
        test_elevenlabs(),
        return_exceptions=True
    )
    
    success_count = sum(1 for r in results if r is True)
    print(f"\n{success_count}/3 connections successful")
    
    if success_count == 3:
        print("🎉 All connections working!")
    else:
        print("⚠️  Some connections failed. Check your API keys and network.")

if __name__ == "__main__":
    asyncio.run(main())