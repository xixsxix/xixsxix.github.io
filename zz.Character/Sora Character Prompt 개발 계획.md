---
title: Sora Character Prompt 개발 계획
created: '"2026-05-06 16:26:04 +0900"'
tags:
  - dami
  - sora
---

# Sora Character Prompt 개발 계획

---

## 🗂️ 1. SYSTEM OVERVIEW (전체 구조)

```markdown
Sora Prompt System
├── 1. Core Identity (정체성)
├── 2. Style Lock (2D 절대 규칙)
├── 3. Anatomy System (비율/형태)
├── 4. Expression System (감정)
├── 5. Fang Mechanism (송곳니 규칙)
├── 6. Pose System (전신 구성)
├── 7. Lighting System (표현 방식)
├── 8. Negative Rules (금지 요소)
└── 9. Prompt Builder (최종 생성기)
```

---

## 🧬 2. CORE IDENTITY (정체성 고정)

```markdown
- Name: Sora
- Type: 2D anime-style fashion illustration character
- Role: Emotional expression-driven character
- Core Focus: Emotion > Form > Detail
```

👉 핵심 한 줄:

> “소라는 감정을 중심으로 움직이는 2D 패션 캐릭터다”

---

## 🎨 3. STYLE LOCK (절대 고정 규칙)

```markdown
✔ Allowed:
- 2D anime illustration
- fashion character sheet style
- clean line art
- soft minimal shading

❌ Forbidden:
- 3D rendering
- clay / figurine / toy style
- photorealism
- CGI / engine render
- material simulation
```

👉 이 파트는 “법” 같은 역할

---

## 🧍 4. ANATOMY SYSTEM (비율 규칙)

```markdown
- Slim elegant proportions
- Long legs, refined torso balance
- Lightweight silhouette
- Fashion illustration anatomy (not realistic)
- Readable shape first, detail second
```

👉 핵심:

> “현실 인간이 아니라 패션 도식 캐릭터”

---

## 😄 5. EXPRESSION SYSTEM (소라 핵심 엔진)

```markdown
Neutral:
- calm, soft gaze

Smile:
- gentle emotional uplift

Laugh:
- bright expression (fang appears)

Tease:
- playful asymmetric smile

Emotion:
- subtle eye-based storytelling
```

👉 핵심:

> “소라는 얼굴이 아니라 감정 장치”

---

## 😈 6. FANG MECHANISM (핵심 IP 기믹)

```markdown
- Hidden canine teeth system
- NOT visible when mouth is closed
- Only appears during natural smile or laugh
- Must be:
  - small
  - cute accent
  - non-threatening
  - emotional highlight

Rule:
Fang = expression effect, not anatomy feature
```

---

## 🧍♀️ 7. POSE SYSTEM (전신 구성 규칙)

```markdown
Default pose:
- upright standing pose

Style:
- fashion model stance
- subtle weight shift
- relaxed arms or soft gesture

Forbidden:
- dynamic action pose
- exaggerated movement
- combat / dramatic posture
```

---

## 💡 8. LIGHTING SYSTEM (표현 규칙)

```markdown
- 2D illustration lighting only
- soft ambient tone
- flat or gradient background
- no physical light simulation
- no realistic shadow behavior
```

---

## 🚫 9. NEGATIVE SYSTEM (절대 금지)

```markdown
- 3D / CGI / render engines
- clay / figurine / toy aesthetics
- photorealism
- heavy texture materials
- hyper-realistic lighting
```

---

## 🧠 10. PROMPT BUILDER (황금 생성기)

👉 이게 핵심이야

```markdown
[CORE IDENTITY]
Sora as a 2D anime fashion illustration character

[STYLE LOCK]
pure 2D, clean anime illustration, fashion sheet style

[ANATOMY]
slim elegant proportions, long legs, refined silhouette

[EXPRESSION]
(choose one: neutral / smile / laugh / tease / emotional gaze)

[FANG RULE]
hidden fang, visible only during natural smile or laugh

[POSE]
standing fashion model pose, subtle weight shift

[LIGHTING]
soft 2D illustration lighting, minimal background

[NEGATIVE]
no 3D, no clay, no photorealism, no CGI
```

---

## 🔥 핵심 개념 (중요)

이 시스템의 진짜 목적은 이거야:

> ❌ “좋은 프롬프트 하나 만들기”  
> ✅ “언제든 동일한 소라를 재생성하는 구조 만들기”

---

## 🚀 이 구조의 장점

## 1️⃣ 일관성 유지

→ 어떤 AI든 결과가 크게 안 흔들림

## 2️⃣ 확장 가능

→ 표정 / 포즈 / 시즌 버전 추가 가능

## 3️⃣ IP화 가능

→ “소라 = 하나의 브랜드 규칙”

---

## 🧩 다음 단계 추천

여기서 진짜 재밌는 건 이제부터야:

## 🎭 1. “소라 표정 시스템 확장 (5 → 12개)”

## 🎬 2. “유튜브 숏츠용 황금 씬 구조”

## 🧠 3. “다미(3D) vs 소라(2D) 세계관 연결 구조”

## 🔁 4. “자동 프롬프트 생성기 (템플릿화)”

---

## 💎 한 줄 정리

> 소라는 이제 “프롬프트 캐릭터”가 아니라 “설계 가능한 2D 시스템 IP”다

---

원하면 다음 단계는 진짜 핵심으로 들어갈 수 있어:

👉 **“소라 황금 프롬프트 1줄 최종 압축 버전”**  
👉 **“Gemini/SD/MJ 공용 버전”**

이건 이제 거의 캐릭터 엔진 만드는 단계야 👍