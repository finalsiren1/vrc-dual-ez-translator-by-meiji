---
title: 常规设置
sidebar_label: 常规设置
sidebar_position: 1
---

# 常规设置

**General Settings (常规设置)** 部分允许您自定义 SyncVRC 应用程序的视觉外观、语言和后台行为。

## UI 语言

此设置更改整个应用程序界面的语言。

* **支持的语言:** 英语、日语 (日本語)、中文 (Chinese) 和韩语 (한국어)。
* **工作原理:** 只需从下拉菜单中选择您偏好的语言。界面将立即更新，无需重启，并且您的偏好将自动保存以供将来的会话使用。

<img 
  src={require('./img/settings-lang.jpg').default} 
  width="900" 
  alt="Settings Lang" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 外观 (深色模式)

您可以随时在深色模式和浅色模式之间切换，以适应您的视觉偏好并减少眼睛疲劳。

<img 
  src={require('./img/settings-theme.jpg').default} 
  width="900" 
  alt="Settings Theme" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 遥测 (崩溃报告)

如果应用程序遇到错误，此选项通过自动发送匿名的崩溃报告来帮助我们改进 SyncVRC。

* **收集什么:** 只有技术错误日志和堆栈跟踪（导致崩溃的特定代码行）会发送到我们安全的 Sentry 服务器。
* **不收集什么:** **绝对不会收集任何语音数据、翻译文本、API 密钥或个人身份信息。** 您的隐私得到充分保障。
* **建议:** 我们强烈建议您启用此功能以帮助我们快速识别和修复错误，但您完全可以随时通过取消选中该框来选择退出。

<img 
  src={require('./img/settings-telemetry.jpg').default} 
  width="900" 
  alt="Settings Telemetry" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>
