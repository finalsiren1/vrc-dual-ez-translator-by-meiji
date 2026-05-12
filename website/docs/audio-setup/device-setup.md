---
title: Audio Device Setup
sidebar_label: Audio Devices
sidebar_position: 1
---

# Audio Device Setup

The **Audio Setup** tab is the core of SyncVRC's audio routing. Incorrect settings here are the most common cause of the AI failing to pick up your voice or the voices of other players.

Follow this detailed breakdown to configure your hardware and software audio correctly.

## 1. Select Microphone (Outgoing)

This setting controls what the AI listens to for the **Outgoing** translation system (your voice).

* **What to select:** Choose your primary, physical microphone (e.g., your VR headset microphone, a USB condenser mic, or an XLR interface input).
* **Important:** Ensure your microphone is not muted in Windows, or the AI will only hear silence.

> 🖼️ **[IMAGE PLACEHOLDER: Microphone Selection]** *(When ready, replace this line with: `![Microphone Setup](/img/audio-mic.png)`)*

---

## 2. Select Speaker Loopback (Incoming)

This setting controls what the AI listens to for the **Incoming** translation system (other players' voices).

* **The Problem:** The speech recognition engine cannot directly capture audio coming *out* of your physical speakers or headphones.
* **The Solution (Virtual Audio):** You must select a "Loopback" or "Virtual Audio" device that intercepts your desktop audio before it reaches your headphones. 
* **Supported Options:**
  * **Windows Stereo Mix** (Built into most Windows PCs, but may need to be enabled in Windows Sound Settings).
  * **VB-Cable** (Free virtual audio cable).
  * **Voicemeeter** (Advanced audio mixing software).
  * **Elgato Wave Link** or **SteelSeries Sonar** (If you use their respective hardware).

> 🖼️ **[IMAGE PLACEHOLDER: Loopback Selection]** *(When ready, replace this line with: `![Speaker Loopback Setup](/img/audio-speaker.png)`)*

---

## 3. Enable VRC Mute Sync

A crucial privacy and optimization feature built specifically for VRChat.

* **How it works:** When enabled, SyncVRC reads your VRChat OSC parameters. If you mute your microphone using your VR controller or the VRChat radial menu, SyncVRC instantly pauses the Outgoing translation.
* **Why use it:** It prevents the AI from continuously listening and sending background noise to your API provider while you are muted, saving your API quota and ensuring complete privacy.

> 🖼️ **[IMAGE PLACEHOLDER: Mute Sync Checkbox]** *(When ready, replace this line with: `![VRC Mute Sync](/img/audio-mutesync.png)`)*

---

To fine-tune how the AI processes your speech, please proceed to the [**Advanced Audio Settings**](./advanced-audio) page.