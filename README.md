# AI Fitness Agent

## Product Demo
[Watch the Demo Video Here!](https://youtu.be/V83CpWSFRZg)

## Introduction
This project outlines the architecture and implementation guide for an AI Fitness Agent that users can call from a regular phone. The agent is designed to provide personalized fitness advice, answer questions about workouts and diet, and maintain conversation context. The architecture is built to be extensible, allowing for future integration of features like WhatsApp or video calls.

## Features
*   **Voice Interaction:** Users can interact with the AI agent through natural voice conversations over a regular phone call.
*   **Personalized Fitness Advice:** The AI agent leverages a knowledge base and user-specific plans to provide tailored fitness and diet recommendations.
*   **Contextual Conversations:** A session manager ensures the AI maintains conversation context for a more natural and helpful interaction.
*   **Scalable Architecture:** Designed for easy expansion to include other communication channels like WhatsApp or video.
*   **Real-time Speech Processing:** Utilizes fast Speech-to-Text and natural-sounding Text-to-Speech for a seamless user experience.

## High-Level Architecture

```
📱 User Phone
   |
   | (Inbound Call)
   v
📞 Twilio Programmable Voice
   |
   | (Audio stream via Webhook)
   v
🎙 Speech-to-Text (Deepgram / Whisper API)
   |
   v
🤖 AI Agent Backend
    - LLM (OpenAI GPT-4 Turbo)
    - RAG (LangChain + Vector DB)
    - Session Manager (stores conversation context)
   |
   v
🔊 Text-to-Speech (ElevenLabs / Amazon Polly)
   |
   | (Audio stream back to Twilio)
   v
📱 User Phone
```

## Tech Stack

| Layer          | Service/Tool                                           |
| -------------- | ------------------------------------------------------ |
| Telephony      | Twilio Programmable Voice                              |
| Speech-to-Text | Deepgram API (fast, low-latency) or OpenAI Whisper API |
| AI Backend     | FastAPI (Python) with LangChain for RAG                |
| LLM            | OpenAI GPT-4 Turbo                                     |
| Vector DB      | Pinecone (cloud) or FAISS (local for small scale)      |
| TTS            | ElevenLabs (natural voice)                             |
| Hosting        | Render / Railway / AWS EC2                             |
| Storage        | PostgreSQL (for call logs, user profiles)              |

## Getting Started

This section provides a high-level overview of how to set up and run the AI Fitness Agent. For detailed steps, please refer to the `GEMINI.md` file.

1.  **Twilio Setup:**
    *   Sign up for Twilio and buy a voice-capable phone number.
    *   Configure a Webhook for incoming calls to point to your backend endpoint.
    *   Enable TwiML Bins or Programmable Voice with Media Streams for real-time audio.

2.  **Backend Server (FastAPI):**
    *   Set up a FastAPI application to handle Twilio call events, integrate with STT/TTS, and manage AI logic.
    *   The project structure typically includes `main.py`, `ai_agent.py`, `stt.py`, `tts.py`, `db.py`, and `utils.py`.

3.  **STT Integration:**
    *   Integrate with Deepgram for streaming transcription or OpenAI Whisper API for offline processing.

4.  **AI Fitness Agent Logic:**
    *   Utilize LangChain with a Vector DB (Pinecone or FAISS) to store fitness knowledge and user-specific plans for Retrieval Augmented Generation (RAG).

5.  **TTS Integration:**
    *   Integrate with ElevenLabs for natural-sounding Text-to-Speech, sending the audio back to Twilio for playback.

6.  **Call Flow:**
    *   The system manages the call flow from user inbound call, through STT, AI processing, TTS, and back to the caller, saving call logs and AI responses to a database.

7.  **Hosting:**
    *   Deploy the application using Docker on platforms like Render, Railway, or AWS EC2. `ngrok` can be used for local testing with Twilio.

## Cost Estimate (Per Month, Light Usage - ~1000 minutes)

| Service                | Unit Cost            | Example Usage (1000 min)       | Monthly Cost        |
| ---------------------- | -------------------- | ------------------------------ | ------------------- |
| Twilio Voice (Inbound) | \$0.0075/min         | 1000 min                       | \$7.50              |
| Deepgram STT           | \$0.004/min          | 1000 min                       | \$4.00              |
| ElevenLabs TTS         | \$0.30/1M chars      | \~200k chars (\~1k min speech) | \$6.00              |
| OpenAI GPT-4 Turbo     | \~\$0.01 / 1K tokens | \~100K tokens                  | \$10.00             |
| Hosting (Render)       | Fixed                | —                              | \$7–\$15            |
| **Total**              | —                    | —                              | **\$35–\$45/month** |

## Deployment Plan

*   **Week 1:** Set up Twilio number & basic FastAPI webhook.
*   **Week 2:** Integrate Deepgram STT + GPT-4 backend.
*   **Week 3:** Add ElevenLabs TTS + send back to Twilio.
*   **Week 4:** Add persistence (PostgreSQL), deploy on Render, test at scale.

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3. See the [LICENSE](LICENSE) file for details.
