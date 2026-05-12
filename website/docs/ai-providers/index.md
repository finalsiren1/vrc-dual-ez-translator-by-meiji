---
title: Cloud AI Providers
sidebar_label: AI Providers
sidebar_position: 5
---

# Cloud AI Providers & API Keys

Welcome to the Cloud AI section. In SyncVRC, we utilize a hybrid AI approach to deliver real-time, highly accurate translations without impacting your VR gaming performance.

## How SyncVRC Uses AI

The translation pipeline is split into two specialized tasks:
1. **Speech-to-Text (Local):** We use the **Faster-Whisper** model running entirely on your local machine to convert your voice into text. This ensures instant speech recognition.
2. **Contextual Translation (Cloud):** Once your speech is transcribed, the text is sent to an advanced **Cloud AI API** (such as Google Gemini, DeepL, or OpenAI) to be translated into the target language. 

## Why Not Use Local Translation Models?

You might wonder why SyncVRC does not run the translation language model locally alongside Faster-Whisper. The answer is **System Performance**.

Running a high-quality Large Language Model (LLM) capable of natural, context-aware translation requires a massive amount of computational power and Video RAM (VRAM). Running a heavy local LLM simultaneously with a demanding VR game like VRChat and the Faster-Whisper model would severely bottleneck your PC. It would cause massive frame drops, lag, and an unplayable VR experience.

By offloading the text translation step to Cloud APIs, SyncVRC guarantees:
* **Zero Impact on Gaming:** Your PC's resources remain fully dedicated to running VRChat smoothly.
* **Lightning-Fast Speed:** Sending small text strings to cloud servers takes only milliseconds.
* **Superior Accuracy:** Cloud APIs leverage massive, multi-billion parameter models that understand slang, context, and grammar far better than any lightweight local model.

## Getting Your API Keys

To connect SyncVRC to these cloud services, you must provide a personal API Key from your chosen AI provider. 

Please select a provider from the sidebar on the left, or click **"Next"** to learn how to register and obtain a **Google Gemini API Key**.