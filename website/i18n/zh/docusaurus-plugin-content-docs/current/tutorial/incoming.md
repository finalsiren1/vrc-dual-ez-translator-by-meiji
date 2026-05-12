---
title: 接收消息 (Incoming)
sidebar_label: 接收翻译
sidebar_position: 5
---

# 翻译他人的声音 (Incoming)

**接收 (Incoming) 系统**会监听来自您游戏的音频（其他玩家的声音），并将其翻译成您的母语。与发送系统不同，这些翻译会私密地显示在您的 SyncVRC 应用界面上，而**不会**发送到 VRChat 聊天框。

## 先决条件：音频路由（关键步骤）

为了翻译其他玩家的声音，应用程序需要“听到”您的游戏音频。**您不能直接选择您的物理“扬声器”或“耳机”。**

1. 转到 **Audio Setup (音频设置)** 选项卡。
2. 在 **Select Speaker Loopback (Virtual Audio) (选择扬声器回环(虚拟音频))** 下拉菜单下，您必须选择一个回环设备。
3. *推荐的虚拟音频设备：* Windows 立体声混音 (Stereo Mix)、VB-Cable、Voicemeeter 或 Elgato Wave Link。

> 🖼️ **[IMAGE PLACEHOLDER: Audio Routing Setup]** *(准备就绪后，将此行替换为：`![Audio Routing Setup](/img/incoming-audio.png)`)*

---

## 如何使用接收系统

正确路由音频后，请按照以下步骤开始翻译：

### 1. 语言设置
在 **Translation (翻译)** 选项卡的右侧面板上，配置您的语言：
* **Listen Language (识别语言):** 将其设置为其他玩家正在说的语言（例如，日语）。
* **Translate to (翻译为):** 将其设置为您的母语（例如，英语）。

### 2. 启动引擎
点击 **Start Incoming (开始接收)** 按钮（或按下您分配的热键，默认：`F3`）。该按钮将变为红色，表示它正在主动监听您的桌面音频。

> 🖼️ **[IMAGE PLACEHOLDER: Incoming Setup and Start]** *(准备就绪后，将此行替换为：`![Start Incoming](/img/incoming-start.png)`)*

### 3. 阅读翻译
当对方说话时，AI 将实时处理音频。原始文本和翻译后的文本将出现在应用程序右下角的 **Incoming Log (接收日志)** 文本框中。

> 🖼️ **[IMAGE PLACEHOLDER: Incoming Log Result]** *(准备就绪后，将此行替换为：`![Incoming Result](/img/incoming-result.png)`)*

---

**💡 专家提示：** 您可以同时运行**发送 (Outgoing)**和**接收 (Incoming)**系统，以进行无缝的双向翻译对话！
