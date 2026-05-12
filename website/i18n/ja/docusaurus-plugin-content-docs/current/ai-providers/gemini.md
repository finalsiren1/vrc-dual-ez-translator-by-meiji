---
title: Gemini APIキーの取得方法
sidebar_label: Google Gemini
sidebar_position: 1
---

# Google Gemini APIキーの取得

Google Geminiは、その高速性と文脈上の正確さから、SyncVRCの推奨翻訳エンジンです。**Google AI Studio**を通じて無料でAPIキーを取得できます。

以下の手順に従って、キーを生成して設定してください。

---

## ステップ 1: Google AI Studioにアクセスする

1. [Google AI Studio](https://aistudio.google.com/)ウェブサイトにアクセスします。
2. 標準のGoogleアカウントでサインインします。

> 🖼️ **[IMAGE PLACEHOLDER: AI Studio Login Page]** *(準備ができたら、この行を次のように置き換えます: `![AI Studio Login](/img/gemini-login.png)`)*

---

## ステップ 2: 新しいAPIキーの作成

1. 左側のサイドバーで、**"Get API key（APIキーを取得）"**ボタン（鍵のアイコン）をクリックします。
2. **"Create API key（APIキーを作成）"**という青いボタンをクリックします。
3. Google Cloudプロジェクトを選択するように求められる場合があります。お持ちでない場合は、**"Create API key in new project（新しいプロジェクトでAPIキーを作成）"**を選択します。
4. 生成されると、ポップアップにAPIキーが表示されます。**このキーをすぐにコピーしてください。**

> 🖼️ **[IMAGE PLACEHOLDER: Create API Key Button]** *(準備ができたら、この行を次のように置き換えます: `![Create API Key](/img/gemini-create-key.png)`)*

---

## ステップ 3: SyncVRCでの設定

1. **SyncVRC**アプリケーションを開きます。
2. **Settings（設定）**タブに移動します。
3. **AI & Translation Engine**で、**Translation Engine**を`Google Gemini`に設定します。
4. コピーしたキーを**API Key**フィールドに貼り付け、**Save（保存）**をクリックします。

> 🖼️ **[IMAGE PLACEHOLDER: SyncVRC Settings Setup]** *(準備ができたら、この行を次のように置き換えます: `![SyncVRC Settings](/img/settings-gemini-setup.png)`)*

---

## 重要: 無料枠と有料プラン

GoogleはGeminiの寛大な**無料枠**を提供していますが、VRChatユーザーには重要なトレードオフがあります。

### 1. 無料枠（テスト用として推奨）
* **レート制限:** 1分あたりのリクエスト数が制限されています。非常に速く話す場合、「API Limit Exceeded」エラーが発生する可能性があります。
* **データプライバシー:** Googleはモデルを改善するために入出力データを使用する場合があります。
* **費用:** 完全に無料です。

### 2. 従量課金制（最高のエクスペリエンスとして推奨）
* **安定性:** より高いレート制限により、激しい会話中に翻訳が一時停止することはありません。
* **プライバシー:** あなたのデータはGoogleのモデルのトレーニングには**使用されません**。
* **費用:** 使用した分だけ支払います（通常、アクティブに話している1時間あたりわずか数セントです）。

**アップグレード方法:** Google AI Studioで、**"設定"**（歯車のアイコン） > **"プランとお支払い"**をクリックしてクレジットカードを登録し、従量課金制を有効にします。

---

## セキュリティの警告 ⚠️

**APIキーは絶対に誰とも共有しないでください。**APIキーは財布のパスワードのようなものです。他人が取得した場合、彼らはあなたのクォータを使用したり、請求アカウントに料金を発生させたりする可能性があります。SyncVRCはPCのローカルにキーを保存し、配信中の偶発的な漏洩を防ぐためにUIではアスタリスクでマスクします。
