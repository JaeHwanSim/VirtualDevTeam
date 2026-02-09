당신은 프로젝트 매니저입니다.
다음 Implementation Plan을 기반으로 상세한 Task 목록을 작성하세요.

---

**Plan 문서**:
```markdown
{plan_content}
```

**참고 - Spec 문서**:
```markdown
{spec_content}
```

---

## 출력 요구사항

다음 형식의 Markdown 문서를 작성하세요:

```markdown
# Tasks

**Input**: plan.md, spec.md

## Format: `[ID] [Priority] Description`

## Phase 1: Setup

- [ ] T001 [P1] 프로젝트 구조 생성
- [ ] T002 [P1] 의존성 설치 (`requirements.txt` or `package.json`)
- [ ] T003 [P2] 환경 변수 설정 (`.env`)

---

## Phase 2: Core Implementation

- [ ] T004 [P1] (핵심 모듈 1) 구현 (`src/...`)
- [ ] T005 [P1] (핵심 모듈 2) 구현 (`src/...`)
- [ ] T006 [P2] (유틸리티) 구현 (`src/utils/...`)
- [ ] T007 [P1] 단위 테스트 작성 (`tests/test_...`)

---

## Phase 3: Integration

- [ ] T008 [P1] (통합 작업 1)
- [ ] T009 [P2] Error handling 추가
- [ ] T010 [P3] 로깅 추가

---

## Phase 4: Verification

- [ ] T011 [P1] 통합 테스트 작성
- [ ] T012 [P2] 성능 테스트
- [ ] T013 [P2] README.md 작성

---

## Dependencies & Execution Order

### Phase Dependencies
- Phase 1 완료 → Phase 2 시작 가능
- Phase 2 완료 → Phase 3 시작 가능
- Phase 3 완료 → Phase 4 시작 가능

### Within Each Phase
- Setup: 모든 태스크 병렬 실행 가능
- Core Implementation: T004 → T005 순서, T006-T007 병렬
- Integration: T008 완료 후 T009-T010 병렬
- Verification: 순차 실행

### Parallel Opportunities
- [P2], [P3] 태스크는 병렬 실행 가능
- 테스트는 해당 모듈 구현 후 병렬 작성 가능
```

## 주의사항

- 각 태스크는 **명확한 완료 조건**을 가져야 합니다
- 파일 경로를 명시하세요
- Priority를 [P1], [P2], [P3]로 구분하세요
- 의존성을 명확히 표시하세요
- 실제로 실행 가능한 태스크로 작성하세요
