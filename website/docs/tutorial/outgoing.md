---
title: Sending Messages (Outgoing)
sidebar_label: Outgoing Translation
sidebar_position: 4
---

# Sending Messages to VRChat (Outgoing)

The **Outgoing System** translates your voice or text and sends it directly to the VRChat Chatbox. This allows other players to read what you are saying in their native language in real-time.

## Prerequisites

Before starting, ensure you are on the **Translation** tab and have configured the following:
1. **Select Microphone:** Choose your physical microphone from the *Audio Setup* tab.
2. **Language Setup:** Set your native spoken language (**From**) and the target language (**Translate to**).

---

## Method 1: Auto Voice Translation (Continuous)

Ideal for hands-free, natural conversations. The AI automatically detects when you speak and when you pause.

1. Select the **Auto (Continuous)** mode.
2. Click the **Start Outgoing** button (or press your assigned hotkey, default: `F2`).
3. The button will turn red, indicating the system is active. Simply speak into your microphone.
4. The AI will process your speech and send the translation to VRChat automatically.

> 🖼️ **[IMAGE PLACEHOLDER: Auto Mode]** *(When ready, replace this line with: `![Auto Mode](/img/outgoing-auto.png)`)*

---

## Method 2: Push-to-Talk (Hold to Speak)

Best for noisy environments or when you only want specific sentences translated.

1. Select the **Push to Record** mode.
2. Click **Start Outgoing** to initialize the AI engine.
3. The **Hold to Speak** button will now become active.
4. Click and hold the **Hold to Speak** button (or hold your assigned Push-to-Talk hotkey) while you are talking.
5. Release the button when you are finished. The translation will process and send immediately.

> 🖼️ **[IMAGE PLACEHOLDER: Push-to-Talk Mode]** *(When ready, replace this line with: `![Push-to-Talk Mode](/img/outgoing-push.png)`)*

---

## Method 3: Manual Text Input

If you prefer typing or need to send a specific phrase without speaking, you can use the Manual Translate box.

1. You **MUST** click **Start Outgoing** first to establish the VRChat connection.
2. Type your message into the **Manual Translate (Type and Send)** text box at the bottom of the left panel.
3. Press **Enter** on your keyboard or click the **Send** button.
4. Your typed text and its translation will be sent to the Chatbox.

> 🖼️ **[IMAGE PLACEHOLDER: Manual Text Input]** *(When ready, replace this line with: `![Manual Text Input](/img/outgoing-manual.png)`)*

---

## Expected Result

Once the AI processes your input, the result will be sent to VRChat via OSC. It will appear above your avatar's head as a chat bubble, typically displaying your original text followed by the translated text.

> 🖼️ **[IMAGE PLACEHOLDER: VRChat Result]** *(When ready, replace this line with: `![VRChat Result Example](/img/outgoing-result.png)`)*