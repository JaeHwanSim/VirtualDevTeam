# 즉시 적용 가이드

**목표**: 현재 시스템을 바로 실전 투입하기 위한 최소 작업

**예상 시간**: 30분 - 1시간

---

## Step 1: 환경 변수 설정 (10분)

### 1.1 `.env` 파일 업데이트

현재 상태 확인:
```bash
cat .env
```

**필수 추가 항목**:
```env
# GitHub (필수 - API 사용)
GITHUB_TOKEN=ghp_your_personal_access_token_here
GITHUB_REPO=your-username/your-repo-name

# Slack (선택 - 알림 받으려면)
SLACK_CHANNEL=#dev-team

# 기존 항목 유지
SLACK_BOT_TOKEN=...
SLACK_SIGNING_SECRET=...
SLACK_WEBHOOK_URL=...
```

### 1.2 GitHub Token 발급

1. https://github.com/settings/tokens 접속
2. "Generate new token" → "Classic"
3. 권한 선택:
   - ✅ `repo` (전체)
   - ✅ `read:org`
4. 생성된 토큰을 `.env`에 복사

---

## Step 2: 의존성 업데이트 (5분)

### 2.1 `requirements.txt`에 추가

```bash
# requirements.txt 마지막에 추가
requests==2.31.0
```

### 2.2 설치

```bash
pip install requests
```

---

## Step 3: 서버 재시작 및 테스트 (10분)

### 3.1 서버 종료 후 재시작

```bash
# 현재 서버 종료 (Ctrl+C)

# 재시작
python src/main.py
```

**확인 사항**:
```
✅ SlackBot 초기화 완료
✅ GitHubClient 초기화 완료  # ← GITHUB_TOKEN 설정 시
✅ 기본 컴포넌트 초기화 완료
✅ Gemini CLI 미사용 (템플릿 모드)  # ← 정상
✅ WorkflowOrchestrator 초기화 완료
```

### 3.2 전체 워크플로우 테스트

```bash
python test_full_workflow.py
```

**예상 결과**:
- Issue #2 생성
- Spec/Plan/Tasks 파일 3개 생성
- 서버 로그에 각 단계 진행 상황 표시

---

## Step 4: README 기본 작성 (10분)

`README.md` 업데이트:

```markdown
# Autonomous Development System

GitHub Issue에서 코드 구현까지 자동화

## Quick Start

1. 의존성 설치
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일 수정
```

3. 서버 시작
```bash
python src/main.py
```

4. 테스트
```bash
python test_full_workflow.py
```

## 환경 변수

| 변수              | 필수 | 설명                         |
| ----------------- | ---- | ---------------------------- |
| GITHUB_TOKEN      | ✅    | GitHub Personal Access Token |
| GITHUB_REPO       | ✅    | owner/repo 형식              |
| SLACK_BOT_TOKEN   | ⚠️    | Slack 알림용 (선택)          |
| SLACK_WEBHOOK_URL | ⚠️    | Slack 알림용 (선택)          |
| SLACK_CHANNEL     | ⚠️    | 기본 채널 (선택)             |

## 기능

- ✅ Issue → Spec 자동 생성
- ✅ Spec → Plan 자동 생성
- ✅ Plan → Tasks 자동 생성
- ✅ Gemini CLI 통합 (선택)
- ✅ Goose 통합 (선택)
- ✅ Slack 알림 (선택)

## 사용 방법

### 방법 1: 테스트 스크립트
```bash
python test_full_workflow.py
```

### 방법 2: API 직접 호출
```bash
curl -X POST http://localhost:8000/github/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: issues" \
  -d @sample_issue.json
```

## 트러블슈팅

### Q: "GitHubClient 초기화 실패"
A: `.env`에 `GITHUB_TOKEN` 설정 확인

### Q: Gemini/Goose 사용하고 싶음
A: 각 CLI 도구 설치 후 서버 재시작 (자동 감지)

### Q: Slack 알림이 안 옴
A: `SLACK_BOT_TOKEN`과 `SLACK_WEBHOOK_URL` 설정 확인

## 다음 단계

- [ ] Gemini CLI 설치 (AI 문서 생성)
- [ ] Goose 설치 (자동 구현)
- [ ] GitHub Webhook 설정
- [ ] 실제 프로젝트 적용
```

---

## Step 5: 실전 적용 (선택)

### 5.1 GitHub Webhook 설정 (ngrok 필요)

```bash
# ngrok 설치 (chocolatey)
choco install ngrok

# authtoken 설정
ngrok config add-authtoken YOUR_TOKEN

# ngrok 실행
ngrok http 8000
```

**GitHub 설정**:
1. Repository → Settings → Webhooks
2. Payload URL: `https://abc123.ngrok.io/github/webhook`
3. Content type: `application/json`
4. Events: Issues만 선택
5. Add webhook

### 5.2 실제 Issue로 테스트

1. GitHub에서 Issue 생성
2. 서버 로그 확인
3. `specs/` 디렉토리에 파일 생성 확인

---

## ✅ 완료 체크리스트

- [ ] `.env` 파일 완성 (GITHUB_TOKEN 추가)
- [ ] `requirements.txt`에 requests 추가
- [ ] 의존성 설치 (`pip install requests`)
- [ ] 서버 재시작 및 초기화 확인
- [ ] `test_full_workflow.py` 실행 성공
- [ ] README 기본 내용 작성
- [ ] (선택) GitHub Webhook 설정
- [ ] (선택) 실제 Issue로 테스트

---

**완료 시**: 시스템이 실전 투입 준비 완료! 🚀

**다음은**: `TODO.md` 참고하여 품질 개선
