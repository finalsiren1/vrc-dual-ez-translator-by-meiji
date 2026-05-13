---
title: 수신 시스템 (음성 번역)
sidebar_label: 수신 시스템 (음성 번역)
sidebar_position: 5
---

# 수신 시스템 (음성 번역)

**수신(Incoming) 시스템**은 게임에서 나오는 오디오(다른 플레이어의 음성)를 듣고 이를 모국어로 번역합니다. 송신 시스템과 달리 이러한 번역은 SyncVRC 앱 인터페이스에 비공개로 표시되며 VRChat 채팅창으로 **전송되지 않습니다**.

## 전제 조건: 오디오 라우팅 (중요한 단계)

다른 플레이어를 번역하려면 앱에서 게임 오디오를 "들어야" 합니다. **물리적 "스피커" 또는 "헤드폰"을 직접 선택할 수는 없습니다.**

1. **Audio Setup (오디오 설정)** 탭으로 이동합니다.
2. **Select Speaker Loopback (Virtual Audio) (스피커 루프백(가상 오디오) 선택)** 드롭다운에서 루프백 장치를 선택해야 합니다.
3. *권장 가상 오디오 장치:* Windows 스테레오 믹스, VB-Cable, Voicemeeter 또는 Elgato Wave Link.

<img 
  src={require('./img/incoming-audio.jpg').default} 
  width="900" 
  alt="Incoming Audio" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 수신 시스템 사용 방법

오디오가 올바르게 라우팅되면 다음 단계에 따라 번역을 시작하십시오.

### 1. 언어 설정
**Translation (번역)** 탭의 오른쪽 패널에서 언어를 구성합니다.
* **Listen Language (인식 언어):** 다른 플레이어가 말하는 언어(예: 일본어)로 설정합니다.
* **Translate to (번역할 언어):** 모국어(예: 영어)로 설정합니다.

### 2. 엔진 시작
**Start Incoming (수신 시작)** 버튼을 클릭합니다(또는 할당된 단축키를 누릅니다. 기본값: `F3`). 데스크톱 오디오를 활발하게 듣고 있음을 나타내기 위해 버튼이 빨간색으로 바뀝니다.

<img 
  src={require('./img/incoming-start.jpg').default} 
  width="900" 
  alt="Incoming Start" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

### 3. 번역 읽기
상대방이 말하면 AI가 오디오를 실시간으로 처리합니다. 원본 텍스트와 번역된 텍스트가 앱 오른쪽 하단의 **Incoming Log (수신 로그)** 텍스트 상자에 나타납니다.

<img 
  src={require('./img/incoming-result.jpg').default} 
  width="900" 
  alt="Incoming Result" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

**💡 전문가 팁:** **송신(Outgoing)** 시스템과 **수신(Incoming)** 시스템을 동시에 실행하여 원활한 양방향 번역 대화를 나눌 수 있습니다!
