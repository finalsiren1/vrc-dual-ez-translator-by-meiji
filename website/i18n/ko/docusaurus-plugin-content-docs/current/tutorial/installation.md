---
title: 설치
sidebar_label: 설치
sidebar_position: 2
---

# SyncVRC 설치 방법

SyncVRC 설치는 간단합니다. 아래 단계에 따라 PC에서 응용 프로그램을 실행하십시오.

## 단계별 설치

**1단계: 설치 프로그램 다운로드**
먼저, [공식 GitHub Releases 페이지](https://github.com/finalsiren1/SyncVRC/releases)에서 최신 `SyncVRC_Setup_vX.X.X.exe` 파일을 다운로드합니다.

**2단계: 설치 언어 선택**
다운로드한 `.exe` 파일을 실행합니다. 설치 중에 사용할 언어를 선택하라는 메시지가 나타납니다. 원하는 언어(예: English)를 선택하고 **OK**를 클릭합니다.

<img 
  src={require('./img/setup-lang.jpg').default} 
  width="300" 
  alt="Setup Lang" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**3단계: 설치 위치 선택**
설치 프로그램이 SyncVRC를 설치할 위치를 묻습니다. 기본 경로는 보통 `C:\Program Files\SyncVRC`입니다. 기본값을 그대로 유지하거나 **Browse (찾아보기)**를 클릭하여 다른 폴더를 선택할 수 있습니다. **Next (다음)**를 클릭하여 계속합니다.

<img 
  src={require('./img/setup-dest.png').default} 
  width="600" 
  alt="Setup Dest" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**4단계: 추가 작업 선택**
바탕 화면에서 SyncVRC에 쉽게 액세스하려면 **"Create a desktop shortcut" (바탕 화면 바로 가기 만들기)** 상자를 선택합니다. **Next (다음)**를 클릭합니다.

<img 
  src={require('./img/setup-tasks.png').default} 
  width="600" 
  alt="Setup Task" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

**5단계: 검토 및 설치**
"Ready to Install (설치 준비 완료)" 화면에서 설치 설정을 검토합니다. 모든 것이 올바르게 보이면 **Install (설치)**를 클릭합니다. 추출 및 설치 과정이 완료될 때까지 기다립니다.

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/setup-install1.png').default} width="45%" alt="Install Step 1" />
  <img src={require('./img/setup-install2.png').default} width="45%" alt="Install Step 2" />
</div>

**6단계: 설정 완료**
설치가 완료되면 **"Launch SyncVRC" (SyncVRC 실행)**가 선택되어 있는지 확인하고 **Finish (완료)**를 클릭합니다. 이제 앱이 열립니다.

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

## ⚠️ 중요: Windows Defender SmartScreen

설치 프로그램(`Setup.exe`)이나 앱을 처음 실행하려고 할 때 **"Windows의 PC 보호"**라는 파란색 경고 화면이 나타날 수 있습니다.

**당황하지 마십시오. SyncVRC는 100% 바이러스가 없으며 사용하기에 안전합니다.**

### 왜 이런 일이 발생합니까?
이 경고는 SyncVRC가 독립 창작자에 의해 개발되었으며 응용 프로그램 파일에 아직 매우 비싼 "디지털 서명"이 없거나 Windows에서 자동으로 인식할 만큼 글로벌 다운로드 기록이 충분하지 않기 때문에 나타납니다.

또한 새로운 업데이트를 출시할 때마다 파일의 코드가 변경됩니다. 이 화면이 나타나면 단순히 이 특정 버전이 **Microsoft Security Intelligence 팀의 화이트리스트 승인을 아직 기다리고 있음**을 의미합니다.

### 경고 우회 방법:
1. 파란색 SmartScreen 창에서 **"추가 정보" (More info)** 텍스트 링크를 클릭합니다.
2. 게시자가 "알 수 없는 게시자"로 표시됩니다. 오른쪽 하단에 새 버튼이 나타납니다.
3. **"실행" (Run anyway)** 버튼을 클릭하여 설치를 계속하거나 앱을 시작합니다.

<div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '40px', marginTop: '20px' }}>
  <img src={require('./img/smartscreen-warning1.png').default} width="45%" alt="Smartscreen 1" />
  <img src={require('./img/smartscreen-warning2.png').default} width="45%" alt="Smartscreen 2" />
</div>

"실행"을 클릭하면 공식 저장소에서 직접 다운로드한 파일을 신뢰한다는 것을 Windows에 알리는 것입니다.
