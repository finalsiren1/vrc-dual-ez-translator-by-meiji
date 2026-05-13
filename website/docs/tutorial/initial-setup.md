---
title: Initial Setup
sidebar_label: Initial Setup
sidebar_position: 3
---

# Initial Setup

Before you start using SyncVRC, there are a few essential configurations required to ensure the AI and communication systems function correctly.

## 1. Obtain an API Key

SyncVRC requires an API key from your preferred Cloud AI provider (e.g., Google Gemini, DeepL, or OpenAI) to process translations.

1.  Register an account with your chosen AI provider.
2.  Navigate to their developer or API dashboard to generate a new API key.
3.  Copy your API key and keep it secure. You will enter this into the app's **Settings** tab.

> **Recommendation:** While free tiers are available (such as the Gemini Free Tier), they often enforce strict rate limits that can cause translation delays or pauses. For a seamless, uninterrupted real-time experience, we highly recommend upgrading to a Pay-as-you-go (prepaid) billing plan with your provider.

## 2. Install NVIDIA CUDA Toolkit (Optional)

SyncVRC can utilize your GPU for high-speed voice recognition (Faster-Whisper). However, this is **optional** and specifically optimized for NVIDIA GPUs.

* **For NVIDIA Users**: To achieve maximum performance, download and install the [NVIDIA CUDA Toolkit 12.x](https://developer.nvidia.com/cuda-12-9-1-download-archive). **Note:** You must restart your PC after installation.
* **For AMD/Intel or No GPU Users**: You do not need to install CUDA. The application will automatically fall back to using your CPU.
* **Changing the Device**: You can always switch between GPU and CPU processing manually in the [**Settings > AI & Translation Engine**](../settings/api-engine).

## 3. Enable VRChat OSC

The app communicates with VRChat via the OSC protocol to type in the chatbox and sync your mute status.

1.  Launch VRChat and open your **Radial Menu**.
2.  Navigate to **Options > OSC**.
3.  Set OSC to **Enabled**.

**Checking OSC Status:** Once enabled and VRChat is running, check the bottom left of your SyncVRC sidebar. The **OSC Status** indicator should update to **🟢 Detected** to confirm a successful connection.

<div style={{ display: 'flex', justifyContent: 'center', gap: '15px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/osc-1.jpg').default} width="30%" alt="OSC-1" />
  <img src={require('./img/osc-2.jpg').default} width="30%" alt="OSC-2" />
  <img src={require('./img/osc-3.jpg').default} width="30%" alt="OSC-3" />
</div>

<img 
  src={require('./img/osc-detected.jpg').default} 
  width="900" 
  alt="Select Language" 
  style={{ marginTop: '20px', marginBottom: '0px', marginLeft: '30px' }} 
/>

## 4. Audio Device Configuration

Proper audio routing is key to successful translation.

* **Outgoing**: Select your physical microphone.
* **Incoming**: Select a **Loopback** or **Virtual Audio Device** (e.g., VB-Cable, Voicemeeter) that captures your desktop/game audio. You cannot select your physical speakers directly.