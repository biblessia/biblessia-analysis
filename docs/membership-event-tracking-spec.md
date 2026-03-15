# Biblessia 멤버십 후원 이벤트 트래킹 명세서

> 작성일: 2026-02-19
> 목적: 멤버십 정기 후원 기능의 전환율 측정 및 수익 분석을 위한 이벤트 설계

---

## 1. 배경

### 멤버십 후원 모델

| 티어 | 월 금액 | 설명 |
|------|---------|------|
| 커피 한 잔 사주기 | 3,000원 | |
| 점심 한 끼 사주기 | 10,000원 | |
| 비타민 챙겨먹여주기 | 20,000원 | |

### 수익 목표

- 단기 (출시 3개월, 6월): 월 50만원 (구독자 ~74명)
- 중기 (출시 6개월, 9월): 월 150만원 (구독자 ~221명)
- 장기 (출시 9개월, 12월): 월 300만원 (구독자 ~441명)

### 왜 이 이벤트가 필요한가

후원 전환은 일반 커머스 퍼널과 달리 "느린 전환(delayed conversion)"입니다.
앱 설치 후 습관이 형성되고, 앱에 대한 감사/애정이 쌓인 후에 전환이 발생합니다.
따라서 세션 내 퍼널이 아닌 **코호트 기반 전환 추적**이 필요하며,
이를 위해 아래 이벤트들이 Amplitude에 정확히 기록되어야 합니다.

---

## 2. 이벤트 명세

### 2-1. PageView - Membership

멤버십 후원 페이지(화면)를 조회했을 때 발생

```
Event Name: "PageView - Membership"
Trigger: 멤버십 페이지가 화면에 표시될 때
```

| Property | Type | Required | 설명 | 예시 |
|----------|------|----------|------|------|
| `source` | string | Y | 어디서 진입했는지 | `"settings"`, `"home_banner"`, `"devotion_complete_popup"`, `"push_notification"` |

**구현 참고:**
- 같은 세션에서 여러 번 진입해도 매번 기록
- source 값으로 어떤 진입 경로가 효과적인지 분석 가능

---

### 2-2. Action - Tap Membership Tier

후원 티어를 선택(탭)했을 때 발생

```
Event Name: "Action - Tap Membership Tier"
Trigger: 특정 후원 티어 버튼을 탭했을 때
```

| Property | Type | Required | 설명 | 예시 |
|----------|------|----------|------|------|
| `tier` | string | Y | 선택한 티어 이름 | `"coffee"`, `"lunch"`, `"vitamin"` |
| `price` | number | Y | 해당 티어 금액 (원) | `3000`, `10000`, `20000` |

**구현 참고:**
- 결제 진행 전 단계 (관심 표현)
- 여러 티어를 번갈아 탭하면 각각 기록

---

### 2-3. Action - Subscribe Membership

멤버십 구독 결제가 완료되었을 때 발생

```
Event Name: "Action - Subscribe Membership"
Trigger: 결제 성공 콜백 수신 시 (서버 확인 후)
```

| Property | Type | Required | 설명 | 예시 |
|----------|------|----------|------|------|
| `tier` | string | Y | 구독한 티어 | `"coffee"`, `"lunch"`, `"vitamin"` |
| `price` | number | Y | 결제 금액 (원) | `3000`, `10000`, `20000` |
| `payment_method` | string | Y | 결제 수단 | `"apple_iap"`, `"google_play"`, `"other"` |
| `is_first_subscription` | boolean | Y | 최초 구독 여부 | `true`, `false` |

**구현 참고:**
- **반드시 결제 성공이 확인된 후에만 발생시킬 것** (클라이언트 추측 X, 서버/스토어 확인 O)
- `is_first_subscription`: 이전에 구독했다가 해지 후 재구독이면 `false`

---

### 2-4. Action - Change Membership Tier

기존 구독자가 티어를 변경했을 때 발생

```
Event Name: "Action - Change Membership Tier"
Trigger: 티어 변경 결제가 완료되었을 때
```

| Property | Type | Required | 설명 | 예시 |
|----------|------|----------|------|------|
| `from_tier` | string | Y | 이전 티어 | `"coffee"` |
| `to_tier` | string | Y | 변경된 티어 | `"lunch"` |
| `from_price` | number | Y | 이전 금액 | `3000` |
| `to_price` | number | Y | 변경 금액 | `10000` |

---

### 2-5. Action - Cancel Membership

구독을 해지했을 때 발생

```
Event Name: "Action - Cancel Membership"
Trigger: 구독 해지 확인 시
```

| Property | Type | Required | 설명 | 예시 |
|----------|------|----------|------|------|
| `tier` | string | Y | 해지한 티어 | `"coffee"` |
| `price` | number | Y | 해지된 금액 | `3000` |
| `duration_days` | number | Y | 구독 유지 기간 (일) | `45` |
| `reason` | string | N | 해지 사유 (선택 입력 시) | `"too_expensive"`, `"not_using"`, `"other"` |

