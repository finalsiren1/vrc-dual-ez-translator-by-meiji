---
title: 如何获取 Gemini API 密钥
sidebar_label: Google Gemini
sidebar_position: 1
---

# 获取 Google Gemini API 密钥

由于其高速度和上下文准确性，Google Gemini 是 SyncVRC 的推荐翻译引擎。您可以通过 **Google AI Studio** 免费获取 API 密钥。

请按照以下步骤生成并配置您的密钥。

---

## 步骤 1：访问 Google AI Studio

1. 访问 [Google AI Studio](https://aistudio.google.com/) 网站。
2. 使用您的标准 Google 帐户登录。

> 🖼️ **[IMAGE PLACEHOLDER: AI Studio Login Page]** *(准备就绪后，将此行替换为：`![AI Studio Login](/img/gemini-login.png)`)*

---

## 步骤 2：创建新的 API 密钥

1. 在左侧边栏上，点击 **"Get API key (获取 API 密钥)"** 按钮（钥匙图标）。
2. 点击标有 **"Create API key (创建 API 密钥)"** 的蓝色按钮。
3. 系统可能会要求您选择一个 Google Cloud 项目。如果您没有，请选择 **"Create API key in new project (在新项目中创建 API 密钥)"**。
4. 生成后，弹出窗口将显示您的 API 密钥。**立即复制此密钥。**

> 🖼️ **[IMAGE PLACEHOLDER: Create API Key Button]** *(准备就绪后，将此行替换为：`![Create API Key](/img/gemini-create-key.png)`)*

---

## 步骤 3：在 SyncVRC 中配置

1. 打开 **SyncVRC** 应用程序。
2. 导航到 **Settings (设置)** 选项卡。
3. 在 **AI & Translation Engine (AI 与翻译引擎)** 下，将 **Translation Engine (翻译引擎)** 设置为 `Google Gemini`。
4. 将复制的密钥粘贴到 **API Key** 字段中，然后点击 **Save (保存)**。

> 🖼️ **[IMAGE PLACEHOLDER: SyncVRC Settings Setup]** *(准备就绪后，将此行替换为：`![SyncVRC Settings](/img/settings-gemini-setup.png)`)*

---

## 重要提示：免费层级与付费计划

Google 提供了慷慨的 Gemini **免费层级**，但对 VRChat 用户来说，存在一些重要的权衡：

### 1. 免费层级（推荐用于测试）
* **速率限制:** 限制每分钟的请求数。如果您说话非常快，您可能会遇到 "API Limit Exceeded" 错误。
* **数据隐私:** Google 可能会使用您的输入/输出数据来改进他们的模型。
* **成本:** 完全免费。

### 2. 按量付费（推荐以获得最佳体验）
* **稳定性:** 更高的速率限制可确保您的翻译在激烈的对话期间永远不会暂停。
* **隐私:** 您的数据**不会**用于训练 Google 的模型。
* **成本:** 您只为使用的内容付费（通常每小时积极说话只需几美分）。

**如何升级:** 在 Google AI Studio 中，点击 **"Settings (设置)"**（齿轮图标）> **"Plan & Billing (计划和账单)"** 以绑定信用卡并启用按量付费。

---

## 安全警告 ⚠️

**永远不要与任何人共享您的 API 密钥。** 您的 API 密钥就像您钱包的密码。如果其他人获得了它，他们可以使用您的配额或在您的结算帐户上产生费用。SyncVRC 将您的密钥本地存储在您的 PC 上，并在 UI 中使用星号将其屏蔽，以防止在直播期间意外泄露。
