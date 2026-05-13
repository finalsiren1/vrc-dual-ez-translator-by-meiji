---
title: 一般設定
sidebar_label: 一般設定
sidebar_position: 1
---

# 一般設定

**General Settings（一般設定）**セクションでは、SyncVRCアプリケーションの視覚的な外観、言語、およびバックグラウンドの動作をカスタマイズできます。

## UI言語

この設定は、アプリケーションインターフェース全体の言語を変更します。

* **サポートされている言語:** 英語、日本語 (Japanese)、中国語 (Chinese)、および韓国語 (Korean)。
* **仕組み:** ドロップダウンメニューからお好みの言語を選択するだけです。インターフェースは再起動を必要とせずに即座に更新され、設定は今後のセッションのために自動的に保存されます。

<img 
  src={require('./img/settings-lang.jpg').default} 
  width="900" 
  alt="Settings Lang" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 外観 (ダークモード)

視覚的な好みに合わせて目の疲れを軽減するために、いつでもダークモードとライトモードを切り替えることができます。

<img 
  src={require('./img/settings-theme.jpg').default} 
  width="900" 
  alt="Settings Theme" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## テレメトリ (クラッシュレポート)

このオプションは、アプリケーションでエラーが発生した場合に匿名でクラッシュレポートを自動的に送信することで、SyncVRCの改善に役立ちます。

* **収集されるもの:** 技術的なエラーログとスタックトレース（クラッシュの原因となった特定のコード行）のみが安全なSentryサーバーに送信されます。
* **収集されないもの:** **音声データ、翻訳されたテキスト、APIキー、または個人を特定できる情報は絶対に収集されません。** プライバシーは完全に保証されます。
* **推奨:** バグを迅速に特定して修正するために、これを有効にしておくことを強くお勧めしますが、ボックスのチェックを外すことでいつでも完全にオプトアウトすることができます。

<img 
  src={require('./img/settings-telemetry.jpg').default} 
  width="900" 
  alt="Settings Telemetry" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>
