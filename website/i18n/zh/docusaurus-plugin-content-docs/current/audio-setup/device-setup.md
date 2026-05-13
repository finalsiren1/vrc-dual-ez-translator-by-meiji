---
title: 音频设置
sidebar_label: 音频设置
sidebar_position: 1
---

# 音频设置

**Audio Setup (音频设置)** 选项卡是 SyncVRC 音频路由的核心。这里设置不正确是导致 AI 无法拾取您的声音或其他玩家声音的最常见原因。

请按照以下详细分类来正确配置您的硬件和软件音频。

## 1. 选择麦克风 (Outgoing)

此设置控制 AI 监听**发送 (Outgoing)** 翻译系统（您的声音）的内容。

* **选择什么:** 选择您的主要物理麦克风（例如，您的 VR 头显麦克风、USB 电容麦克风或 XLR 接口输入）。
* **重要提示:** 确保您的麦克风在 Windows 中未静音，否则 AI 将只能听到静音。

<img 
  src={require('./img/audio-mic.jpg').default} 
  width="900" 
  alt="Audio Mic" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 2. 选择扬声器回环 (Incoming)

此设置控制 AI 监听**接收 (Incoming)** 翻译系统（其他玩家的声音）的内容。

* **问题:** 语音识别引擎无法直接捕获从物理扬声器或耳机“输出”的音频。
* **解决方案 (虚拟音频):** 您必须选择一个“回环”或“虚拟音频”设备，该设备会在桌面音频到达您的耳机之前拦截它。
* **支持的选项:**
  * **Windows 立体声混音 (Stereo Mix)**（内置于大多数 Windows PC，但可能需要在 Windows 声音设置中启用）。
  * **VB-Cable**（免费虚拟音频线）。
  * **Voicemeeter**（高级音频混合软件）。
  * **Elgato Wave Link** 或 **SteelSeries Sonar**（如果您使用他们各自的硬件）。

<img 
  src={require('./img/audio-speaker.jpg').default} 
  width="900" 
  alt="Audio Speaker" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 3. 启用 VRC 静音同步

专门为 VRChat 打造的关键隐私和优化功能。

* **工作原理:** 启用后，SyncVRC 会读取您的 VRChat OSC 参数。如果您使用 VR 控制器或 VRChat 轮盘菜单静音您的麦克风，SyncVRC 会立即暂停发送 (Outgoing) 翻译。
* **为什么要使用它:** 它可以防止 AI 在您静音时持续监听并将背景噪音发送给您的 API 提供商，从而节省您的 API 额度并确保完全的隐私。

<img 
  src={require('./img/audio-mutesync.jpg').default} 
  width="900" 
  alt="Audio Mute Sync" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

要微调 AI 处理您的语音的方式，请继续前往 [**高级音频设置 (Advanced Audio Settings)**](./advanced-audio) 页面。
