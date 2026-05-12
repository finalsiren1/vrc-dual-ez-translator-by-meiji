---
title: 메시지 송신 (Outgoing)
sidebar_label: 송신 번역
sidebar_position: 4
---

# VRChat으로 메시지 보내기 (Outgoing)

**송신(Outgoing) 시스템**은 사용자의 음성이나 텍스트를 번역하여 VRChat 채팅창으로 직접 보냅니다. 이를 통해 다른 플레이어는 사용자가 말하는 내용을 모국어로 실시간으로 읽을 수 있습니다.

## 전제 조건

시작하기 전에 **Translation (번역)** 탭에 있는지 확인하고 다음을 구성했는지 확인하십시오.
1. **Select Microphone (마이크 선택):** *Audio Setup (오디오 설정)* 탭에서 물리적 마이크를 선택합니다.
2. **Language Setup (언어 설정):** 모국어(**From (번역 출발 언어)**) 및 대상 언어(**Translate to (번역 도착 언어)**)를 설정합니다.

---

## 방법 1: 자동 음성 번역 (연속)

핸즈프리하고 자연스러운 대화에 이상적입니다. AI는 사용자가 언제 말하고 언제 일시 중지하는지 자동으로 감지합니다.

1. **Auto (Continuous) (자동 (연속))** 모드를 선택합니다.
2. **Start Outgoing (송신 시작)** 버튼을 클릭합니다(또는 할당된 단축키를 누릅니다. 기본값: `F2`).
3. 버튼이 빨간색으로 바뀌어 시스템이 활성 상태임을 나타냅니다. 마이크에 대고 말하기만 하면 됩니다.
4. AI가 음성을 처리하고 번역을 VRChat으로 자동으로 보냅니다.

> 🖼️ **[IMAGE PLACEHOLDER: Auto Mode]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![Auto Mode](/img/outgoing-auto.png)`)*

---

## 방법 2: 푸시 투 토크 (누르고 말하기)

시끄러운 환경이나 특정 문장만 번역하려는 경우에 가장 좋습니다.

1. **Push to Record (누르고 녹음하기)** 모드를 선택합니다.
2. **Start Outgoing (송신 시작)**을 클릭하여 AI 엔진을 초기화합니다.
3. 이제 **Hold to Speak (누르고 말하기)** 버튼이 활성화됩니다.
4. 말하는 동안 **Hold to Speak** 버튼을 클릭한 채로 유지합니다(또는 할당된 푸시 투 토크 단축키를 누른 채로 유지합니다).
5. 완료되면 버튼을 놓습니다. 번역이 즉시 처리되고 전송됩니다.

> 🖼️ **[IMAGE PLACEHOLDER: Push-to-Talk Mode]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![Push-to-Talk Mode](/img/outgoing-push.png)`)*

---

## 방법 3: 수동 텍스트 입력

입력하는 것을 선호하거나 말하지 않고 특정 문구를 보내야 하는 경우 수동 번역 상자를 사용할 수 있습니다.

1. VRChat 연결을 설정하려면 먼저 **Start Outgoing (송신 시작)**을 클릭**해야** 합니다.
2. 왼쪽 패널 하단의 **Manual Translate (Type and Send) (수동 번역(입력 및 전송))** 텍스트 상자에 메시지를 입력합니다.
3. 키보드의 **Enter**를 누르거나 **Send (전송)** 버튼을 클릭합니다.
4. 입력한 텍스트와 번역이 채팅창으로 전송됩니다.

> 🖼️ **[IMAGE PLACEHOLDER: Manual Text Input]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![Manual Text Input](/img/outgoing-manual.png)`)*

---

## 예상 결과

AI가 입력을 처리하면 결과가 OSC를 통해 VRChat으로 전송됩니다. 아바타 머리 위에 말풍선으로 표시되며, 일반적으로 원본 텍스트 뒤에 번역된 텍스트가 표시됩니다.

> 🖼️ **[IMAGE PLACEHOLDER: VRChat Result]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![VRChat Result Example](/img/outgoing-result.png)`)*
