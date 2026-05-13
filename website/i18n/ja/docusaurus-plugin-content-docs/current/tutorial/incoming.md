---
title: 受信システム (他人の音声を翻訳)
sidebar_label: 受信システム (他人の音声を翻訳)
sidebar_position: 5
---

# 受信システム (他人の音声を翻訳)

**受信（Incoming）システム**は、ゲームから来るオーディオ（他のプレイヤーの声）をリッスンし、あなたの母国語に翻訳します。送信システムとは異なり、これらの翻訳はSyncVRCアプリのインターフェース上にプライベートに表示され、VRChatのチャットボックスには**送信されません**。

## 前提条件: オーディオルーティング（重要なステップ）

他のプレイヤーの声を翻訳するには、アプリがゲームのオーディオを「聞く」必要があります。**物理的な「スピーカー」や「ヘッドフォン」を直接選択することはできません。**

1. **Audio Setup（オーディオ設定）**タブに移動します。
2. **Select Speaker Loopback (Virtual Audio)（スピーカーループバック（仮想オーディオ）の選択）**ドロップダウンから、ループバックデバイスを選択する必要があります。
3. *推奨される仮想オーディオデバイス:* Windows Stereo Mix、VB-Cable、Voicemeeter、またはElgato Wave Link。

<img 
  src={require('./img/incoming-audio.jpg').default} 
  width="900" 
  alt="Incoming Audio" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 受信システムの使用方法

オーディオが正しくルーティングされたら、次の手順に従って翻訳を開始します:

### 1. 言語設定
**Translation（翻訳）**タブの右パネルで、言語を設定します:
* **Listen Language（認識言語）:** 他のプレイヤーが話している言語（例：日本語）に設定します。
* **Translate to（翻訳先）:** あなたの母国語（例：英語）に設定します。

### 2. エンジンの開始
**Start Incoming（受信開始）**ボタンをクリックします（または割り当てられたホットキー、デフォルト：`F3`を押します）。ボタンが赤色になり、デスクトップオーディオをアクティブにリッスンしていることを示します。

<img 
  src={require('./img/incoming-start.jpg').default} 
  width="900" 
  alt="Incoming Start" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

### 3. 翻訳を読む
相手が話すと、AIがリアルタイムで音声を処理します。元のテキストと翻訳されたテキストは、アプリの右下にある**Incoming Log（受信ログ）**テキストボックスに表示されます。

<img 
  src={require('./img/incoming-result.jpg').default} 
  width="900" 
  alt="Incoming Result" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

**💡 プロのヒント:** **送信（Outgoing）**システムと**受信（Incoming）**システムの両方を同時に実行することで、シームレスな双方向の翻訳会話を行うことができます！
