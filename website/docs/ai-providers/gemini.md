---
title: How to get Gemini API Key
sidebar_label: Google Gemini
sidebar_position: 1
---

# Obtaining a Google Gemini API Key

Google Gemini is the recommended translation engine for SyncVRC due to its high speed and contextual accuracy. You can obtain an API key for free through **Google AI Studio**.

Follow these steps to generate and configure your key.

---

## Step 1: Visit Google AI Studio

1. Go to the [Google AI Studio](https://aistudio.google.com/) website.
2. Sign in with your standard Google Account.

> 🖼️ **[IMAGE PLACEHOLDER: AI Studio Login Page]** *(When ready, replace this line with: `![AI Studio Login](/img/gemini-login.png)`)*

---

## Step 2: Create a New API Key

1. On the left-hand sidebar, click on the **"Get API key"** button (the key icon).
2. Click the blue button labeled **"Create API key"**.
3. You may be asked to select a Google Cloud Project. If you don't have one, select **"Create API key in new project"**.
4. Once generated, a pop-up will show your API key. **Copy this key immediately.**

> 🖼️ **[IMAGE PLACEHOLDER: Create API Key Button]** *(When ready, replace this line with: `![Create API Key](/img/gemini-create-key.png)`)*

---

## Step 3: Configure in SyncVRC

1. Open the **SyncVRC** application.
2. Navigate to the **Settings** tab.
3. Under **AI & Translation Engine**, set the **Translation Engine** to `Google Gemini`.
4. Paste your copied key into the **API Key** field and click **Save**.

> 🖼️ **[IMAGE PLACEHOLDER: SyncVRC Settings Setup]** *(When ready, replace this line with: `![SyncVRC Settings](/img/settings-gemini-setup.png)`)*

---

## Important: Free Tier vs. Paid Plan

Google offers a generous **Free Tier** for Gemini, but there are important trade-offs for VRChat users:

### 1. Free Tier (Recommended for Testing)
* **Rate Limits:** Limited requests per minute. If you speak very rapidly, you may encounter "API Limit Exceeded" errors.
* **Data Privacy:** Google may use your input/output data to improve their models.
* **Cost:** Completely free.

### 2. Pay-as-you-go (Recommended for Best Experience)
* **Stability:** Higher rate limits ensure your translations never pause during intense conversations.
* **Privacy:** Your data is **not** used to train Google's models.
* **Cost:** You only pay for what you use (typically just a few cents per hour of active talking).

**How to upgrade:** In Google AI Studio, click on **"Settings"** (gear icon) > **"Plan & Billing"** to attach a credit card and enable pay-as-you-go.

---

## Security Warning ⚠️

**Never share your API Key with anyone.** Your API key is like a password to your wallet. If someone else gets it, they can use your quota or run up charges on your billing account. SyncVRC stores your key locally on your PC and masks it with asterisks in the UI to prevent accidental leaks during streams.