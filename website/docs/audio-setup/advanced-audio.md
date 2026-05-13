---
title: Advanced Audio Settings
sidebar_label: Advanced Audio
sidebar_position: 2
---

# Advanced Audio Settings

These sliders allow you to fine-tune how the AI processes speech, helping you balance speed, accuracy, and your personal speaking cadence.

## Silence Timeout (0.3s - 2.0s)
* **What it does:** Determines how long the AI waits after you stop speaking before it considers the sentence "finished" and sends it for translation.
* **Recommendation:** If you speak fast, keep it low (e.g., `0.5s`). If you tend to pause and think in the middle of sentences, increase it (e.g., `1.0s` or higher) so your sentences aren't cut in half.

## Max Recording Time (5s - 30s)
* **What it does:** Sets a hard limit on how long the AI will record a single phrase before forcing a translation. 
* **Recommendation:** Keep it around `15s`. Setting this too high might cause extremely long delays in translation if you speak continuously without pausing.

## AI Accuracy vs Speed [Beam Size] (1 - 5)
* **What it does:** Adjusts the "Beam Size" of the Faster-Whisper model.
* **Recommendation:** * Lower values (1-2): Faster processing, but slightly less accurate context.
  * Higher values (4-5): Highly accurate, but requires more GPU power and takes slightly longer to process. Default is `2`.

<img 
  src={require('./img/audio-advanced.jpg').default} 
  width="900" 
  alt="Audio Advanced" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>