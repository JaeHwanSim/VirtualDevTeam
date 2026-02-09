# Virtual Dev Team - 자율 개발 시스템

**GitHub Issue 기반의 자율 개발 워크플로우 자동화 시스템**

Issue 생성만으로 Spec → Plan → Tasks → 구현까지 자동으로 진행되는 하이브리드 멀티 에이전트 시스템입니다.

---

## 개요

Virtual Dev Team은 다음과 같은 자율 개발 워크플로우를 제공합니다:

```
GitHub Issue 생성
    ↓
📄 Spec 자동 생성 (Gemini CLI)
    ↓ (Review Agent 검토 + 사용자 승인)
📋 Plan 자동 생성
    ↓ (Review Agent 검토 + 사용자 승인)
✓ Tasks 자동 생성
    ↓ (Review Agent 검토 + 사용자 승인)
🚀 구현 자동 실행 (Goose)
```

---

## 핵심 기능

- **Issue-Driven Workflow**: GitHub Issue 기반 자동화
- **Specification-Driven Development**: 문서 우선 개발
- **Multi-Agent System**: 
  - **Goose Manager** (명령 계층)
  - **Gemini CLI** (지능 계층)
  - **Spec-kit** (실행 계층)
- **Slack 연동**: 각 단계 알림 및 승인 요청
- **Human-in-the-Loop**: 주요 마일스톤에서 사용자 승인

---

## 프로젝트 구조

```
virtual_dev_team/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # 프로젝트 헌장 (v1.1.0)
│   └── templates/                   # Spec/Plan/Tasks 템플릿
├── specs/
│   └── autonomous-dev-system/       # 첫 번째 기능 Spec
│       ├── spec.md                  # 기능 명세
│       ├── plan.md                  # 구현 계획
│       └── tasks.md                 # 상세 태스크
├── src/
│   ├── main.py                      # FastAPI 서버
│   ├── integrations/
│   │   ├── github_client.py         # GitHub API
│   │   └── slack_bot.py             # Slack 연동
│   ├── workflow/
│   │   ├── orchestrator.py          # 워크플로우 오케스트레이터
│   │   ├── stage_executor.py        # 각 단계 실행
│   │   └── review_agent.py          # Review Agent
│   └── models/                      # 데이터 모델
├── tests/                           # 테스트
├── .env                             # 환경 변수
└── requirements.txt                 # Python 의존성
```

---

## 기술 스택

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Integrations**: 
  - GitHub API (PyGithub)
  - Slack Webhook
- **AI Agents**:
  - Gemini CLI (문서 생성)
  - Goose (코드 구현)
- **Testing**: pytest

---

## 시작하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```env
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
GITHUB_TOKEN=ghp_your_token
```

### 3. 서버 실행

```bash
python src/main.py
```

### 4. GitHub Webhook 설정

1. GitHub 저장소 Settings → Webhooks
2. Payload URL: `https://your-domain.com/github/webhook`
3. Content type: `application/json`
4. Events: Issues

---

## Constitution (v1.1.0)

프로젝트의 핵심 원칙:

1. **Specification-Driven Development (SDD)**: 문서 우선
2. **Multi-Agent Conflict & Synergy**: 비판적 검토
3. **Human-in-the-Loop Milestones**: 주요 지점 승인
4. **Hybrid Cost Control**: Gemini CLI 우선
5. **Test-First Implementation**: 테스트 우선
6. **Issue-Driven Workflow**: Issue 기반 자동화
7. **Slack-Based Confirmation**: 2단계 승인 프로세스

---

## 현재 상태

### ✅ Bootstrap 완료

- **Constitution** v1.1.0 업데이트
- **Spec** 작성 (4개 User Stories)
- **Plan** 작성 (4단계 구현 플랜)
- **Tasks** 작성 (28개 태스크)
- **Slack 연동** 기능 동작 확인

### 🚧 다음 단계

**Phase 2: Foundational** 구현 시작
- GitHub API 클라이언트
- 워크플로우 오케스트레이터
- Review Agent Mock

자세한 내용은 [tasks.md](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/tasks.md) 참조

---

## 문서

- [Constitution](file:///f:/work/virtual_dev_team/.specify/memory/constitution.md) - 프로젝트 헌장
- [Spec](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/spec.md) - 기능 명세
- [Plan](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/plan.md) - 구현 계획
- [Tasks](file:///f:/work/virtual_dev_team/specs/autonomous-dev-system/tasks.md) - 상세 태스크

---

## License

MIT
