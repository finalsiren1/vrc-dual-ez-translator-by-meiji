---
title: 初始设置
sidebar_label: 初始设置
sidebar_position: 3
---

# 初始设置

在开始使用 SyncVRC 之前，需要进行一些必要的配置，以确保 AI 和通信系统正常运行。

## 1. 获取 API 密钥

SyncVRC 需要您首选的云 AI 提供商（例如 Google Gemini、DeepL 或 OpenAI）的 API 密钥来处理翻译。

1. 注册您选择的 AI 提供商的帐户。
2. 导航到其开发者或 API 仪表板以生成新的 API 密钥。
3. 复制您的 API 密钥并妥善保管。您将把它输入到应用的 **Settings (设置)** 选项卡中。

> **建议:** 虽然有免费层级可用（例如 Gemini 免费层级），但它们通常强制执行严格的速率限制，这会导致翻译延迟或暂停。为了获得无缝、不间断的实时体验，我们强烈建议将您的提供商升级到按量付费（预付）的计费计划。

## 2. 安装 NVIDIA CUDA Toolkit (可选)

SyncVRC 可以利用您的 GPU 进行高速语音识别 (Faster-Whisper)。但是，这是**可选的**，并且专门针对 NVIDIA GPU 进行了优化。

* **对于 NVIDIA 用户**: 为了获得最大性能，请下载并安装 [NVIDIA CUDA Toolkit 12.x](https://developer.nvidia.com/cuda-12-9-1-download-archive)。**注意:** 安装后必须重启您的电脑。
* **对于 AMD/Intel 或无 GPU 用户**: 您不需要安装 CUDA。应用程序将自动回退到使用您的 CPU。
* **更改设备**: 您可以随时在 [**Settings > AI & Translation Engine**](../settings/api-engine) 中手动切换 GPU 和 CPU 处理。

## 3. 启用 VRChat OSC

该应用程序通过 OSC 协议与 VRChat 通信，以在聊天框中打字并同步您的静音状态。

1. 启动 VRChat 并打开您的**轮盘菜单 (Radial Menu)**。
2. 导航到 **Options > OSC**。
3. 将 OSC 设置为 **Enabled (启用)**。

**检查 OSC 状态:** 启用且 VRChat 正在运行后，检查 SyncVRC 侧边栏的左下方。**OSC Status** 指示器应更新为 **🟢 Detected** 以确认连接成功。

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

## 4. 音频设备配置

正确的音频路由是成功翻译的关键。

* **Outgoing (发送)**: 选择您的物理麦克风。
* **Incoming (接收)**: 选择捕获桌面/游戏音频的**回环 (Loopback)**或**虚拟音频设备 (Virtual Audio Device)**（例如 VB-Cable、Voicemeeter）。您无法直接选择您的物理扬声器。
