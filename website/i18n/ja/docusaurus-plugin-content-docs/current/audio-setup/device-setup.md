---
title: オーディオ設定
sidebar_label: オーディオ設定
sidebar_position: 1
---

# オーディオ設定

**Audio Setup（オーディオ設定）**タブは、SyncVRCのオーディオル​​ーティングの核となります。ここの設定が正しくないと、AIがあなたの声や他のプレイヤーの声を拾えなくなる最も一般的な原因になります。

ハードウェアおよびソフトウェアのオーディオを正しく設定するには、以下の詳細な内訳に従ってください。

## 1. マイクの選択 (Outgoing)

この設定は、AIが**送信（Outgoing）**翻訳システム（あなたの声）のために何をリッスンするかを制御します。

* **選択するもの:** メインの物理的なマイク（VRヘッドセットのマイク、USBコンデンサーマイク、またはXLRインターフェース入力など）を選択します。
* **重要:** Windowsでマイクがミュートされていないことを確認してください。そうしないと、AIは無音しかリッスンできません。

<img 
  src={require('./img/audio-mic.jpg').default} 
  width="900" 
  alt="Audio Mic" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 2. スピーカーループバックの選択 (Incoming)

この設定は、AIが**受信（Incoming）**翻訳システム（他のプレイヤーの声）のために何をリッスンするかを制御します。

* **問題点:** 音声認識エンジンは、物理的なスピーカーまたはヘッドフォンから「出ている」オーディオを直接キャプチャすることはできません。
* **解決策（仮想オーディオ）:** ヘッドフォンに到達する前にデスクトップオーディオを傍受する「ループバック」または「仮想オーディオ」デバイスを選択する必要があります。
* **サポートされているオプション:**
  * **Windows Stereo Mix**（ほとんどのWindows PCに組み込まれていますが、Windowsのサウンド設定で有効にする必要がある場合があります）。
  * **VB-Cable**（無料の仮想オーディオケーブル）。
  * **Voicemeeter**（高度なオーディオミキシングソフトウェア）。
  * **Elgato Wave Link** または **SteelSeries Sonar**（それぞれのハードウェアを使用している場合）。

<img 
  src={require('./img/audio-speaker.jpg').default} 
  width="900" 
  alt="Audio Speaker" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 3. VRCミュート同期を有効にする

VRChat専用に構築された重要なプライバシーおよび最適化機能です。

* **仕組み:** 有効にすると、SyncVRCはVRChatのOSCパラメーターを読み取ります。VRコントローラーまたはVRChatのラジアルメニューを使用してマイクをミュートすると、SyncVRCは即座に送信（Outgoing）翻訳を一時停止します。
* **使用する理由:** ミュート中にAIが継続的にリッスンし、バックグラウンドノイズをAPIプロバイダーに送信するのを防ぎ、APIクォータを節約し、完全なプライバシーを確​​保します。

<img 
  src={require('./img/audio-mutesync.jpg').default} 
  width="900" 
  alt="Audio Mute Sync" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

AIによる音声処理方法を微調整するには、[**高度なオーディオ設定（Advanced Audio Settings）**](./advanced-audio)ページに進んでください。
