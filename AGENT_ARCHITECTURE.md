# Multi-Agent 시스템 설계

**목표**: 각 역할별 전문 Agent를 구성하여 완전 자동화된 개발 팀 구축

---

## 🎯 Agent 역할 정의

### 1. PM Agent (Product Manager)
**역할**: 프로젝트 관리 및 우선순위 결정

**입력**: GitHub Issue
**출력**: 분석된 요구사항, 우선순위, 작업 범위

**책임**:
- Issue 분석 및 분류
- 우선순위 결정 (P0/P1/P2)
- Milestone 할당
- 초기 요구사항 정리

**구현 방법**:
```python
# src/agents/pm_agent.py
class PMAgent:
    def analyze_issue(self, issue: GitHubIssue) -> IssueAnalysis:
        # Gemini로 Issue 분석
        # - 복잡도 측정
        # - 의존성 파악
        # - 우선순위 제안
```

---

### 2. RA Agent (Requirements Analyst)
**역할**: 요구사항 분석 및 Spec 작성

**입력**: PM Agent의 분석 결과
**출력**: spec.md (Feature Specification)

**책임**:
- User Story 작성 (Given-When-Then)
- Functional/Non-Functional Requirements 정의
- Success Criteria 설정
- Edge Cases 파악

**구현 방법**:
```python
# src/agents/ra_agent.py
class RequirementsAnalystAgent:
    def create_specification(self, analysis: IssueAnalysis) -> str:
        # Gemini로 고급 Spec 생성
        # - 요구사항 정교화
        # - 테스트 시나리오 작성
        # - 성공 기준 정의
```

**현재 상태**: ✅ 부분 구현됨 (Gemini Client가 이 역할 수행)

---

### 3. Review Agent (LLM 기반)
**역할**: 문서 품질 검토 및 개선 제안

**입력**: Spec/Plan/Tasks
**출력**: ReviewResult (승인/거부, 개선 제안)

**책임**:
- 문서 완전성 검증
- 논리적 오류 발견
- 모호한 표현 지적
- 개선 제안 제공

**구현 방법**:
```python
# src/agents/llm_review_agent.py (✅ 방금 작성됨!)
class LLMReviewAgent:
    def review_spec(self, content: str) -> ReviewResult:
        # Gemini로 고급 리뷰
        # - 완전성, 명확성, 테스트 가능성 검토
        # - 구체적인 개선 제안
```

**현재 상태**: ✅ 기본 구현 완료, LLM 버전 추가됨

---

### 4. Architect Agent
**역할**: 기술 스택 선정 및 아키텍처 설계

**입력**: Spec
**출력**: plan.md (Implementation Plan)

**책임**:
- 기술 스택 선정
- 시스템 아키텍처 설계
- API 설계
- 데이터베이스 스키마 설계
- Phase별 구현 계획

**구현 방법**:
```python
# src/agents/architect_agent.py
class ArchitectAgent:
    def design_architecture(self, spec: str) -> str:
        # Gemini로 아키텍처 설계
        # - 기술 스택 선정 근거
        # - 확장 가능한 구조 설계
        # - 성능 고려사항
```

**현재 상태**: ✅ 부분 구현됨 (Gemini Client가 Plan 생성)

---

### 5. Coder Agent
**역할**: 실제 코드 구현

**입력**: Tasks (plan.md 기반)
**출력**: 소스 코드, 테스트 코드

**책임**:
- Task별 코드 구현
- 단위 테스트 작성
- 코드 스타일 준수
- 문서화 (docstring)

**구현 방법**:
```python
# src/agents/coder_agent.py
class CoderAgent:
    def implement_task(self, task: Task, context: str) -> CodeOutput:
        # Goose 또는 Gemini Code로 구현
        # - 요구사항 기반 코드 생성
        # - 테스트 포함
        # - SOLID 원칙 준수
```

**구현 옵션**:
- **Option 1**: Goose CLI (✅ 부분 구현됨)
- **Option 2**: Gemini Code Generation
- **Option 3**: Cursor API
- **Option 4**: GitHub Copilot API

**현재 상태**: ✅ Goose 통합 완료

