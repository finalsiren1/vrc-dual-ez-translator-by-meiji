---
title: 如何获取 OpenAI API 密钥
sidebar_label: OpenAI (GPT)
sidebar_position: 3
---

# 获取 OpenAI API 密钥

SyncVRC 支持使用 **OpenAI 的模型**（例如 GPT-4o 或 GPT-3.5）进行翻译。OpenAI 是一个受欢迎的选择，以其高质量的翻译和广泛的语言支持而闻名。

:::warning 免责声明
本教程可能不完整或略微过时，因为开发者日常测试主要不使用 OpenAI API。请参阅官方 OpenAI 文档以获取最准确的信息。
:::

---

## 获取密钥的步骤

1. **创建 OpenAI 帐户:** 访问 [OpenAI Platform](https://platform.openai.com/) 并注册或登录。
2. **访问 API 密钥:** 导航到左侧边栏中的 **"API Keys"** 部分（在 "Dashboard" 或 "Settings" 菜单下）。
3. **创建私钥:** 点击 **"+ Create new secret key"** 按钮。
4. **命名并复制:** 给您的密钥起个名字（例如，“SyncVRC”），然后点击 **Create**。**立即复制该密钥**，因为关闭窗口后您将无法再次看到它。
5. **在 SyncVRC 中配置:** 打开 SyncVRC 中的 **Settings (设置)** 选项卡，选择 `OpenAI` 作为您的引擎，并粘贴密钥。

---

## 重要提示：使用额度

* **预付费系统:** OpenAI 通常需要您提前购买“积分”，然后 API 才能运行。即使是新帐户，您可能也需要至少充值 5 美元余额才能开始使用翻译服务。
* **层级:** 随着时间的推移您在平台上花费的增加，您的“使用层级”（这决定了您的速率限制）将会增加。
