---
title: 초기 설정
sidebar_label: 초기 설정
sidebar_position: 3
---

# 초기 설정

SyncVRC를 사용하기 전에 AI 및 통신 시스템이 제대로 작동하는지 확인하기 위해 몇 가지 필수 구성이 필요합니다.

## 1. API 키 얻기

SyncVRC는 번역을 처리하기 위해 선호하는 클라우드 AI 제공업체(예: Google Gemini, DeepL 또는 OpenAI)의 API 키가 필요합니다.

1. 선택한 AI 제공업체에 계정을 등록합니다.
2. 개발자 또는 API 대시보드로 이동하여 새 API 키를 생성합니다.
3. API 키를 복사하여 안전하게 보관하십시오. 이 키를 앱의 **Settings (설정)** 탭에 입력해야 합니다.

> **권장 사항:** 무료 등급(예: Gemini 무료 등급)을 사용할 수 있지만, 번역 지연이나 일시 중지를 유발할 수 있는 엄격한 속도 제한이 적용되는 경우가 많습니다. 원활하고 중단 없는 실시간 경험을 위해 제공업체의 종량제(선불) 요금제로 업그레이드하는 것을 강력히 권장합니다.

## 2. NVIDIA CUDA Toolkit 설치 (선택 사항)

SyncVRC는 고속 음성 인식(Faster-Whisper)을 위해 GPU를 활용할 수 있습니다. 그러나 이는 **선택 사항**이며 NVIDIA GPU에 특별히 최적화되어 있습니다.

* **NVIDIA 사용자**: 최대 성능을 얻으려면 [NVIDIA CUDA Toolkit 12.x](https://developer.nvidia.com/cuda-12-9-1-download-archive)를 다운로드하여 설치하십시오. **참고:** 설치 후 PC를 재부팅해야 합니다.
* **AMD/Intel 또는 GPU가 없는 사용자**: CUDA를 설치할 필요가 없습니다. 애플리케이션은 자동으로 CPU를 사용하도록 대체됩니다.
* **장치 변경**: [**Settings > AI & Translation Engine**](../settings/api-engine)에서 언제든지 GPU와 CPU 처리 간에 수동으로 전환할 수 있습니다.

## 3. VRChat OSC 활성화

이 앱은 OSC 프로토콜을 통해 VRChat과 통신하여 채팅창에 입력하고 음소거 상태를 동기화합니다.

1. VRChat을 실행하고 **방사형 메뉴(Radial Menu)**를 엽니다.
2. **Options > OSC**로 이동합니다.
3. OSC를 **Enabled (활성화됨)**로 설정합니다.

**OSC 상태 확인:** 활성화되고 VRChat이 실행 중이면 SyncVRC 사이드바 왼쪽 하단을 확인합니다. 성공적인 연결을 확인하려면 **OSC Status** 표시등이 **🟢 Detected**로 업데이트되어야 합니다.

> 🖼️ **[IMAGE PLACEHOLDER: OSC Status]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![OSC Status](/img/setup-osc.png)`)*

## 4. 오디오 장치 구성

올바른 오디오 라우팅은 성공적인 번역의 핵심입니다.

* **Outgoing (송신)**: 물리적 마이크를 선택합니다.
* **Incoming (수신)**: 데스크톱/게임 오디오를 캡처하는 **루프백(Loopback)** 또는 **가상 오디오 장치(Virtual Audio Device)**(예: VB-Cable, Voicemeeter)를 선택합니다. 물리적 스피커를 직접 선택할 수는 없습니다.
