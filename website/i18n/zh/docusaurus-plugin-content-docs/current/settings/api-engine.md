---
title: AI 与翻译引擎
sidebar_label: AI 与引擎
sidebar_position: 2
---

# AI 与翻译引擎配置

**AI & Translation Engine (AI 与翻译引擎)** 部分是 SyncVRC 的核心。您可以在此处配置翻译文本的云服务以及处理您声音的本地硬件。

此处设置不正确可能导致 API 错误或性能下降，因此请仔细遵循本指南。

## 翻译引擎

选择将处理文本翻译的云 AI 提供商。

* **支持的引擎:** Google Gemini、DeepL API 和 OpenAI。
* **建议:** 强烈推荐 **Google Gemini**，并且目前针对 SyncVRC 进行了全面优化，提供令人难以置信的快速实时响应和出色的对话上下文。

> 🖼️ **[IMAGE PLACEHOLDER: Translation Engine Selection]** *(准备就绪后，将此行替换为：`![Translation Engine](/img/settings-engine.png)`)*

---

## API 密钥管理

要使用云翻译服务，您必须提供您选择的提供商的 API 密钥。

* **如何设置:**
  1. 从下拉菜单中选择您首选的引擎。
  2. 将您的秘密 API 密钥粘贴到 **API Key** 输入字段中。
  3. 点击 **Save (保存)**。
* **隐私与主播模式:** 保存后，文本字段将被锁定，您的密钥将被隐藏为星号 (`********`)。这可以防止您在直播或屏幕共享时意外泄露您的 API 密钥。
* **如何编辑:** 点击 **Edit (编辑)** 按钮解锁该字段，输入您的新密钥，然后再次点击保存。

> 🖼️ **[IMAGE PLACEHOLDER: API Key Input and Save]** *(准备就绪后，将此行替换为：`![API Key Setup](/img/settings-apikey.png)`)*

---

## AI 处理设备 (语音转文本)

此设置决定了您计算机上的哪个硬件组件运行离线 **Faster-Whisper** 语音识别模型。

* **GPU (NVIDIA) - 强烈推荐:** 利用您的显卡实现极速、近乎即时的语音识别。
  * *要求:* 您**必须**拥有 NVIDIA 显卡并安装了 [NVIDIA CUDA Toolkit 12.x](./../tutorial/initial-setup)。
* **CPU (回退):** 利用您计算机的主处理器。
  * *何时使用:* 如果您拥有 AMD 或 Intel GPU，或者如果在启动时遇到 CUDA 错误，请选择此项。请注意，CPU 处理明显慢于 GPU 处理。

> 🖼️ **[IMAGE PLACEHOLDER: AI Processing Device Selection]** *(准备就绪后，将此行替换为：`![AI Device](/img/settings-device.png)`)*

---

## 固定的模型信息

**ℹ️ 关于准确性的注意事项:** 为了在翻译速度和转录准确性之间取得最佳平衡，SyncVRC 硬编码为在本地使用 **Whisper 'Medium'** 模型。这确保 AI 在将文本发送到云端之前准确理解您的发音，并且无法手动更改。
