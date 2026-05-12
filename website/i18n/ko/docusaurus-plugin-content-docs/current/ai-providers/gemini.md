---
title: Gemini API 키 얻는 방법
sidebar_label: Google Gemini
sidebar_position: 1
---

# Google Gemini API 키 얻기

Google Gemini는 빠른 속도와 상황에 맞는 정확성 때문에 SyncVRC에 권장되는 번역 엔진입니다. **Google AI Studio**를 통해 무료로 API 키를 얻을 수 있습니다.

키를 생성하고 구성하려면 다음 단계를 따르십시오.

---

## 1단계: Google AI Studio 방문

1. [Google AI Studio](https://aistudio.google.com/) 웹사이트로 이동합니다.
2. 표준 Google 계정으로 로그인합니다.

> 🖼️ **[IMAGE PLACEHOLDER: AI Studio Login Page]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![AI Studio Login](/img/gemini-login.png)`)*

---

## 2단계: 새 API 키 생성

1. 왼쪽 사이드바에서 **"Get API key(API 키 얻기)"** 버튼(열쇠 아이콘)을 클릭합니다.
2. **"Create API key(API 키 만들기)"**라는 파란색 버튼을 클릭합니다.
3. Google Cloud 프로젝트를 선택하라는 메시지가 표시될 수 있습니다. 프로젝트가 없는 경우 **"Create API key in new project(새 프로젝트에서 API 키 만들기)"**를 선택합니다.
4. 생성되면 팝업에 API 키가 표시됩니다. **이 키를 즉시 복사하십시오.**

> 🖼️ **[IMAGE PLACEHOLDER: Create API Key Button]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![Create API Key](/img/gemini-create-key.png)`)*

---

## 3단계: SyncVRC에서 구성

1. **SyncVRC** 애플리케이션을 엽니다.
2. **Settings (설정)** 탭으로 이동합니다.
3. **AI & Translation Engine**에서 **Translation Engine**을 `Google Gemini`로 설정합니다.
4. 복사한 키를 **API Key** 필드에 붙여넣고 **Save (저장)**를 클릭합니다.

> 🖼️ **[IMAGE PLACEHOLDER: SyncVRC Settings Setup]** *(준비가 되면 이 줄을 다음과 같이 교체하십시오: `![SyncVRC Settings](/img/settings-gemini-setup.png)`)*

---

## 중요: 무료 등급 vs. 유료 요금제

Google은 Gemini에 대해 관대한 **무료 등급**을 제공하지만 VRChat 사용자에게는 몇 가지 중요한 절충점이 있습니다.

### 1. 무료 등급 (테스트용으로 권장)
* **속도 제한:** 분당 요청이 제한됩니다. 매우 빠르게 말하면 "API Limit Exceeded" 오류가 발생할 수 있습니다.
* **데이터 개인 정보 보호:** Google은 모델을 개선하기 위해 입력/출력 데이터를 사용할 수 있습니다.
* **비용:** 완전 무료.

### 2. 종량제 (최상의 경험을 위해 권장)
* **안정성:** 속도 제한이 높기 때문에 격렬한 대화 중에도 번역이 일시 중지되지 않습니다.
* **개인 정보 보호:** 데이터는 Google 모델을 학습하는 데 **사용되지 않습니다**.
* **비용:** 사용한 만큼만 지불합니다(일반적으로 활발하게 말하는 1시간당 몇 센트).

**업그레이드 방법:** Google AI Studio에서 **"설정"**(톱니바퀴 아이콘) > **"요금제 및 결제"**를 클릭하여 신용카드를 연결하고 종량제를 활성화합니다.

---

## 보안 경고 ⚠️

**API 키를 절대 다른 사람과 공유하지 마십시오.** API 키는 지갑 비밀번호와 같습니다. 다른 사람이 키를 얻으면 할당량을 사용하거나 결제 계정에 요금을 청구할 수 있습니다. SyncVRC는 키를 PC에 로컬로 저장하고 방송 중 우발적인 유출을 방지하기 위해 UI에서 별표로 마스킹합니다.
