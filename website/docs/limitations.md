---
title: Current Limitations
sidebar_label: Limitations
sidebar_position: 6
---

# Current Limitations & Known Issues

To provide full transparency, we want to outline the current technical and practical limitations of SyncVRC. We believe in being upfront about what the software can and cannot do. Understanding these constraints will help you set the right expectations and optimize your experience.

## 1. VRChat Chatbox Character Limits & Delays
* **The Constraint:** VRChat imposes a strict limit of **144 characters** per chatbox message.
* **How SyncVRC Handles It:** If your translated sentence exceeds 144 characters, SyncVRC automatically slices the text into smaller chunks. To avoid triggering VRChat's anti-spam filters, the app forces a **1.8-second delay** before sending the next chunk.
* **The Reality:** Long monologues or extremely long sentences will take several seconds to fully render above your avatar's head. Keep your sentences relatively short for the best real-time experience.

## 2. API Rate Limits (Free Tiers)
* **The Constraint:** Free API keys (especially the Google Gemini Free Tier) come with strict "Requests Per Minute" (RPM) quotas.
* **The Reality:** If you use the **Auto (Continuous)** mode and speak frequently, you will likely hit this quota very quickly. The app will throw an `API Limit Exceeded` error and pause translations until the cloud provider resets your limit.
* **The Solution:** Use **Push-to-Talk** to minimize unnecessary API calls, or upgrade your API account to a Pay-as-you-go billing plan.

## 3. Hardware & VR Performance Bottlenecks
* **The Constraint:** SyncVRC transcribes your voice entirely locally using the **Faster-Whisper (Medium)** model to ensure privacy and low latency.
* **The Reality:**
  * **GPU Mode:** If you have a modern NVIDIA GPU, transcription is near-instant.
  * **CPU Mode:** If you are using an AMD/Intel GPU or have not installed CUDA, the app falls back to your CPU. Running VRChat in VR alongside a local AI model on your CPU is incredibly resource-heavy. You may experience noticeable transcription delays, PC lag, or frame drops in VR if your processor is not powerful enough.

## 4. Audio Isolation (Incoming System)
* **The Constraint:** SyncVRC's Incoming System captures audio using a Virtual Audio Cable or Loopback device. It listens to the entire audio stream routed through that device.
* **The Reality:** The app **cannot** isolate VRChat player voices from other desktop sounds. If you are watching YouTube, listening to Spotify, or getting Discord notifications while the Incoming System is active, the AI will attempt to transcribe and translate that background noise as well, resulting in chaotic or nonsensical logs.

## 5. Context and Slang Translation
* **The Constraint:** Cloud AI translation engines process text almost sentence-by-sentence to maintain high speed.
* **The Reality:** The AI does not retain long-term memory of a 10-minute conversation. It may occasionally mistranslate highly contextual VRChat slang, niche anime terminology, or specific character names, as it lacks the full visual and historical context of your current VR session.