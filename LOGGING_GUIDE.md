# Agent 로깅 시스템 사용 가이드

## 📋 로그 확인 방법

### 1. 실시간 로그 (콘솔)

서버 실행 시 콘솔에서 실시간으로 확인 가능:

```bash
python src/main.py

# 출력 예시:
# 2026-02-09 13:43:15 | workflow | INFO | 🎯 Spec 생성 시작 - Issue #1: 테스트 기능
# 2026-02-09 13:43:15 | workflow | DEBUG |   디렉토리 생성 중...
# 2026-02-09 13:43:15 | workflow | INFO |   📁 디렉토리: specs/1-테스트-기능
# 2026-02-09 13:43:15 | review | INFO | 📋 Spec 리뷰 시작: '테스트 기능'
# 2026-02-09 13:43:15 | review | DEBUG |   [체크 1/5] 길이 검사...
# 2026-02-09 13:43:15 | review | DEBUG |     ✓ 충분한 길이 (0.3점)
```

### 2. 로그 파일 (영구 저장)

#### 전체 로그
```
logs/workflow_YYYYMMDD.log
```
**용도**: 하루 동안의 모든 워크플로우 기록

**예시**:
```
2026-02-09 13:43:15 | workflow.999 | INFO | 🚀 워크플로우 시작
2026-02-09 13:43:15 | workflow.999 | INFO | Issue #999: 테스트 기능
2026-02-09 13:43:15 | review | DEBUG | [체크 1/5] 길이 검사...
```

#### Issue별 상세 로그
```
logs/issue_<번호>/workflow_<타임스탬프>.log
```
**용도**: 특정 Issue의 전체 과정 상세 기록

**예시**:
```
logs/issue_1/workflow_20260209_134315.log
logs/issue_2/workflow_20260209_140000.log
```

---

## 🔍 각 단계별 로그 내용

### 1. Workflow Orchestrator 로그

```
============================================================
🚀 워크플로우 시작
Issue #1: 테스트 기능 구현
작성자: testuser
============================================================
현재 단계: spec

📄 Step 1/4: Spec 생성
✅ Spec 생성 완료: specs/1-테스트-기능-구현/spec.md
📱 Slack 알림 전송: #dev-team
✅ Spec 리뷰 통과 (점수: 0.85)
🔄 자동으로 다음 단계 진행...
```

### 2. Stage Executor 로그

```
🎯 Spec 생성 시작 - Issue #1: 테스트 기능 구현
  디렉토리 생성 중...
  📁 디렉토리: specs/1-테스트-기능-구현
  🤖 Gemini CLI로 Spec 생성 시도...
  ⚠️ Gemini 생성 실패, 템플릿 사용
  📝 템플릿 기반 Spec 생성...
  ✅ 템플릿으로 생성 완료
  생성된 Spec 길이: 847 글자
  파일 저장 중...
  💾 Spec 파일: specs/1-테스트-기능-구현/spec.md
  🔍 Review Agent 검토 시작...
  ✅ 검토 완료: Approved
```

### 3. Review Agent 로그 (생각 과정!)

```
📋 Spec 리뷰 시작: '테스트 기능 구현'
Spec 길이: 847 글자
  [체크 1/5] 길이 검사...
    ✓ 충분한 길이 (0.3점)
  [체크 2/5] 필수 섹션 검사...
    ✓ 'Requirements' 섹션 발견 (0.2점)
    ✓ 'User Story' 섹션 발견 (0.2점)
    ✓ 'Success Criteria' 섹션 발견 (0.2점)
  발견된 섹션: Requirements, User Story, Success Criteria
  [체크 3/5] 구체성 검사...
    ✓ 구체적인 요구사항 포함 (0.15점)
  [체크 4/5] 테스트 시나리오 검사...
    ✓ Given-When-Then 시나리오 포함 (0.15점)
  [체크 5/5] Markdown 형식 검사...
    ✓ Markdown 헤더 사용 (0.1점)
  총점: 1.00/1.0
✅ 리뷰 통과 (점수: 1.00)
```

---

## 📂 로그 파일 구조

