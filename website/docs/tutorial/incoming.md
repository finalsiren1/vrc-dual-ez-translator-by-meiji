---
title: Receiving Messages (Incoming)
sidebar_label: Incoming Translation
sidebar_position: 5
---

# Translating Others (Incoming)

The **Incoming System** listens to the audio coming from your game (other players' voices) and translates it into your native language. Unlike the Outgoing system, these translations are displayed privately on your SyncVRC app interface and are **not** sent to the VRChat Chatbox.

## Prerequisites: Audio Routing (Crucial Step)

To translate other players, the app needs to "hear" your game audio. **You cannot simply select your physical "Speakers" or "Headphones" directly.**

1. Go to the **Audio Setup** tab.
2. Under the **Select Speaker Loopback (Virtual Audio)** dropdown, you must select a loopback device.
3. *Recommended Virtual Audio Devices:* Windows Stereo Mix, VB-Cable, Voicemeeter, or Elgato Wave Link.

> 🖼️ **[IMAGE PLACEHOLDER: Audio Routing Setup]** *(When ready, replace this line with: `![Audio Routing Setup](/img/incoming-audio.png)`)*

---

## How to Use the Incoming System

Once your audio is routed correctly, follow these steps to start translating:

### 1. Language Setup
On the right panel of the **Translation** tab, configure your languages:
* **Listen Language:** Set this to the language the other players are speaking (e.g., Japanese).
* **Translate to:** Set this to your native language (e.g., English).

### 2. Start the Engine
Click the **Start Incoming** button (or press your assigned hotkey, default: `F3`). The button will turn red to indicate it is actively listening to your desktop audio.

> 🖼️ **[IMAGE PLACEHOLDER: Incoming Setup and Start]** *(When ready, replace this line with: `![Start Incoming](/img/incoming-start.png)`)*

### 3. Read the Translation
When the other person speaks, the AI will process the audio in real-time. The original text and the translated text will appear in the **Incoming Log** text box at the bottom right of the app.

> 🖼️ **[IMAGE PLACEHOLDER: Incoming Log Result]** *(When ready, replace this line with: `![Incoming Result](/img/incoming-result.png)`)*

---

**💡 Pro Tip:** You can run both the **Outgoing** and **Incoming** systems at the same time to have a seamless, two-way translated conversation!