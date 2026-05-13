---
title: 输出系统 (语音 -> VRChat)
sidebar_label: 输出系统 (语音 -> VRChat)
sidebar_position: 4
---

# 输出系统 (语音 -> VRChat)

**发送 (Outgoing) 系统**会翻译您的语音或文本，并将其直接发送到 VRChat 聊天框。这允许其他玩家实时以他们的母语阅读您正在说的内容。

## 先决条件

开始之前，请确保您在 **Translation (翻译)** 选项卡上并已配置以下内容：
1. **Select Microphone (选择麦克风):** 从 *Audio Setup (音频设置)* 选项卡中选择您的物理麦克风。
2. **Language Setup (语言设置):** 设置您的母语 (**From (从)**) 和目标语言 (**Translate to (翻译为)**)。

---

## 方法 1：自动语音翻译（连续）

非常适合免提、自然的对话。AI 会自动检测您何时说话以及何时停顿。

1. 选择 **Auto (Continuous) (自动(连续))** 模式。
2. 点击 **Start Outgoing (开始发送)** 按钮（或按下您分配的热键，默认：`F2`）。
3. 按钮将变为红色，表示系统处于活动状态。只需对着麦克风说话即可。
4. AI 将处理您的语音并自动将翻译发送到 VRChat。

<img 
  src={require('./img/auto-voice.jpg').default} 
  width="900" 
  alt="Auto Voice" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 方法 2：按键说话（按住说话）

最适合嘈杂的环境或当您只想翻译特定句子时。

1. 选择 **Push to Record (按住录音)** 模式。
2. 点击 **Start Outgoing (开始发送)** 初始化 AI 引擎。
3. **Hold to Speak (按住说话)** 按钮现在将变为活动状态。
4. 在您说话时点击并按住 **Hold to Speak** 按钮（或按住您分配的按键说话热键）。
5. 完成后松开按钮。翻译将被处理并立即发送。

<img 
  src={require('./img/push-to-talk.jpg').default} 
  width="900" 
  alt="Push to Talk" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 方法 3：手动文本输入

如果您喜欢打字或需要发送特定短语而不说话，您可以使用手动翻译框。

1. 您**必须**首先点击 **Start Outgoing (开始发送)** 以建立 VRChat 连接。
2. 在左侧面板底部的 **Manual Translate (Type and Send) (手动翻译(打字并发送))** 文本框中输入您的消息。
3. 按键盘上的 **Enter** 键或点击 **Send (发送)** 按钮。
4. 您输入的文本及其翻译将被发送到聊天框。

<img 
  src={require('./img/manual-text.jpg').default} 
  width="900" 
  alt="Manual Text" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 预期结果

一旦 AI 处理了您的输入，结果将通过 OSC 发送到 VRChat。它将作为聊天气泡出现在您虚拟形象的头顶上，通常会显示您的原始文本，然后是翻译后的文本。

<img 
  src={require('./img/chatbox.jpg').default} 
  width="600" 
  alt="Chatbox" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>
