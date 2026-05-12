---
title: 如何获取 DeepL API 密钥
sidebar_label: DeepL API
sidebar_position: 2
---

# 获取 DeepL API 密钥

SyncVRC 支持通过 **DeepL API** 进行翻译。这项服务以其听起来自然的翻译而闻名，特别是对于欧洲和亚洲语言。

:::warning 免责声明
本教程可能不完整或略微过时，因为开发者日常测试主要不使用 DeepL API。如果您遇到任何不一致之处，请参阅官方 DeepL 文档。
:::

---

## 获取密钥的步骤

1. **创建 DeepL 帐户:** 访问 [DeepL Pro](https://www.deepl.com/pro-api) 网站。
2. **选择 API 计划:** 选择 **"DeepL API Free"**（每月最多 500,000 个字符）或 **"DeepL API Pro"** 计划。
    * *注意：即使是免费计划，DeepL 通常也需要有效的信用卡进行身份验证。*
3. **访问帐户控制台:** 登录后，导航到 **"帐户"** 选项卡。
4. **找到您的身份验证密钥:** 向下滚动到帐户页面的底部，找到您的 **"DeepL API 身份验证密钥"**。
5. **复制并粘贴:** 复制密钥并将其粘贴到 SyncVRC 中的 **Settings (设置)** 选项卡下的 DeepL API 部分。

---

## DeepL API Free vs. Pro

* **DeepL API Free:** 免费提供宽松的每月字符数限制，但在大多数地区需要信用卡验证。
* **DeepL API Pro:** 取消了字符数限制（按量付费），并提供最大的数据安全性，确保您的文本永远不会被存储或用于训练他们的模型。
