# Implementation Plan: 자율 개발 시스템

**Branch**: `001-autonomous-dev-system` | **Date**: 2026-02-09 | **Spec**: [spec.md](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/spec.md)

## Summary

GitHub Issue 기반의 자율 개발 워크플로우 시스템 구축. Issue 생성 시 자동으로 Constitution → Spec → Plan → Tasks → 구현 순서로 진행하며, 각 단계마다 Review Agent의 검토와 사용자 승인을 거칩니다. Python/FastAPI 기반으로 구현하며, Slack Webhook을 통해 알림을 전송합니다.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, GitHub API (PyGithub), Slack SDK, python-dotenv  
**Storage**: 파일 시스템 (specs/ 디렉토리에 markdown 파일)  
**Testing**: pytest  
**Target Platform**: Windows/Linux 서버  
**Project Type**: single (CLI + 백그라운드 서비스)  
**Performance Goals**: GitHub Issue 감지 후 5분 이내 Spec 생성  
**Constraints**: API Rate Limit 준수 (GitHub API: 5000 req/hour, Slack: 1 req/sec)  
**Scale/Scope**: 소규모 팀용 (동시 Issue 처리 최대 10개)

## Constitution Check

✅ **I. Specification-Driven Development (SDD)**: spec.md 생성 및 승인 후 구현 진행  
✅ **II. Multi-Agent Conflict & Synergy**: Review Agent 비판적 검토 프로세스 포함  
✅ **III. Human-in-the-Loop Milestones**: 각 단계마다 사용자 승인 대기  
✅ **IV. Hybrid Cost Control**: Gemini CLI 우선 사용 (구현 시 고려)  
✅ **V. Test-First Implementation**: pytest 기반 테스트 포함  
✅ **VI. Issue-Driven Workflow**: GitHub Issue 기반 워크플로우  
✅ **VII. Slack-Based Confirmation**: Slack 알림 및 승인 프로세스

## Project Structure

### Documentation (this feature)

```text
specs/autonomous-dev-system/
├── spec.md              # ✅ 완료
├── plan.md              # 이 파일
└── tasks.md             # 다음 단계에서 생성
```

### Source Code (repository root)

```text
src/
├── main.py                     # ✅ FastAPI 서버 (기존)
├── integrations/
│   ├── __init__.py            # ✅ 완료
│   ├── slack_bot.py           # ✅ Slack 연동 (기존)
│   └── github_client.py       # GitHub API 클라이언트
├── workflow/
│   ├── __init__.py
│   ├── orchestrator.py        # 워크플로우 오케스트레이터
│   ├── stage_executor.py      # 각 단계 실행 로직
│   └── review_agent.py        # Review Agent (Mock)
├── models/
│   ├── __init__.py
│   ├── issue.py               # GitHub Issue 모델
│   ├── workflow_state.py      # 워크플로우 상태 관리
│   └── approval.py            # 승인 요청 모델
└── utils/
    ├── __init__.py
    ├── file_manager.py        # 파일 생성/관리
    └── logger.py              # 로깅

tests/
├── test_github_client.py
├── test_orchestrator.py
└── test_workflow.py

.env                            # ✅ 환경 변수
requirements.txt                # ✅ 의존성
```

## Implementation Phases

### Phase 1: GitHub Issue 감지 및 Spec 생성 (User Story 1)

**목표**: GitHub Issue 생성 시 자동으로 `spec.md` 생성

**모듈**:
- `src/integrations/github_client.py`: GitHub API 연동
- `src/workflow/stage_executor.py`: Spec 생성 로직
- `src/models/issue.py`: Issue 데이터 모델

**구현 순서**:
1. GitHub Webhook 수신 엔드포인트 추가 (`/github/webhook`)
2. Issue 파싱 및 저장
3. Gemini CLI 호출하여 `spec.md` 생성 (또는 템플릿 기반)
4. Review Agent Mock 구현
5. Slack 알림 전송
6. 사용자 승인 대기 로직

---

### Phase 2: Spec → Plan 자동 생성 (User Story 2)

**목표**: Spec 승인 후 `plan.md` 자동 생성

**모듈**:
- `src/workflow/orchestrator.py`: 다음 단계 트리거
- Plan 생성 로직 추가

**구현 순서**:
1. 승인 후 다음 단계 트리거 메커니즘
2. Plan 생성 로직 (템플릿 기반)
3. Review Agent 리뷰
4. Slack 알림

---

### Phase 3: Plan → Tasks 자동 생성 (User Story 3)

**목표**: Plan 승인 후 `tasks.md` 자동 생성

**구현 순서**:
1. Tasks 생성 로직
2. 의존성 분석 (선택사항)
3. Review Agent 리뷰
4. Slack 알림

---

### Phase 4: Tasks → 구현 자동 실행 (User Story 4)

**목표**: Tasks 승인 후 Goose 세션 자동 시작

**구현 순서**:
1. Goose CLI 호출 로직
2. Tasks 파싱 및 순차 실행
3. pytest 실행 및 결과 리포트
4. Slack 알림

---

## API Endpoints

### GitHub Webhook

```
POST /github/webhook
Body: GitHub Webhook Payload (application/json)
```

### Slack Interactive (기존)

```
POST /slack/interactive
Body: Slack Interactive Components Payload (form-urlencoded)
```

### 승인 API (내부 사용)

```
POST /api/approve/{stage}
Body: { "approved": true/false, "comment": "..." }
```

---

## Dependencies

```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
slack-sdk==3.33.3
python-dotenv==1.0.1
python-multipart==0.0.12
PyGithub==2.4.0       # 새로 추가
requests==2.32.0
pytest==8.3.0         # 테스트용
```

---

## Verification Plan

### Automated Tests

```bash
# 단위 테스트
pytest tests/ -v

# 통합 테스트 (GitHub Mock + Slack Mock)
pytest tests/test_workflow.py -v
```

### Manual Verification

1. **GitHub Issue 생성 테스트**
   - GitHub에서 새 Issue 생성
   - `specs/[issue-number]-[title]/spec.md` 파일 확인
   - Slack 알림 수신 확인

2. **전체 워크플로우 테스트**
   - Issue 생성 → Spec → Plan → Tasks → 구현까지 전체 진행
   - 각 단계에서 승인/거부 테스트
   - Slack 알림 정상 수신 확인

3. **에러 시나리오 테스트**
   - GitHub API 실패 시나리오
   - Slack 전송 실패 시나리오
   - Review Agent REJECT 시나리오
