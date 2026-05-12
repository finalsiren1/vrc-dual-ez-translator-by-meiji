---
title: 故障排除指南
sidebar_label: 故障排除
sidebar_position: 8
---

# 故障排除与常见问题

如果您在使用 SyncVRC 时遇到问题，请在报告错误之前查看本指南，了解最常见的问题及其解决方案。

## 1. AI 处理与硬件错误

**错误:** `CUDA/GPU Error: No compatible NVIDIA GPU found.` 或启动麦克风时应用崩溃。
* **原因:** 应用程序正在尝试使用您的 GPU 来处理 Faster-Whisper 模型，但找不到必需的 NVIDIA 驱动程序。
* **解决方案:**
  * 如果您拥有 **NVIDIA GPU**，您必须安装 [NVIDIA CUDA Toolkit 12.x](./tutorial/initial-setup)。安装后重启您的电脑。
  * 如果您拥有的是 **AMD、Intel，或没有独立显卡**，请转到 **Settings (设置)** 选项卡，并将 **AI Processing Device (AI 处理设备)** 更改为 `CPU (Fallback)`。

## 2. API 与翻译错误

**错误:** `API Limit Exceeded: Too many requests.`
* **原因:** 您正在使用免费层级的 API 密钥（尤其是 Google Gemini），并且说得太多、太快，达到了速率限制。
* **解决方案:** 停止说话一分钟，让限制重置。为了彻底解决问题，请将您的 API 账户升级为按量付费的计费计划。或者，将您的 SyncVRC 模式从 *Auto (Continuous)* 切换为 *Push to Record*。

**错误:** `API Error: Invalid API Key.`
* **原因:** 您的 API 密钥为空、复制错误，或者您的云服务提供商账户受到限制。
* **解决方案:** 在 **Settings (设置)** 选项卡中仔细检查您的 API 密钥。确保密钥的开头或结尾没有多余的空格。

**错误:** `API Request Error: 400 Bad Request`（或类似的 400 错误）
* **原因:** 这通常发生在提供商更改了 AI 模型名称，或者发送的文本违反了云服务提供商的安全指南（例如极端的脏话）时。
* **解决方案:** SyncVRC 默认禁用了安全过滤器，但提供商仍可能硬性拦截某些词语。尝试说另一句话。

## 3. VRChat OSC 连接问题

**问题:** OSC 状态显示 `🔴 Not Detected` 或翻译未出现在 VRChat 中。
* **原因:** VRChat 未在默认端口（`9000`）上发送或接收 OSC 数据。
* **解决方案:**
  1. 打开您的 VRChat 轮盘菜单 (Radial Menu)。
  2. 转到 **Options > OSC** 并将其切换为 **Off**，然后再切换回 **On** 以重置连接。
  3. 确保没有其他 OSC 应用程序（如面部追踪器或心率监测器）阻塞了端口 `9000` 或 `9001`。

## 4. 音频路由与麦克风问题

**问题:** 接收系统正在转录我自己说话的声音，或转录 YouTube 视频的声音。
* **原因:** 您在 *Speaker Loopback (扬声器回环)* 设置中选择了您的物理扬声器或耳机。
* **解决方案:** 您必须使用虚拟音频线（例如 VB-Cable）或 Windows 立体声混音 (Stereo Mix)。请确保**仅**将 VRChat 的音频路由到此虚拟音频线，并在 SyncVRC 的接收设置中选择该虚拟音频线。

**问题:** 应用程序显示“Listening...”但从不翻译我的声音。
* **原因:** AI 听不到您的声音，或者您的麦克风音量太小。
* **解决方案:**
  * 确保您的麦克风没有被硬件静音。
  * 检查 Windows 声音设置，确保您的麦克风是默认输入设备，并且输入音量足够高。
  * 调整高级音频设置 (Advanced Audio Settings) 中的 **Silence Timeout (静音超时)**；如果设置得太高，AI 可能会等待太长时间才进行处理。

## 5. 静音同步 (Mute Sync) 不起作用
**问题:** 我在 VRChat 中静音了麦克风，但 SyncVRC 仍在翻译。
* **原因:** OSC 未启用，或者您没有勾选 Mute Sync 框。
* **解决方案:** 转到 **Audio Setup (音频设置)** 并确保已勾选 **Enable VRC Mute Sync (启用 VRC 静音同步)**。另外，验证左下角的 OSC 状态是否为绿色（`🟢 Detected`）。

---

## 仍需要帮助？

如果此处未列出您的问题，请确保您在设置 (Settings) 选项卡中启用了 **Telemetry (Crash Reports) (遥测(崩溃报告))**。这允许应用程序将错误日志安全地发送给开发者。

您也可以在我们的 [GitHub Issues 页面](https://github.com/finalsiren1/SyncVRC/issues)寻求支持或报告错误。
