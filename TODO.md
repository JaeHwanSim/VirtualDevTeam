# TODO - 개선 및 추가 사항

**Last Updated**: 2026-02-09

## 상태 요약

- ✅ **핵심 기능**: 100% 완료 (User Story 1-4)
- ⚠️ **프로덕션 준비**: 60%
- ⚠️ **문서화**: 70%
- ⚠️ **테스트**: 90%

---

## 🔴 우선순위 1 - 즉시 필요

### 1.1 환경 설정 완성

**현재 상태**: `.env` 파일 일부만 설정됨

**해야할 일**:
```bash
# .env 파일에 추가 필요
GITHUB_TOKEN=ghp_your_personal_access_token
GITHUB_REPO=your-username/your-repo
SLACK_CHANNEL=#dev-team
```

**작업 위치**: `.env`

**예상 시간**: 10분

---

### 1.2 README.md 작성

**현재 상태**: 기본 README만 있음

**해야할 일**:
- [ ] 프로젝트 소개
- [ ] 설치 방법
- [ ] 환경 변수 설명
- [ ] 사용 방법 (단계별 가이드)
- [ ] 예제 (스크린샷)
- [ ] 트러블슈팅

**작업 위치**: `README.md`

**예상 시간**: 1시간

**템플릿**:
```markdown
# Autonomous Development System

GitHub Issue → 자동 구현까지 완전 자동화

## Features
- Issue → Spec → Plan → Tasks → 구현
- Gemini CLI 통합 (AI 문서)
- Goose 통합 (자동 구현)
- Slack 알림

## Installation
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Configure environment variables
5. Run: `python src/main.py`

## Usage
...

## Configuration
...
```

---

### 1.3 의존성 추가

**현재 상태**: `requirements.txt`에 `requests` 누락

**해야할 일**:
```bash
# requirements.txt에 추가
requests==2.31.0
pytest==7.4.3  # 테스트용
```

**작업 위치**: `requirements.txt`

**예상 시간**: 5분

---

## 🟡 우선순위 2 - 품질 개선

### 2.1 단위 테스트 작성

**현재 상태**: 통합 테스트만 있음 (0개 단위 테스트)

**해야할 일**:
```python
# tests/test_github_client.py
- [ ] test_get_issue()
- [ ] test_add_comment()
- [ ] test_add_label()

# tests/test_file_manager.py
- [ ] test_create_issue_directory()
- [ ] test_create_spec_file()
- [ ] test_sanitize_filename()

# tests/test_stage_executor.py
- [ ] test_create_spec()
- [ ] test_create_plan()
- [ ] test_create_tasks()

# tests/test_orchestrator.py
- [ ] test_start_workflow()
- [ ] test_approve_and_continue()
```

**작업 위치**: `tests/` 디렉토리

**예상 시간**: 3-4시간

**시작 템플릿**:
```python
import pytest
from src.integrations.github_client import GitHubClient

def test_github_client_init():
    # Given
    client = GitHubClient()
    
    # When/Then
    assert client is not None
    # ...
```

---

### 2.2 로깅 시스템 추가

**현재 상태**: `print()` 문만 사용

**해야할 일**:
```python
# src/utils/logger.py 생성
import logging

def setup_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    # 콘솔 + 파일 핸들러
    return logger
```

**적용 위치**:
- `src/integrations/*.py` (모든 클라이언트)
- `src/workflow/*.py` (오케스트레이터, 실행기)
- `src/main.py`

**예상 시간**: 2시간

---

### 2.3 에러 핸들링 강화

**현재 상태**: 기본적인 try-except만

**해야할 일**:
- [ ] 커스텀 Exception 클래스
  ```python
  # src/exceptions.py
  class WorkflowError(Exception): pass
  class GitHubAPIError(Exception): pass
  class SlackAPIError(Exception): pass
  ```
- [ ] 재시도 로직 (GitHub/Slack API)
- [ ] Graceful degradation (Gemini/Goose 실패 시)

**작업 위치**: `src/exceptions.py` 생성 후 전체 코드에 적용

**예상 시간**: 2-3시간

---

### 2.4 WorkflowState 영구 저장

**현재 상태**: 메모리에만 저장 (서버 재시작 시 손실)

**해야할 일**:
```python
# Option 1: JSON 파일
- [ ] src/storage/json_storage.py
- [ ] .workflow_states/ 디렉토리에 저장

# Option 2: SQLite
- [ ] src/storage/db_storage.py
- [ ] workflow_states.db 생성
```

**작업 위치**: `src/storage/` 디렉토리 생성

**예상 시간**: 2-3시간

---

## 🟢 우선순위 3 - 사용성 개선

### 3.1 CLI 인터페이스

**현재 상태**: FastAPI 서버만

**해야할 일**:
```python
# cli.py 생성
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--issue', type=int)
    parser.add_argument('--approve', type=int)
    # ...
```

**명령어 예시**:
```bash
python cli.py --issue 123
python cli.py --approve 123
python cli.py --status 123
```

**작업 위치**: `cli.py`

**예상 시간**: 2-3시간

---

### 3.2 설정 파일 시스템

**현재 상태**: 하드코딩된 설정