```
virtual_dev_team/
├── logs/
│   ├── workflow_20260209.log         # 오늘 전체 로그
│   ├── issue_1/
│   │   └── workflow_20260209_134315.log  # Issue #1 상세
│   ├── issue_2/
│   │   └── workflow_20260209_140000.log  # Issue #2 상세
│   └── issue_3/
│       └── workflow_20260209_141200.log  # Issue #3 상세
```

---

## 💡 사용 시나리오

### 시나리오 1: 전체 워크플로우 추적

```bash
# 테스트 실행
python test_full_workflow.py

# 로그 확인 (실시간)
# 콘솔에서 바로 확인 가능

# 또는 파일로 확인
type logs\workflow_20260209.log

# 특정 Issue만 확인
type logs\issue_2\workflow_*.log
```

### 시나리오 2: Review Agent 리뷰 과정 확인

```bash
# 로그에서 'review' 검색
findstr /C:"review" logs\workflow_20260209.log

# 출력:
# 📋 Spec 리뷰 시작
# [체크 1/5] 길이 검사...
# [체크 2/5] 필수 섹션 검사...
# ...
# ✅ 리뷰 통과
```

### 시나리오 3: 에러 추적

```bash
# ERROR 레벨만 확인
findstr /C:"ERROR" logs\workflow_20260209.log

# WARNING 포함
findstr /C:"WARNING" /C:"ERROR" logs\workflow_20260209.log
```

---

## 🎯 로그 레벨

| 레벨        | 용도               | 예시                  |
| ----------- | ------------------ | --------------------- |
| **DEBUG**   | 상세 진행 과정     | `디렉토리 생성 중...` |
| **INFO**    | 일반 정보          | `✅ Spec 생성 완료`    |
| **WARNING** | 경고 (동작은 계속) | `⚠️ Gemini 생성 실패`  |
| **ERROR**   | 오류 (작업 실패)   | `❌ Spec 생성 오류`    |

---

## 🔧 로그 설정 변경

### 더 상세한 로그 보기

`src/utils/logger.py`:
```python
# DEBUG 레벨로 변경 (기본: INFO)
main_logger = setup_logger("main", level=logging.DEBUG)
```

### 파일 저장 끄기

```python
logger = setup_logger("name", log_to_file=False)  # 콘솔만
```

---

## 📊 로그 분석 예시

### 각 단계 소요 시간 확인

```bash
# logs/issue_2/workflow_*.log 에서:
13:40:00 | 🚀 워크플로우 시작
13:40:02 | ✅ Spec 생성 완료        # 2초
13:40:05 | ✅ Plan 생성 완료        # 3초
13:40:08 | ✅ Tasks 생성 완료       # 3초

# 총 소요 시간: 8초
```

### Review Agent 평가 항목 확인

```
[체크 1/5] 길이 검사... ✓
[체크 2/5] 필수 섹션 검사... ✓ 3개
[체크 3/5] 구체성 검사... ✓
[체크 4/5] 테스트 시나리오 검사... ✗
[체크 5/5] Markdown 형식 검사... ✓

총점: 0.75/1.0
```

---

## 🚀 빠른 시작

### 1. 로깅 시스템 데모

```bash
python demo_logging.py
```

### 2. 실제 워크플로우 실행 및 로그 확인

```bash
# 서버 시작
python src/main.py

# 별도 터미널에서 테스트
python test_full_workflow.py

# 로그 확인
type logs\workflow_20260209.log
type logs\issue_2\workflow_*.log
```

### 3. 로그 파일 탐색

```powershell
# 모든 로그 파일 나열
Get-ChildItem logs -Recurse

# 최신 로그 보기
Get-Content logs\workflow_*.log -Tail 50

# 특정 Issue 로그 찾기
Get-ChildItem logs\issue_* -Recurse
```

---

## 💬 자주 묻는 질문

### Q: 로그가 너무 많아요
A: `src/utils/logger.py`에서 레벨을 `logging.INFO`로 설정 (DEBUG 줄임)

### Q: 로그 파일이 너무 커져요
A: 날짜별로 자동 분리되며, 오래된 파일은 수동 삭제 가능

### Q: 실시간으로만 보고 싶어요
A: `log_to_file=False` 설정

### Q: Gemini/Goose 로그도 있나요?
A: 있습니다! `gemini_logger`, `goose_logger` 사용 중

---

**이제 Agent들의 생각 과정을 모두 볼 수 있습니다!** 🎉
