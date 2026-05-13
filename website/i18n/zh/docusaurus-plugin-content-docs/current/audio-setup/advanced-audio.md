---
title: ⚙️ 高级音频设置
sidebar_label: ⚙️ 高级音频设置
sidebar_position: 2
---

# ⚙️ 高级音频设置

这些滑块允许您微调 AI 处理语音的方式，帮助您平衡速度、准确性以及您的个人语速。

## Silence Timeout (静音超时) (0.3秒 - 2.0秒)
* **作用:** 决定在您停止说话后，AI 等待多长时间才认为句子已“完成”并将其发送出去进行翻译。
* **建议:** 如果您说话很快，请将其保持在较低水平（例如 `0.5s`）。如果您倾向于在句子中间停顿和思考，请增加它（例如 `1.0s` 或更高），以免您的句子被截断成两半。

## Max Recording Time (最大录音时间) (5秒 - 30秒)
* **作用:** 设置 AI 在强制翻译之前录制单个短语的最长硬性限制。
* **建议:** 保持在 `15s` 左右。如果设置得太高，而您不停顿地连续说话，可能会导致翻译极其严重的延迟。

## AI Accuracy vs Speed [Beam Size] (AI 准确度与速度 [Beam Size]) (1 - 5)
* **作用:** 调整 Faster-Whisper 模型的“Beam Size”。
* **建议:**
  * 较低的值 (1-2): 处理速度更快，但上下文准确性略低。
  * 较高的值 (4-5): 高度准确，但需要更多的 GPU 算力，并且处理时间略长。默认值为 `2`。

<img 
  src={require('./img/audio-advanced.jpg').default} 
  width="900" 
  alt="Audio Advanced" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>
