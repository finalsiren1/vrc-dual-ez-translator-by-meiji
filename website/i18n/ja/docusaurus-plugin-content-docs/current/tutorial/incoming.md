---
title: メッセージの受信 (Incoming)
sidebar_label: 受信翻訳
sidebar_position: 5
---

# 他人の声を翻訳する (Incoming)

**受信（Incoming）システム**は、ゲームから来るオーディオ（他のプレイヤーの声）をリッスンし、あなたの母国語に翻訳します。送信システムとは異なり、これらの翻訳はSyncVRCアプリのインターフェース上にプライベートに表示され、VRChatのチャットボックスには**送信されません**。

## 前提条件: オーディオルーティング（重要なステップ）

他のプレイヤーの声を翻訳するには、アプリがゲームのオーディオを「聞く」必要があります。**物理的な「スピーカー」や「ヘッドフォン」を直接選択することはできません。**

1. **Audio Setup（オーディオ設定）**タブに移動します。
2. **Select Speaker Loopback (Virtual Audio)（スピーカーループバック（仮想オーディオ）の選択）**ドロップダウンから、ループバックデバイスを選択する必要があります。
3. *推奨される仮想オーディオデバイス:* Windows Stereo Mix、VB-Cable、Voicemeeter、またはElgato Wave Link。

> 🖼️ **[IMAGE PLACEHOLDER: Audio Routing Setup]** *(準備ができたら、この行を次のように置き換えます: `![Audio Routing Setup](/img/incoming-audio.png)`)*

---

## 受信システムの使用方法

オーディオが正しくルーティングされたら、次の手順に従って翻訳を開始します:

### 1. 言語設定
**Translation（翻訳）**タブの右パネルで、言語を設定します:
* **Listen Language（認識言語）:** 他のプレイヤーが話している言語（例：日本語）に設定します。
* **Translate to（翻訳先）:** あなたの母国語（例：英語）に設定します。

### 2. エンジンの開始
**Start Incoming（受信開始）**ボタンをクリックします（または割り当てられたホットキー、デフォルト：`F3`を押します）。ボタンが赤色になり、デスクトップオーディオをアクティブにリッスンしていることを示します。

> 🖼️ **[IMAGE PLACEHOLDER: Incoming Setup and Start]** *(準備ができたら、この行を次のように置き換えます: `![Start Incoming](/img/incoming-start.png)`)*

### 3. 翻訳を読む
相手が話すと、AIがリアルタイムで音声を処理します。元のテキストと翻訳されたテキストは、アプリの右下にある**Incoming Log（受信ログ）**テキストボックスに表示されます。

> 🖼️ **[IMAGE PLACEHOLDER: Incoming Log Result]** *(準備ができたら、この行を次のように置き換えます: `![Incoming Result](/img/incoming-result.png)`)*

---

**💡 プロのヒント:** **送信（Outgoing）**システムと**受信（Incoming）**システムの両方を同時に実行することで、シームレスな双方向の翻訳会話を行うことができます！
