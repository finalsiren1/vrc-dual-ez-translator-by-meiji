---
slug: /
title: Tutorial
sidebar_label: Tutorial
sidebar_position: 1
---

# Welcome to SyncVRC

This documentation will guide you through the basic features, installation, and setup of SyncVRC. Follow the steps below to get started.

## What is SyncVRC?

SyncVRC is a real-time voice translation tool designed specifically for VRChat. It leverages local AI (Faster-Whisper) for highly accurate speech recognition and advanced Cloud APIs (Gemini, DeepL, OpenAI) for contextual translation, enabling seamless cross-language communication in virtual reality.

## Main Features

* 🎙️ **Dual-Way Translation**: Operates both an Outgoing system (translating your voice to the VRChat Chatbox) and an Incoming system (translating others' voices to your screen) simultaneously.
* 🔇 **Smart VRC Mute Sync**: Reads VRChat OSC parameters to automatically pause outgoing translations when your microphone is muted in-game, ensuring privacy and conserving API quotas.
* 🔄 **Full-Auto Updater**: Includes a built-in automatic updater for seamless, one-click software patches without manual file replacement.
* 🔒 **Absolute Privacy**: Stores API keys strictly on your local machine (`config.json`) and communicates directly with official API endpoints. No voice data or keys are collected or stored remotely.
* ⚙️ **Pro-Level Audio Control**: Provides granular adjustments for AI accuracy (Beam Size), silence timeouts, and maximum recording durations to match your personal speaking cadence.

### ⚠️ Important Notice: API Key Required

To be completely transparent, **SyncVRC cannot function without an API Key** for the translation services (like Gemini, DeepL, or OpenAI). You must obtain your own API key to use this software. 

We highly recommend using a **Paid API Key** if possible. Free tier keys often have strict rate limits which will cause translations to pause, skip, or fail during continuous conversation, leading to a frustrating experience. For details on how to get an API key, please visit: [AI Providers & API Setup](https://finalsiren1.github.io/SyncVRC/ai-providers)

## Get Started

### How to Install

Please refer to the [Installation Guide](./tutorial/installation) for detailed instructions on how to download, install, and properly run SyncVRC on your system.