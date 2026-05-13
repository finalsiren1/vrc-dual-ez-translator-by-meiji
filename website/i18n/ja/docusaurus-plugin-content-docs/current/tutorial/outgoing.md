---
title: 送信システム (音声 -> VRChat)
sidebar_label: 送信システム (音声 -> VRChat)
sidebar_position: 4
---

# 送信システム (音声 -> VRChat)

**送信（Outgoing）システム**は、あなたの声やテキストを翻訳し、VRChatのチャットボックスに直接送信します。これにより、他のプレイヤーはあなたが言っていることをリアルタイムで彼らの母国語で読むことができます。

## 前提条件

開始する前に、**Translation（翻訳）**タブにいることと、以下の設定が完了していることを確認してください:
1. **Select Microphone（マイクの選択）:** *Audio Setup（オーディオ設定）*タブから物理的なマイクを選択します。
2. **Language Setup（言語設定）:** あなたの母国語（**From（翻訳元）**）とターゲット言語（**Translate to（翻訳先）**）を設定します。

---

## 方法1: 自動音声翻訳（連続）

ハンズフリーで自然な会話に最適です。AIは、あなたがいつ話し、いつ休止したかを自動的に検出します。

1. **Auto (Continuous)（自動（連続））**モードを選択します。
2. **Start Outgoing（送信開始）**ボタンをクリックします（または割り当てられたホットキー、デフォルト：`F2`を押します）。
3. ボタンが赤色になり、システムがアクティブであることを示します。マイクに向かって話すだけです。
4. AIがあなたの音声を処理し、翻訳をVRChatに自動的に送信します。

<img 
  src={require('./img/auto-voice.jpg').default} 
  width="900" 
  alt="Auto Voice" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 方法2: プッシュ・トゥ・トーク（押している間話す）

騒がしい環境や、特定の文だけを翻訳したい場合に最適です。

1. **Push to Record（プッシュして録音）**モードを選択します。
2. **Start Outgoing（送信開始）**をクリックしてAIエンジンを初期化します。
3. **Hold to Speak（押して話す）**ボタンがアクティブになります。
4. 話している間、**Hold to Speak**ボタンをクリックして押し続けます（または割り当てられたプッシュ・トゥ・トークのホットキーを押し続けます）。
5. 終わったらボタンを離します。翻訳が処理され、すぐに送信されます。

<img 
  src={require('./img/push-to-talk.jpg').default} 
  width="900" 
  alt="Push to Talk" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 方法3: 手動テキスト入力

入力したい場合、または話さずに特定のフレーズを送信したい場合は、手動翻訳（Manual Translate）ボックスを使用できます。

1. VRChat接続を確立するには、最初に**Start Outgoing（送信開始）**をクリック**しなければなりません**。
2. 左パネルの下部にある**Manual Translate (Type and Send)（手動翻訳（入力して送信））**テキストボックスにメッセージを入力します。
3. キーボードの**Enter**を押すか、**Send（送信）**ボタンをクリックします。
4. 入力したテキストとその翻訳がチャットボックスに送信されます。

<img 
  src={require('./img/manual-text.jpg').default} 
  width="900" 
  alt="Manual Text" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 期待される結果

AIがあなたの入力を処理すると、結果はOSC経由でVRChatに送信されます。アバターの頭上にチャットバブルとして表示され、通常は元のテキストの後に翻訳されたテキストが表示されます。

<img 
  src={require('./img/chatbox.jpg').default} 
  width="600" 
  alt="Chatbox" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>
