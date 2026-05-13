---
title: 오디오 설정
sidebar_label: 오디오 설정
sidebar_position: 1
---

# 오디오 설정

**Audio Setup (오디오 설정)** 탭은 SyncVRC 오디오 라우팅의 핵심입니다. 여기의 설정이 잘못되면 AI가 사용자의 음성이나 다른 플레이어의 음성을 선택하지 못하는 가장 일반적인 원인이 됩니다.

하드웨어 및 소프트웨어 오디오를 올바르게 구성하려면 다음 세부 분류를 따르십시오.

## 1. 마이크 선택 (Outgoing)

이 설정은 AI가 **송신(Outgoing)** 번역 시스템(사용자의 음성)을 위해 듣는 내용을 제어합니다.

* **선택할 항목:** 기본 물리적 마이크(예: VR 헤드셋 마이크, USB 콘덴서 마이크 또는 XLR 인터페이스 입력)를 선택합니다.
* **중요:** Windows에서 마이크가 음소거되어 있지 않은지 확인하십시오. 그렇지 않으면 AI는 침묵만 듣게 됩니다.

<img 
  src={require('./img/audio-mic.jpg').default} 
  width="900" 
  alt="Audio Mic" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 2. 스피커 루프백 선택 (Incoming)

이 설정은 AI가 **수신(Incoming)** 번역 시스템(다른 플레이어의 음성)을 위해 듣는 내용을 제어합니다.

* **문제점:** 음성 인식 엔진은 물리적 스피커나 헤드폰에서 '나오는' 오디오를 직접 캡처할 수 없습니다.
* **해결책 (가상 오디오):** 데스크톱 오디오가 헤드폰에 도달하기 전에 데스크톱 오디오를 가로채는 "루프백" 또는 "가상 오디오" 장치를 선택해야 합니다.
* **지원되는 옵션:**
  * **Windows 스테레오 믹스 (Stereo Mix)** (대부분의 Windows PC에 내장되어 있지만 Windows 소리 설정에서 활성화해야 할 수 있음).
  * **VB-Cable** (무료 가상 오디오 케이블).
  * **Voicemeeter** (고급 오디오 믹싱 소프트웨어).
  * **Elgato Wave Link** 또는 **SteelSeries Sonar** (각각의 하드웨어를 사용하는 경우).

<img 
  src={require('./img/audio-speaker.jpg').default} 
  width="900" 
  alt="Audio Speaker" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

## 3. VRC 음소거 동기화 활성화

VRChat을 위해 특별히 제작된 중요한 개인 정보 보호 및 최적화 기능입니다.

* **작동 방식:** 활성화되면 SyncVRC는 VRChat OSC 매개변수를 읽습니다. VR 컨트롤러 또는 VRChat 방사형 메뉴를 사용하여 마이크를 음소거하면 SyncVRC는 송신(Outgoing) 번역을 즉시 일시 중지합니다.
* **사용 이유:** 음소거된 상태에서 AI가 배경 소음을 지속적으로 듣고 API 제공업체로 보내는 것을 방지하여 API 할당량을 절약하고 완전한 개인 정보 보호를 보장합니다.

<img 
  src={require('./img/audio-mutesync.jpg').default} 
  width="900" 
  alt="Audio Mute Sync" 
  style={{ marginTop: '20px', marginBottom: '40px', marginLeft: '30px' }} 
/>

---

AI가 음성을 처리하는 방법을 미세 조정하려면 [**고급 오디오 설정 (Advanced Audio Settings)**](./advanced-audio) 페이지로 진행하십시오.
