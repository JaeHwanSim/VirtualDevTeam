# Goose 기반 Multi-Agent 시스템

**핵심**: Goose Session에 역할(Role) 프롬프트를 전달하여 다양한 Agent로 활용

---

## 🎯 개념

### 기존 오해 ❌
```python
# 각 Agent를 별도 구현
GeminiClient → Spec 생성
GooseClient → 코드만 생성
ReviewAgent → Python 코드로 구현
```

### 올바른 접근 ✅
```python
# Goose Session에 역할 부여
goose session start --role "Review Agent"  → Spec 검토
goose session start --role "RA Agent"      → Spec 작성
goose session start --role "Coder"         → 코드 생성
```

**모든 Agent = Goose + 역할 프롬프트!**

---

## 🔧 Goose Session 기반 Agent 시스템

### 아키텍처

```
agents/prompts/
├── review_agent.md     # 역할 정의
├── ra_agent.md         # 역할 정의
├── architect_agent.md  # 역할 정의
└── coder_agent.md      # 역할 정의

↓ (프롬프트 로드)

GooseAgentExecutor
  ├── Session: review-123    (Review Agent 역할)
  ├── Session: ra-456        (RA Agent 역할)
  ├── Session: architect-789 (Architect 역할)
  └── Session: coder-abc     (Coder 역할)
```

### 동작 방식

```bash
# 1. Review Agent로 Goose 실행
goose session start review-agent-issue-1 \
  --role "당신은 Review Agent입니다. Spec을 검토하세요."

# 2. RA Agent로 Goose 실행
goose session start ra-agent-issue-1 \
  --role "당신은 Requirements Analyst입니다. Spec을 작성하세요."

# 3. Coder로 Goose 실행
goose session start coder-issue-1 \
  --role "당신은 Python Coder입니다. Task를 구현하세요."
```

---

## 💻 구현

### GooseAgentExecutor

```python
"""
Goose 기반 Agent 실행기

Goose Session에 역할 프롬프트를 전달
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

class GooseAgentExecutor:
    """Goose Session 기반 Agent 실행기"""
    
    def __init__(self, prompts_dir: str = "agents/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.sessions = {}  # session_name -> session_id
        self._check_goose()
    
    def _check_goose(self):
        """Goose CLI 확인"""
        try:
            result = subprocess.run(
                ["goose", "--version"],
                capture_output=True,
                timeout=5
            )
            self.goose_available = result.returncode == 0
            if not self.goose_available:
                print("⚠️ Goose CLI not found")
        except:
            self.goose_available = False
            print("⚠️ Goose CLI not found")
    
    def execute_agent(self,
                     agent_name: str,
                     task: str,
                     context: Dict[str, Any],
                     issue_number: int) -> Dict[str, Any]:
        """
        Agent 실행 (Goose Session 활용)
        
        Args:
            agent_name: Agent 이름 (예: "Review Agent")
            task: 수행할 작업
            context: 컨텍스트 데이터
            issue_number: Issue 번호
        """
        if not self.goose_available:
            return {"error": "Goose CLI not available"}
        
        # 역할 프롬프트 로드
        role_prompt = self._load_role_prompt(agent_name)
        if not role_prompt:
            return {"error": f"Agent '{agent_name}' prompt not found"}
        
        # Session 이름 생성
        session_name = f"{agent_name.lower().replace(' ', '-')}-issue-{issue_number}"
        
        # Goose Session 시작 및 실행
        return self._run_goose_session(
            session_name=session_name,
            role_prompt=role_prompt,
            task=task,
            context=context
        )
    
    def _load_role_prompt(self, agent_name: str) -> Optional[str]:
        """역할 프롬프트 로드"""
        # agents/prompts/{agent_name}.md 파일 찾기
        filename = agent_name.lower().replace(' ', '_') + '.md'
        prompt_file = self.prompts_dir / filename
        
        if not prompt_file.exists():
            return None
        
        content = prompt_file.read_text(encoding='utf-8')
        
        # Frontmatter 제거하고 프롬프트만 추출
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
        
        return content
    
    def _run_goose_session(self,
                          session_name: str,
                          role_prompt: str,
                          task: str,
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Goose Session 실행
        
        Goose에게 역할 프롬프트 + Task 전달
        """
        # 전체 프롬프트 구성
        full_prompt = f"""
{role_prompt}

---

## Current Task
{task}

## Context
{self._format_context(context)}
"""
        
        try:
            # Goose Session 실행
            result = subprocess.run(
                ["goose", "session", "run", session_name, 
                 "--prompt", full_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                return {
                    "error": result.stderr,
                    "output": result.stdout
                }
            
            return {
                "success": True,
                "output": result.stdout,
                "session": session_name
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "Timeout (2분 초과)"}
        except Exception as e:
            return {"error": str(e)}
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """컨텍스트를 읽기 쉬운 형식으로 변환"""
        lines = []
        for key, value in context.items():
            lines.append(f"**{key}**:")
            lines.append(f"```")
            lines.append(str(value))
            lines.append(f"```")
            lines.append("")
        return "\n".join(lines)
