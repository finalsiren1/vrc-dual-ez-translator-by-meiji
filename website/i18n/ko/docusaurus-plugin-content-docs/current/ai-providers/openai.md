---
title: OpenAI API 키 얻는 방법
sidebar_label: OpenAI (GPT)
sidebar_position: 3
---

# OpenAI API 키 얻기

SyncVRC는 **OpenAI 모델**(예: GPT-4o 또는 GPT-3.5)을 사용한 번역을 지원합니다. OpenAI는 고품질 번역과 광범위한 언어 지원으로 유명한 인기 있는 선택지입니다.

:::warning 면책 조항
개발자가 일일 테스트에 OpenAI API를 주로 사용하지 않으므로 이 튜토리얼이 불완전하거나 약간 오래되었을 수 있습니다. 가장 정확한 정보는 공식 OpenAI 설명서를 참조하십시오.
:::

---

## 키를 얻는 단계

1. **OpenAI 계정 만들기:** [OpenAI Platform](https://platform.openai.com/)을 방문하여 가입하거나 로그인합니다.
2. **API 키 액세스:** 왼쪽 사이드바의 **"API Keys"** 섹션("Dashboard" 또는 "Settings" 메뉴 아래)으로 이동합니다.
3. **새 비밀 키 만들기:** **"+ Create new secret key"** 버튼을 클릭합니다.
4. **이름 지정 및 복사:** 키에 이름(예: "SyncVRC")을 지정하고 **Create**를 클릭합니다. 창을 닫으면 키를 다시 볼 수 없으므로 **즉시 키를 복사하십시오**.
5. **SyncVRC에서 구성:** SyncVRC의 **Settings (설정)** 탭을 열고 엔진으로 `OpenAI`를 선택한 다음 키를 붙여넣습니다.

---

## 중요: 사용 크레딧

* **선불 시스템:** OpenAI는 일반적으로 API가 작동하기 전에 "크레딧"을 미리 구매해야 합니다. 새 계정이더라도 번역 서비스를 시작하려면 잔액에 최소 $5를 추가해야 할 수 있습니다.
* **등급:** 시간이 지남에 따라 플랫폼에서 더 많이 지출함에 따라 "사용 등급"(속도 제한을 결정함)이 증가합니다.
