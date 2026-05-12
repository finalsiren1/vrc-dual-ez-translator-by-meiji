---
title: Troubleshooting Guide
sidebar_label: Troubleshooting
sidebar_position: 8
---

# Troubleshooting & Common Issues

If you run into issues while using SyncVRC, please check this guide for the most common problems and their solutions before reporting a bug.

## 1. AI Processing & Hardware Errors

**Error:** `CUDA/GPU Error: No compatible NVIDIA GPU found.` or the app crashes when starting the microphone.
* **Cause:** The app is trying to use your GPU to process the Faster-Whisper model, but it cannot find the required NVIDIA drivers.
* **Solution:** * If you have an **NVIDIA GPU**, you MUST install the [NVIDIA CUDA Toolkit 12.x](./tutorial/initial-setup). Restart your PC after installing.
  * If you have an **AMD, Intel, or no dedicated GPU**, go to the **Settings** tab and change the **AI Processing Device** to `CPU (Fallback)`.

## 2. API & Translation Errors

**Error:** `API Limit Exceeded: Too many requests.`
* **Cause:** You are using a Free Tier API key (especially Google Gemini) and have spoken too much, too fast, hitting the rate limit.
* **Solution:** Pause speaking for a minute to let the limit reset. For a permanent fix, upgrade your API account to a Pay-as-you-go billing plan. Alternatively, switch your SyncVRC mode from *Auto (Continuous)* to *Push to Record*.

**Error:** `API Error: Invalid API Key.`
* **Cause:** Your API key is empty, incorrectly copied, or your cloud provider account is restricted.
* **Solution:** Double-check your API key in the **Settings** tab. Ensure there are no extra spaces at the beginning or end of the key.

**Error:** `API Request Error: 400 Bad Request` (or similar 400 errors)
* **Cause:** This usually happens if the AI model name was changed by the provider, or if the text sent violates the cloud provider's safety guidelines (e.g., extreme profanity).
* **Solution:** SyncVRC has safety filters disabled by default, but providers may still hard-block certain words. Try speaking a different sentence.

## 3. VRChat OSC Connection Issues

**Issue:** OSC Status shows `🔴 Not Detected` or translations are not appearing in VRChat.
* **Cause:** VRChat is not sending or receiving OSC data on the default port (`9000`).
* **Solution:** 1. Open your VRChat Radial Menu.
  2. Go to **Options > OSC** and toggle it **Off**, then turn it back **On** to reset the connection.
  3. Ensure no other OSC applications (like face trackers or heart rate monitors) are blocking port `9000` or `9001`.

## 4. Audio Routing & Microphone Problems

**Issue:** The Incoming System is transcribing my own voice, or transcribing YouTube videos.
* **Cause:** You selected your physical Speakers or Headphones in the *Speaker Loopback* setting.
* **Solution:** You must use a Virtual Audio Cable (like VB-Cable) or Windows Stereo Mix. Route ONLY VRChat's audio to this virtual cable, and select that virtual cable in SyncVRC's Incoming settings.

**Issue:** The app says "Listening..." but never translates my voice.
* **Cause:** The AI cannot hear you, or your microphone volume is too low.
* **Solution:** * Ensure your microphone is not hardware-muted.
  * Check Windows Sound Settings to ensure your microphone is the default input device and the input volume is high enough.
  * Adjust the **Silence Timeout** in Advanced Audio Settings; if it's too high, the AI might wait too long before processing.

## 5. Mute Sync is not working
**Issue:** I muted my mic in VRChat, but SyncVRC keeps translating.
* **Cause:** OSC is not enabled, or you did not check the Mute Sync box.
* **Solution:** Go to **Audio Setup** and ensure **Enable VRC Mute Sync** is checked. Also, verify that the OSC Status in the bottom left is green (`🟢 Detected`).

---

## Still Need Help?

If your issue is not listed here, please ensure you have **Telemetry (Crash Reports)** enabled in the Settings tab. This allows the app to securely send error logs to the developer. 

You can also reach out for support or report bugs on our [GitHub Issues page](https://github.com/finalsiren1/SyncVRC/issues).