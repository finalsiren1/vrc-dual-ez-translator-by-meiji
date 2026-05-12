---
title: Installation Guide
sidebar_label: Installation
sidebar_position: 2
---

# How to Install SyncVRC

Installing SyncVRC is straightforward. Follow the steps below to get the application running on your PC.

## Step-by-Step Installation

**Step 1: Download the Installer**
First, download the latest `SyncVRC_Setup_vX.X.X.exe` file from our official GitHub Releases page.

**Step 2: Select Setup Language**
Run the downloaded `.exe` file. You will be prompted to select the language to use during the installation. Select your preferred language (e.g., English) and click **OK**.

<img 
  src={require('./img/setup-lang.jpg').default} 
  width="300" 
  alt="Select Language" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**Step 3: Select Destination Location**
The setup will ask where you want to install SyncVRC. The default path is usually `C:\Program Files\SyncVRC`. You can leave this as default or click **Browse** to choose a different folder. Click **Next** to continue.

<img 
  src={require('./img/setup-dest.png').default} 
  width="600" 
  alt="Select Language" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**Step 4: Select Additional Tasks**
Check the box for **"Create a desktop shortcut"** if you want easy access to SyncVRC from your desktop. Click **Next**.

<img 
  src={require('./img/setup-tasks.png').default} 
  width="600" 
  alt="Select Language" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**Step 5: Review and Install**
Review your installation settings on the "Ready to Install" screen. If everything looks correct, click **Install**. Wait for the extraction and installation process to complete.

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/setup-install1.png').default} width="45%" alt="Install Step 1" />
  <img src={require('./img/setup-install2.png').default} width="45%" alt="Install Step 2" />
</div>

**Step 6: Finish Setup**
Once the installation is complete, make sure **"Launch SyncVRC"** is checked and click **Finish**. The app will now open.

<img 
  src={require('./img/setup-finish.png').default} 
  width="600" 
  alt="Select Language" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## ⚠️ Important: Windows Defender SmartScreen

When you try to run the installer (`Setup.exe`) or the app for the first time, you might encounter a blue warning screen that says **"Windows protected your PC"**. 

**Please do not panic. SyncVRC is 100% virus-free and safe to use.**

### Why does this happen?
This warning appears because SyncVRC is developed by an independent creator, and the application file does not yet have a highly expensive "Digital Signature" or enough global download history for Windows to automatically recognize it. 

Furthermore, whenever we release a new update, the file's code changes. If you see this screen, it simply means this specific version is **still pending whitelist approval from the Microsoft Security Intelligence team**.

### How to bypass the warning:
1. On the blue SmartScreen window, click on the **"More info"** text link.
2. The publisher will show as "Unknown publisher". A new button will appear at the bottom right.
3. Click the **"Run anyway"** button to proceed with the installation or launch the app.

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/smartscreen-warning1.png').default} width="45%" alt="Install Step 1" />
  <img src={require('./img/smartscreen-warning2.png').default} width="45%" alt="Install Step 2" />
</div>

By clicking "Run anyway," you are telling Windows that you trust the file downloaded directly from our official repository.