---

### 6. QA Agent
**역할**: 코드 품질 검증 및 테스트

**입력**: Coder Agent의 코드
**출력**: 테스트 결과, 코드 리뷰 의견

**책임**:
- 코드 리뷰 (정적 분석)
- 단위/통합 테스트 실행
- 커버리지 확인
- 보안 취약점 검사
- 성능 측정

**구현 방법**:
```python
# src/agents/qa_agent.py
class QAAgent:
    def review_code(self, code: str, tests: str) -> QAResult:
        # Gemini로 코드 리뷰
        # - 버그 가능성 지적
        # - 성능 개선 제안
        # - 보안 이슈 발견
        
    def run_tests(self, code_path: str) -> TestResult:
        # pytest/jest 등 실행
        # 커버리지 측정
```

**현재 상태**: ❌ 미구현

---

## 🔄 Agent 간 워크플로우

```
GitHub Issue
    ↓
[PM Agent] 분석 및 우선순위
    ↓
[RA Agent] Spec 작성
    ↓
[Review Agent] Spec 검토 ← Gemini LLM
    ↓ (수정 필요시 RA에게 피드백)
    ↓ (승인 시)
[Architect Agent] Plan 설계
    ↓
[Review Agent] Plan 검토 ← Gemini LLM
    ↓ (승인 시)
[PM Agent] Tasks 분해
    ↓
[Coder Agent] 코드 구현 ← Goose/Gemini
    ↓
[QA Agent] 테스트 및 검증
    ↓ (실패 시 Coder에게 피드백)
    ↓ (성공 시)
✅ PR 생성 → Merge
```

---

## 📊 구현 우선순위

### Phase 1: 핵심 Agent (완료 ✅)
- [x] RA Agent (Spec 생성) - Gemini Client
- [x] Review Agent (Mock) - 기본 검증
- [x] Architect Agent (Plan 생성) - Gemini Client
- [x] Coder Agent (구현) - Goose

### Phase 2: LLM 고급화 (진행 중 🔄)
- [x] LLM Review Agent - Gemini 기반 리뷰
- [ ] RA Agent 개선 - 더 정교한 Spec
- [ ] Architect Agent 개선 - 더 체계적인 Plan

### Phase 3: 추가 Agent (예정 📋)
- [ ] PM Agent - Issue 분석 및 우선순위
- [ ] QA Agent - 코드 리뷰 및 테스트
- [ ] DevOps Agent - 배포 자동화

### Phase 4: Agent 협업 (장기 🔮)
- [ ] Agent 간 대화 (토론)
- [ ] 다수결 의사결정
- [ ] 자동 재작업 (iterative improvement)

---

## 🎯 현재 vs 목표

### 현재 (v1.0)
```
Issue → [RA] → Spec → [Mock Review] → Plan → Tasks → [Goose] → Code
```

### 목표 (v2.0)
```
Issue → [PM 분석]
  ↓
[RA] → Spec → [LLM Review ✅] ⟲ (피드백 루프)
  ↓
[Architect] → Plan → [LLM Review] ⟲
  ↓
[PM] → Tasks
  ↓
[Coder] → Code → [QA] ⟲
  ↓
✅ Production
```

---

## 💡 다음 단계

### 즉시 가능
1. **LLM Review Agent 활성화**
   ```python
   review_agent = LLMReviewAgent(use_llm=True)
   ```
2. **Gemini CLI 설치** (AI 리뷰 사용)

### 단기 (1주)
1. RA Agent 독립 클래스 작성
2. Architect Agent 독립 클래스 작성
3. Agent 간 인터페이스 표준화

### 중기 (2주)
1. PM Agent 구현
2. QA Agent 구현
3. Agent 협업 메커니즘

### 장기 (1개월+)
1. Agent 간 대화 시스템
2. 자동 재작업 루프
3. 성능 메트릭 수집

---

**다음은 어떤 Agent를 먼저 구현할까요?**

1. PM Agent (Issue 분석)
2. QA Agent (코드 리뷰)
3. LLM Review Agent 활성화 (Gemini 설치)
4. RA/Architect Agent 독립화
