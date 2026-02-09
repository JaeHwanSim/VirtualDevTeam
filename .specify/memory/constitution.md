<!--
Sync Impact Report:
- Version: 1.0.0 → 1.1.0 (MINOR: Issue-Driven Workflow, Slack Confirmation 원칙 추가)
- Modified Principles:
  - 기존 5개 원칙 유지
- Added Sections:
  - VI. Issue-Driven Workflow - GitHub Issue 기반 자동 워크플로우
  - VII. Slack-Based Confirmation - 2단계 승인 프로세스 (Review Agent → 사용자)
- Templates Status:
  - .specify/templates/plan-template.md: ✅ Compatible.
  - .specify/templates/spec-template.md: ✅ Compatible.
  - .specify/templates/tasks-template.md: ✅ Compatible.
-->
# 📜 가상 개발팀 프로젝트 헌법 (Constitution)

## 1. 운영 철학 (Operating Philosophy)
- **SDD 지향 (Specification-Driven Development):** 모든 개발은 명세(Specification)에서 시작하며, 문서와 코드의 동기화를 엄격히 유지한다.
- **비용 최적화 (Cost Optimization):** Gemini Enterprise CLI 사용을 극대화하고, API 비용 지출을 최소화한다.
- **자율 실행 (Autonomous Execution):** GitHub Issue에서 시작된 작업은 승인된 범위 내에서 에이전트가 자율적으로 진행한다.

## 2. 에이전트 역할 및 책임 (Agent Roles & Responsibilities)
- **Goose Manager:** 워크플로우 전체를 지휘하며 `status.md`를 통해 마일스톤을 관리한다.
- **Requirement Agent:** `specify-cli`를 도구로 사용하여 정밀한 기획안을 도출한다.
- **Review Agent:** 기획 및 코드의 무결성을 검증하며, 'REJECT' 권한을 가진다.

## 3. 마일스톤 관리 (Milestone Management)
- **M1 (Spec-Lock):** 기획/리뷰 에이전트 합의 후 사용자가 `spec.md`를 최종 승인한 단계.
- **M2 (Code-Complete):** Goose가 구현 및 셀프 힐링 테스트를 마친 단계.

## 4. 코드 품질 가이드라인 (Code Quality Guidelines)
- 모든 함수는 Docstring을 포함한다.
- `pytest` 통과율 100%를 지향한다.

## 5. 핵심 원칙 (Core Principles)

**I. Specification-Driven Development (SDD)**
모든 구현은 명세에서 시작합니다. `specs/**/spec.md`가 생성되고 인간(Human-in-the-loop)의 승인을 받기 전까지는 소스코드 파일을 단 하나도 생성하거나 수정할 수 없습니다.

**II. Multi-Agent Conflict & Synergy**
에이전트 간의 '비판적 검토'를 의무화합니다. Planner Agent가 작성한 기획안은 반드시 Review Agent의 검증을 통과해야 하며, Review Agent는 기획의 모호함이나 예외 처리 누락을 발견할 경우 즉시 'REJECT'를 선언해야 합니다.

**III. Human-in-the-Loop Milestones**
AI의 독단적인 진행을 막기 위해 마일스톤 승인제를 운영합니다. 명세 확정(M1), 구현 계획 수립, 최종 코드 완료 시점에서 시스템은 반드시 사용자의 명시적 승인(APPROVED)을 기다려야 합니다.

**IV. Hybrid Cost Control**
지능 공급의 우선순위를 지킵니다. 모든 명세 분석 및 가벼운 구현은 정액제 Gemini CLI를 최우선으로 사용하며, 복잡한 로직이나 할당량 초과 시에만 API(Tetrate)를 보조적으로 활용합니다.

**V. Test-First Implementation**
구현 단계에서 Goose는 반드시 테스트 코드를 먼저 작성하거나 로직과 동시에 작성해야 합니다. `pytest` 통과율 100% 달성 전에는 작업을 종료할 수 없습니다.

**VI. Issue-Driven Workflow**
모든 작업은 GitHub Issue에서 시작합니다. Issue가 생성되면 시스템은 자동으로 다음 순서를 따릅니다:
1. `constitution.md` 검토 및 업데이트 (필요시)
2. `spec.md` 생성 → Review Agent 검토 → 사용자 승인
3. `plan.md` 생성 → Review Agent 검토 → 사용자 승인
4. `tasks.md` 생성 → Review Agent 검토 → 사용자 승인
5. 구현 → Review Agent 검토 → 사용자 최종 승인

**VII. Slack-Based Confirmation**
모든 마일스톤 완료 시 2단계 승인 프로세스를 따릅니다:
1. **Review Agent 자동 리뷰**: `speckit.analyze.toml` 레시피를 통해 비판적 검토 수행
2. **사용자 컨펌 요청**: Review Agent가 APPROVED한 경우에만 Slack으로 사용자 승인 요청 전송
3. **승인/거부 처리**: 사용자 응답에 따라 다음 단계 진행 또는 수정 후 재리뷰

## 6. 거버넌스 (Governance)
**비준일 (Ratification Date):** 2026-02-09
**최종 개정일 (Last Amended):** 2026-02-09
**헌법 버전 (Constitution Version):** 1.1.0

**개정 절차 (Amendment Process)**
본 헌법의 개정은 프로젝트 참여자(사용자 및 에이전트)의 제안으로 시작되며, 변경 사항은 의미론적 버전 관리(Semantic Versioning) 규칙을 따릅니다.
- **MAJOR:** 기존 원칙의 삭제 또는 하위 호환되지 않는 변경.
- **MINOR:** 새로운 원칙 추가 또는 기존 원칙의 확장.
- **PATCH:** 문구 수정 및 명확화.

**준수 검토 (Compliance)**
모든 기획(Plan) 및 명세(Spec) 단계에서 본 헌법의 원칙 준수 여부를 확인해야 합니다(`Constitution Check`).