```

---

## 📋 사용 예시

### 1. Review Agent로 Spec 검토

```python
executor = GooseAgentExecutor()

result = executor.execute_agent(
    agent_name="Review Agent",
    task="다음 Spec을 검토하고 피드백을 제공하세요",
    context={
        "spec_content": "...",
        "issue_title": "사용자 로그인"
    },
    issue_number=1
)

# Goose Session: review-agent-issue-1
# → agents/prompts/review_agent.md 역할 수행
```

### 2. RA Agent로 Spec 작성

```python
result = executor.execute_agent(
    agent_name="RA Agent",
    task="Issue를 분석하여 상세한 Spec을 작성하세요",
    context={
        "issue_title": "사용자 로그인",
        "issue_body": "..."
    },
    issue_number=1
)

# Goose Session: ra-agent-issue-1
# → agents/prompts/ra_agent.md 역할 수행
```

### 3. Coder Agent로 코드 구현

```python
result = executor.execute_agent(
    agent_name="Coder Agent",
    task="Tasks를 읽고 코드를 구현하세요",
    context={
        "tasks_file": "specs/1-login/tasks.md",
        "spec_file": "specs/1-login/spec.md"
    },
    issue_number=1
)

# Goose Session: coder-agent-issue-1
# → agents/prompts/coder_agent.md 역할 수행
```

---

## 🎯 전체 워크플로우

```
GitHub Issue #1
    ↓
┌─────────────────────────────────────┐
│ RA Agent (Goose Session)            │
│ → agents/prompts/ra_agent.md        │
│ → Spec 작성                          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Review Agent (Goose Session)        │
│ → agents/prompts/review_agent.md    │
│ → Spec 검토                          │
└─────────────────────────────────────┘
    ↓ (승인 시)
┌─────────────────────────────────────┐
│ Architect Agent (Goose Session)     │
│ → agents/prompts/architect_agent.md │
│ → Plan 작성                          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Coder Agent (Goose Session)         │
│ → agents/prompts/coder_agent.md     │
│ → 코드 구현                          │
└─────────────────────────────────────┘
```

**모든 Agent = Goose + 역할 프롬프트!**

---

## 💡 장점

1. **단일 LLM**: Goose만 사용 (Gemini 불필요)
2. **일관성**: 모든 Agent가 동일한 컨텍스트 유지 (Goose Session)
3. **협업**: Goose Session 간 파일 공유
4. **파일 조작**: Goose가 직접 파일 읽기/쓰기
5. **도구 사용**: Goose의 모든 도구 활용 가능

---

## 🔄 Gemini vs Goose

### Gemini Agent (기존)
```python
# API 호출만 가능
gemini.generate_spec(issue)
→ 텍스트 응답만 받음
→ 파일 저장은 Python 코드가 처리
```

### Goose Agent (새로운)
```python
# Goose가 직접 파일 조작
goose execute_agent("RA Agent", task="Spec 작성")
→ Goose가 직접 specs/1-login/spec.md 생성
→ 추가 도구 사용 가능 (git, 검색 등)
```

---

## 🚀 다음 단계

1. **GooseAgentExecutor 구현** (30분)
2. **Agent 프롬프트 작성** (각 10분)
   - ra_agent.md
   - architect_agent.md
   - coder_agent.md
3. **Orchestrator 통합** (30분)
4. **전체 워크플로우 테스트** (30분)

**지금 바로 구현할까요?**
