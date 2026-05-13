---
title: 安装
sidebar_label: 安装
sidebar_position: 2
---

# 如何安装 SyncVRC

安装 SyncVRC 非常简单。请按照以下步骤在您的电脑上运行该应用程序。

## 分步安装

**步骤 1: 下载安装程序**
首先，从我们的 [官方 GitHub Releases 页面](https://github.com/finalsiren1/SyncVRC/releases) 下载最新的 `SyncVRC_Setup_vX.X.X.exe` 文件。

**步骤 2: 选择安装语言**
运行下载的 `.exe` 文件。在安装过程中系统会提示您选择要使用的语言。选择您偏好的语言（例如：English），然后点击 **OK**。

<img 
  src={require('./img/setup-lang.jpg').default} 
  width="300" 
  alt="Setup Lang" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**步骤 3: 选择目标位置**
安装程序会询问您想将 SyncVRC 安装在哪里。默认路径通常是 `C:\Program Files\SyncVRC`。您可以保留默认设置，或者点击 **Browse (浏览)** 选择一个不同的文件夹。点击 **Next (下一步)** 继续。

<img 
  src={require('./img/setup-dest.png').default} 
  width="600" 
  alt="Setup Dest" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**步骤 4: 选择附加任务**
如果您想从桌面方便地访问 SyncVRC，请勾选 **"Create a desktop shortcut" (创建桌面快捷方式)** 选项。点击 **Next (下一步)**。

<img 
  src={require('./img/setup-tasks.png').default} 
  width="600" 
  alt="Setup Task" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**步骤 5: 查看并安装**
在“准备安装”屏幕上检查您的安装设置。如果一切看起来无误，请点击 **Install (安装)**。等待解压和安装过程完成。

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/setup-install1.png').default} width="45%" alt="Install Step 1" />
  <img src={require('./img/setup-install2.png').default} width="45%" alt="Install Step 2" />
</div>

**步骤 6: 完成设置**
安装完成后，请确保勾选了 **"Launch SyncVRC" (运行 SyncVRC)**，然后点击 **Finish (完成)**。应用程序现在将会打开。

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

## ⚠️ 重要提示: Windows Defender SmartScreen

当您尝试首次运行安装程序 (`Setup.exe`) 或该应用程序时，可能会遇到一个蓝色的警告屏幕，提示 **"Windows 已保护你的电脑"**。

**请不要惊慌。SyncVRC 100% 无病毒，可以安全使用。**

### 为什么会发生这种情况？
出现此警告是因为 SyncVRC 是由独立创作者开发的，并且该应用程序文件尚未获得非常昂贵的“数字签名”，或者没有足够的全球下载记录以便 Windows 自动识别它。

此外，每当我们发布新的更新时，文件的代码都会发生改变。如果您看到此屏幕，仅意味着此特定版本 **仍在等待 Microsoft Security Intelligence 团队的白名单批准**。

### 如何绕过此警告:
1. 在蓝色的 SmartScreen 窗口上，点击 **"更多信息" (More info)** 文本链接。
2. 发布者将显示为“未知发布者”。右下角将出现一个新按钮。
3. 点击 **"仍要运行" (Run anyway)** 按钮以继续安装或启动应用程序。

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/smartscreen-warning1.png').default} width="45%" alt="Smartscreen 1" />
  <img src={require('./img/smartscreen-warning2.png').default} width="45%" alt="Smartscreen 2" />
</div>

点击“仍要运行”，即表示您告诉 Windows，您信任直接从我们官方仓库下载的文件。
