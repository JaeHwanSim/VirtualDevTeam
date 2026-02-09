# Tasks: 자율 개발 시스템 (Autonomous Dev System)

**Input**: [spec.md](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/spec.md), [plan.md](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/plan.md)

**Prerequisites**: Constitution v1.1.0, spec.md (P1-P4 User Stories), plan.md (4단계 구현 플랜)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 병렬 실행 가능 (다른 파일, 의존성 없음)
- **[Story]**: 해당 태스크가 속한 User Story (US1, US2, US3, US4)
- 정확한 파일 경로 포함

---

## Phase 1: Setup (공통 인프라)

**Purpose**: 프로젝트 초기화 및 기본 구조

- [x] T001 프로젝트 구조 생성 (`src/`, `tests/`)
- [x] T002 Python 의존성 설치 (`requirements.txt`)
- [x] T003 [P] 환경 변수 설정 (`.env`)

---

## Phase 2: Foundational (필수 선행 작업)

**Purpose**: 모든 User Story가 의존하는 핵심 인프라

**⚠️ CRITICAL**: 이 Phase 완료 전에는 User Story 작업 시작 불가

- [ ] T004 GitHub API 클라이언트 구현 (`src/integrations/github_client.py`)
- [ ] T005 [P] 워크플로우 상태 모델 (`src/models/workflow_state.py`)
- [ ] T006 [P] Issue 데이터 모델 (`src/models/issue.py`)
- [ ] T007 [P] 파일 관리 유틸리티 (`src/utils/file_manager.py`)
- [ ] T008 Review Agent Mock 구현 (`src/workflow/review_agent.py`)

**Checkpoint**: 기반 인프라 준비 완료 - User Story 구현 시작 가능

---

## Phase 3: User Story 1 - GitHub Issue→Spec 자동 생성 (Priority: P1) 🎯 MVP

**Goal**: GitHub Issue 생성 시 자동으로 `spec.md` 생성 및 Slack 알림

**Independent Test**: GitHub Issue 생성 → `specs/[issue-number]-[title]/spec.md` 파일 생성 확인

### Implementation for User Story 1

- [ ] T009 [P] [US1] GitHub Webhook 엔드포인트 추가 (`src/main.py`)
- [ ] T010 [P] [US1] Spec 생성 로직 (`src/workflow/stage_executor.py`)
- [ ] T011 [US1] Spec 생성 워크플로우 통합 (`src/workflow/orchestrator.py`)
- [ ] T012 [US1] Slack 알림 기능 통합
- [ ] T013 [US1] 에러 핸들링 및 로깅

**Checkpoint**: User Story 1 완료 - Issue→Spec 자동 생성 기능 동작

---

## Phase 4: User Story 2 - Spec→Plan 자동 생성 (Priority: P2)

**Goal**: Spec 승인 후 자동으로 `plan.md` 생성

**Independent Test**: spec.md 승인 → `plan.md` 자동 생성 확인

### Implementation for User Story 2

- [ ] T014 [P] [US2] Plan 생성 로직 (`src/workflow/stage_executor.py`)
- [ ] T015 [US2] 승인 후 다음 단계 트리거 메커니즘
- [ ] T016 [US2] Plan 생성 워크플로우 통합

**Checkpoint**: User Story 1 & 2 모두 독립적으로 동작

---

## Phase 5: User Story 3 - Plan→Tasks 자동 생성 (Priority: P3)

**Goal**: Plan 승인 후 자동으로 `tasks.md` 생성

**Independent Test**: plan.md 승인 → `tasks.md` 자동 생성 확인

### Implementation for User Story 3

- [ ] T017 [P] [US3] Tasks 생성 로직 (`src/workflow/stage_executor.py`)
- [ ] T018 [US3] Tasks 생성 워크플로우 통합
- [ ] T019 [US3] 의존성 분석 (선택사항)

**Checkpoint**: User Story 1, 2, 3 모두 독립적으로 동작

---

## Phase 6: User Story 4 - Tasks→구현 자동 실행 (Priority: P4)

**Goal**: Tasks 승인 후 Goose 자동 실행

**Independent Test**: tasks.md 승인 → Goose 세션 시작 확인

### Implementation for User Story 4

- [ ] T020 [P] [US4] Goose CLI 호출 로직 (`src/workflow/stage_executor.py`)
- [ ] T021 [US4] Tasks 파싱 및 순차 실행
- [ ] T022 [US4] pytest 실행 및 결과 리포트
- [ ] T023 [US4] 최종 결과 Slack 알림

**Checkpoint**: 전체 워크플로우 완성 (Issue → 구현)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 전체 시스템 개선

- [ ] T024 [P] 통합 테스트 작성 (`tests/test_workflow.py`)
- [ ] T025 [P] 단위 테스트 작성 (`tests/test_github_client.py` 등)
- [ ] T026 에러 복구 메커니즘 (Polling fallback)
- [ ] T027 [P] 로깅 강화 (`src/utils/logger.py`)
- [ ] T028 README.md 및 사용 가이드 작성

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 즉시 시작 가능 ✅ 완료
- **Foundational (Phase 2)**: Setup 완료 후 - **모든 User Story를 BLOCK**
- **User Stories (Phase 3-6)**: Foundational 완료 후 시작
  - 병렬 진행 가능 (팀 역량에 따라)
  - 또는 순차 진행 (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: 원하는 User Story 완료 후

### User Story Dependencies

- **User Story 1 (P1)**: Foundational 완료 후 - 다른 Story 의존성 없음
- **User Story 2 (P2)**: Foundational 완료 후 - US1 통합 가능하지만 독립 테스트 가능
- **User Story 3 (P3)**: Foundational 완료 후 - US1/US2와 통합하지만 독립 테스트 가능
- **User Story 4 (P4)**: Foundational 완료 후 - 전체 워크플로우 종점

### Within Each User Story

- Models/Utils 먼저 → Services 다음 → Orchestration 마지막
- 에러 핸들링은 핵심 로직 후
- Story 완료 후 다음 priority로 이동

### Parallel Opportunities

- Foundational Phase 내 모든 [P] 태스크 병렬 실행
- User Stories는 서로 다른 팀원이 병렬 작업 가능
- Polish Phase 내 모든 [P] 태스크 병렬 실행

---

## Implementation Strategy

### MVP First (User Story 1만)

1. Phase 1: Setup ✅ 완료
2. Phase 2: Foundational (CRITICAL)
3. Phase 3: User Story 1
4. **STOP & VALIDATE**: Issue→Spec 기능 독립 테스트
5. 필요시 배포/데모

### Incremental Delivery

1. Setup + Foundational → 기반 완성
2. + User Story 1 → Issue→Spec 자동화 (MVP!)
3. + User Story 2 → Spec→Plan 자동화
4. + User Story 3 → Plan→Tasks 자동화
5. + User Story 4 → 전체 워크플로우 완성

---

## Notes

- [P] 태스크 = 병렬 실행 가능
- [Story] 레이블로 User Story 추적
- 각 User Story는 독립적으로 완료 및 테스트 가능
- 각 Checkpoint에서 독립 검증
- 커밋은 태스크 또는 논리적 그룹 단위로