---

### 2-6. User Property 업데이트

멤버십 상태 변경 시 User Property도 함께 업데이트

```
구독 시:
  - membership_status: "active"
  - membership_tier: "coffee" | "lunch" | "vitamin"
  - membership_start_date: "2026-03-15"

해지 시:
  - membership_status: "cancelled"
  - membership_tier: (유지 - 마지막 구독 티어)
  - membership_end_date: "2026-05-20"
```

**이 User Property가 중요한 이유:**
- Amplitude에서 "구독자 vs 비구독자" 세그먼트 비교가 가능해짐
- 구독자의 앱 사용 패턴, 리텐션을 별도로 분석 가능

---

## 3. 이벤트 흐름도

```
[유저 앱 사용]
     │
     ▼
[멤버십 페이지 진입] ─── PageView - Membership (source)
     │
     ▼
[티어 선택] ─────────── Action - Tap Membership Tier (tier, price)
     │
     ▼
[결제 진행]
     │
     ├─ 성공 ─── Action - Subscribe Membership (tier, price, ...)
     │            └─ User Property 업데이트 (membership_status: active)
     │
     └─ 실패 ─── (별도 이벤트 불필요, 퍼널 이탈로 자동 측정)


[기존 구독자]
     │
     ├─ 티어 변경 ─── Action - Change Membership Tier
     │
     └─ 해지 ──────── Action - Cancel Membership
                       └─ User Property 업데이트 (membership_status: cancelled)
```

---

## 4. 분석 활용 가이드

### 4-1. 코호트 전환율 (핵심 지표)

> "가입 후 몇 주 만에 후원 전환하는가?"

```
Amplitude Retention Chart:
  Start Event: [Amplitude] New User
  Return Event: Action - Subscribe Membership
  Method: Rolling (N일 이내 1회 이상)
  Interval: Weekly
  Range: Last 90 Days
```

### 4-2. 관심 → 전환 퍼널

> "멤버십 페이지를 본 사람 중 몇 %가 실제 구독하는가?"

```
Amplitude Funnel:
  Step 1: PageView - Membership
  Step 2: Action - Tap Membership Tier
  Step 3: Action - Subscribe Membership
  Conversion Window: 7 Days
```

### 4-3. 선행 지표 모니터링

| 지표 | 계산 방법 | 목표 |
|------|----------|------|
| 후원 페이지 조회율 | `PageView - Membership 유저 수 / DAU` | 10%+ |
| 페이지 → 구독 전환율 | `Subscribe / PageView - Membership` | 5%+ |
| 월간 신규 구독자 수 | `Subscribe (is_first_subscription=true)` 카운트 | 매월 증가 |
| 월간 해지 수 | `Cancel Membership` 카운트 | 신규의 30% 이하 |
| 구독자 평균 유지 기간 | `Cancel의 duration_days 평균` | 90일+ |

### 4-4. 수익 트래킹

```
MRR (Monthly Recurring Revenue):
  = 활성 구독자 × 티어별 금액

  Amplitude에서:
    - Subscribe 이벤트의 price를 SUM (metric: sums)
    - 단, 해지 반영이 안 되므로 서버사이드 MRR 별도 관리 권장
```

---

## 5. 구현 우선순위

### Phase 1 - 출시와 동시에 (필수)

- [ ] `Action - Subscribe Membership` 이벤트 + 모든 property
- [ ] `Action - Cancel Membership` 이벤트 + 모든 property
- [ ] User Property 업데이트 (`membership_status`, `membership_tier`)

> 이것만 있어도 "몇 명이 구독/해지했는가" 기본 추적 가능

### Phase 2 - 출시 후 1~2주 내

- [ ] `PageView - Membership` 이벤트 + `source` property
- [ ] `Action - Tap Membership Tier` 이벤트

> 퍼널 분석과 진입 경로 최적화 가능

### Phase 3 - 출시 후 1개월 내

- [ ] `Action - Change Membership Tier` 이벤트
- [ ] `Cancel Membership`의 `reason` property (해지 사유 수집 UI)
- [ ] User Property에 `membership_start_date`, `membership_end_date` 추가

---

## 6. 주의사항

1. **이벤트 이름 컨벤션**: 기존 Biblessia 이벤트 (`Action - Complete Devotional`, `PageView - DevotionalDetail` 등)와 동일한 네이밍 규칙 유지
2. **결제 이벤트 신뢰성**: `Subscribe`는 반드시 스토어/서버에서 결제 확인 후 발생. 클라이언트 단독 판단 금지
3. **중복 발생 방지**: 같은 결제에 대해 이벤트가 2번 이상 발생하지 않도록 처리
4. **테스트 환경 분리**: 개발/테스트 시 발생하는 이벤트가 프로덕션 데이터에 섞이지 않도록 주의