**해야할 일**:
```yaml
# config.yaml 생성
workflow:
  auto_approve: false
  review_threshold: 0.7
  
gemini:
  enabled: true
  timeout: 60
  
goose:
  enabled: true
  timeout: 300

slack:
  notifications: true
  channel: "#dev-team"
```

**작업 위치**: `config.yaml` + `src/config.py`

**예상 시간**: 1-2시간

---

### 3.3 대시보드 (웹 UI)

**현재 상태**: API만 있음

**해야할 일**:
```html
<!-- templates/dashboard.html -->
- [ ] 워크플로우 상태 보기
- [ ] Issue 목록
- [ ] 승인/거부 버튼
- [ ] 로그 보기
```

**기술 스택**: 
- FastAPI + Jinja2 templates
- Bootstrap 5
- htmx (선택)

**작업 위치**: `templates/`, `static/`

**예상 시간**: 4-6시간

---

## 🔵 우선순위 4 - 확장 기능

### 4.1 Multi-Repository 지원

**현재 상태**: 단일 레포만 지원

**해야할 일**:
```python
# src/integrations/github_client.py 수정
class GitHubClient:
    def __init__(self, repo: str = None):
        # 여러 레포 관리
        self.repos = {}
        
    def add_repository(self, repo: str):
        # ...
```

**작업 위치**: `src/integrations/github_client.py`

**예상 시간**: 2-3시간

---

### 4.2 커스텀 Review Agent 플러그인

**현재 상태**: 고정된 Review Agent

**해야할 일**:
```python
# src/plugins/review_agents/
- [ ] base_agent.py (Abstract Base Class)
- [ ] simple_agent.py (현재 구현)
- [ ] llm_agent.py (Gemini로 리뷰)
- [ ] rule_based_agent.py (규칙 기반)
```

**작업 위치**: `src/plugins/review_agents/`

**예상 시간**: 3-4시간

---

### 4.3 Workflow 템플릿 시스템

**현재 상태**: 고정된 워크플로우

**해야할 일**:
```yaml
# templates/workflows/
- simple.yaml      # Issue → Spec만
- standard.yaml    # 현재 구현
- extended.yaml    # Spec → Design → Plan → Tasks
- custom.yaml      # 사용자 정의
```

**작업 위치**: `templates/workflows/`

**예상 시간**: 4-5시간

---

### 4.4 메트릭 & 모니터링

**현재 상태**: 메트릭 없음

**해야할 일**:
```python
# src/metrics/collector.py
- [ ] 워크플로우 완료 시간
- [ ] 각 단계별 소요 시간
- [ ] 승인/거부 비율
- [ ] Gemini/Goose 사용률
- [ ] 에러 발생 빈도
```

**출력 형식**:
- Prometheus 형식
- JSON 로그
- 대시보드 차트

**작업 위치**: `src/metrics/`

**예상 시간**: 3-4시간

---

## 📚 문서화

### 추가 필요 문서

- [ ] **CONTRIBUTING.md** - 기여 가이드
- [ ] **ARCHITECTURE.md** - 시스템 아키텍처 설명
- [ ] **API.md** - REST API 문서
- [ ] **DEPLOYMENT.md** - 배포 가이드
- [ ] **TROUBLESHOOTING.md** - 문제 해결 가이드

**예상 시간**: 2-3시간

---

## 🔧 DevOps

### CI/CD 파이프라인

**해야할 일**:
```yaml
# .github/workflows/test.yml
- [ ] 자동 테스트 (pytest)
- [ ] 린팅 (pylint, black)
- [ ] 타입 체크 (mypy)

# .github/workflows/deploy.yml
- [ ] Docker 이미지 빌드
- [ ] 자동 배포
```

**예상 시간**: 2-3시간

---

### Docker 컨테이너화

**해야할 일**:
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
```

**예상 시간**: 1-2시간

---

## 📊 작업 우선순위 요약

### 즉시 (1-2일)
1. ✅ 환경 설정 완성 (10분)
2. ✅ README 작성 (1시간)
3. ✅ 의존성 추가 (5분)

### 단기 (1주)
4. 단위 테스트 (3-4시간)
5. 로깅 시스템 (2시간)
6. 에러 핸들링 (2-3시간)

### 중기 (2주)
7. WorkflowState 영구 저장 (2-3시간)
8. CLI 인터페이스 (2-3시간)
9. 설정 파일 시스템 (1-2시간)

### 장기 (1개월+)
10. 대시보드 (4-6시간)
11. Multi-repo 지원 (2-3시간)
12. 플러그인 시스템 (3-4시간)

---

## 🎯 선택 가이드

### 개인 프로젝트용
- 우선순위 1만 완료 → 바로 사용 가능

### 팀 프로젝트용
- 우선순위 1-2 완료 → 안정적 사용

### 오픈소스/상용
- 우선순위 1-3 완료 → 프로덕션 준비

---

## 📝 체크리스트

매주 업데이트:

- [ ] 환경 설정 완성
- [ ] README 작성
- [ ] 의존성 추가
- [ ] 단위 테스트 50% 이상
- [ ] 로깅 시스템 적용
- [ ] 에러 핸들링 강화
- [ ] WorkflowState 영구 저장
- [ ] CLI 인터페이스
- [ ] 설정 파일 시스템
- [ ] 대시보드 v1.0

---

**참고**: 이 TODO는 지속적으로 업데이트됩니다.
