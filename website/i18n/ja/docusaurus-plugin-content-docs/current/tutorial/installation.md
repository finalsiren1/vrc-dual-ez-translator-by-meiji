---
title: インストール
sidebar_label: インストール
sidebar_position: 2
---

# SyncVRC のインストール方法

SyncVRC のインストールは簡単です。以下の手順に従って、PCでアプリケーションを実行してください。

## ステップバイステップのインストール

**ステップ 1: インストーラのダウンロード**
まず、[公式の GitHub Releases ページ](https://github.com/finalsiren1/SyncVRC/releases)から最新の `SyncVRC_Setup_vX.X.X.exe` ファイルをダウンロードします。

**ステップ 2: セットアップ言語の選択**
ダウンロードした `.exe` ファイルを実行します。インストール中に使用する言語の選択を求められます。希望の言語（例：English）を選択し、**OK** をクリックします。

<img 
  src={require('./img/setup-lang.jpg').default} 
  width="300" 
  alt="Setup Lang" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**ステップ 3: インストール先の選択**
セットアップで SyncVRC のインストール先を尋ねられます。デフォルトのパスは通常 `C:\Program Files\SyncVRC` です。このままにするか、**Browse (参照)** をクリックして別のフォルダを選択できます。**Next (次へ)** をクリックして続行します。

<img 
  src={require('./img/setup-dest.png').default} 
  width="600" 
  alt="Setup Dest" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**ステップ 4: 追加タスクの選択**
デスクトップから SyncVRC に簡単にアクセスしたい場合は、**"Create a desktop shortcut" (デスクトップショートカットを作成する)** のチェックボックスをオンにします。**Next (次へ)** をクリックします。

<img 
  src={require('./img/setup-tasks.png').default} 
  width="600" 
  alt="Setup Task" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**ステップ 5: 確認してインストール**
「Ready to Install (インストールの準備完了)」画面でインストール設定を確認します。すべて正しければ、**Install (インストール)** をクリックします。展開とインストールのプロセスが完了するまで待ちます。

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/setup-install1.png').default} width="45%" alt="Install Step 1" />
  <img src={require('./img/setup-install2.png').default} width="45%" alt="Install Step 2" />
</div>

**ステップ 6: セットアップの完了**
インストールが完了したら、**"Launch SyncVRC" (SyncVRC を起動する)** がチェックされていることを確認し、**Finish (完了)** をクリックします。これでアプリが開きます。

<img 
  src={require('./img/setup-finish.png').default} 
  width="600" 
  alt="Finish Setup" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

<img 
  src={require('./img/app-launch.jpg').default} 
  width="900" 
  alt="App Launch" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## ⚠️ 重要: Windows Defender SmartScreen

インストーラ (`Setup.exe`) またはアプリを初めて実行しようとしたときに、**"Windows によって PC が保護されました"** という青い警告画面が表示されることがあります。

**パニックにならないでください。SyncVRC は 100% ウイルスフリーであり、安全に使用できます。**

### なぜこれが起こるのですか？
この警告が表示される理由は、SyncVRC が個人のクリエイターによって開発されており、アプリケーションファイルがまだ非常に高価な「デジタル署名」を持っていないか、Windows が自動的に認識するほどのグローバルなダウンロード履歴が十分ではないためです。

さらに、新しいアップデートをリリースするたびにファイルのコードが変更されます。この画面が表示された場合、それは単にこの特定のバージョンが **Microsoft Security Intelligence チームのホワイトリスト承認をまだ待っている** ことを意味します。

### 警告をバイパスする方法:
1. 青い SmartScreen ウィンドウで、**"詳細情報" (More info)** のテキストリンクをクリックします。
2. 発行元が「不明な発行元」として表示されます。右下に新しいボタンが表示されます。
3. **"実行" (Run anyway)** ボタンをクリックして、インストールを続行するか、アプリを起動します。

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/smartscreen-warning1.png').default} width="45%" alt="Smartscreen 1" />
  <img src={require('./img/smartscreen-warning2.png').default} width="45%" alt="Smartscreen 2" />
</div>

「実行」をクリックすることで、公式リポジトリから直接ダウンロードされたファイルを信頼していることを Windows に伝えることになります。
