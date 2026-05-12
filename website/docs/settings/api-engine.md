---
title: AI & Translation Engine
sidebar_label: AI & Engine
sidebar_position: 2
---

# AI & Translation Engine Configuration

The **AI & Translation Engine** section is the core of SyncVRC. This is where you configure the cloud services that translate your text and the local hardware that processes your voice.

Incorrect settings here may result in API errors or degraded performance, so please follow this guide carefully.

## Translation Engine

Choose the cloud AI provider that will handle the text translation.

* **Supported Engines:** Google Gemini, DeepL API, and OpenAI.
* **Recommendation:** **Google Gemini** is highly recommended and currently fully optimized for SyncVRC, offering incredibly fast real-time responses and excellent conversational context.

> 🖼️ **[IMAGE PLACEHOLDER: Translation Engine Selection]** *(When ready, replace this line with: `![Translation Engine](/img/settings-engine.png)`)*

---

## API Key Management

To use the cloud translation services, you must provide your own API key from your selected provider.

* **How to Setup:** 1. Select your preferred engine from the dropdown.
  2. Paste your secret API key into the **API Key** input field.
  3. Click **Save**. 
* **Privacy & Streamer Mode:** Once saved, the text field will be locked and your key will be hidden as asterisks (`********`). This prevents you from accidentally leaking your API key while streaming or screen sharing.
* **How to Edit:** Click the **Edit** button to unlock the field, enter your new key, and click Save again.

> 🖼️ **[IMAGE PLACEHOLDER: API Key Input and Save]** *(When ready, replace this line with: `![API Key Setup](/img/settings-apikey.png)`)*

---

## AI Processing Device (Speech-to-Text)

This setting determines which hardware component on your computer runs the offline **Faster-Whisper** speech recognition model.

* **GPU (NVIDIA) - Highly Recommended:** Utilizes your graphics card for blazing-fast, near-instant voice recognition. 
  * *Requirement:* You **MUST** have an NVIDIA graphics card and the [NVIDIA CUDA Toolkit 12.x](./../tutorial/initial-setup) installed.
* **CPU (Fallback):** Utilizes your computer's main processor. 
  * *When to use:* Select this if you have an AMD or Intel GPU, or if you encounter CUDA errors on startup. Note that CPU processing is noticeably slower than GPU processing.

> 🖼️ **[IMAGE PLACEHOLDER: AI Processing Device Selection]** *(When ready, replace this line with: `![AI Device](/img/settings-device.png)`)*

---

## Fixed Model Information

**ℹ️ Note on Accuracy:** For the best balance between translation speed and transcription accuracy, SyncVRC is hardcoded to use the **Whisper 'Medium'** model locally. This ensures the AI accurately understands your pronunciation before sending the text to the cloud, and cannot be changed manually.