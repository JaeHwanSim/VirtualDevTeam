# Prompt-Based Agent 시스템 설계

**철학**: Agent는 코드가 아니라 프롬프트다!

---

## 🎯 핵심 개념

### 기존 방식 (문제점)
```
src/agents/
├── pm_agent.py           # 200줄
├── ra_agent.py           # 250줄
├── review_agent.py       # 300줄
├── architect_agent.py    # 280줄
├── coder_agent.py        # 350줄
└── qa_agent.py           # 320줄

→ 총 1,700줄, 6개 파일
→ Agent 추가 시마다 코드 작성 필요
→ 유지보수 어려움
```

### 새로운 방식 (Prompt 기반)
```
agents/
├── prompts/
│   ├── pm_agent.md           # Agent 정의 (프롬프트)
│   ├── ra_agent.md           # Agent 정의
│   ├── review_agent.md       # Agent 정의
│   ├── architect_agent.md    # Agent 정의
│   ├── coder_agent.md        # Agent 정의
│   └── qa_agent.md           # Agent 정의
└── agent_executor.py         # 범용 실행기 (100줄)

→ Agent는 .md 파일로 정의
→ 하나의 실행기가 모든 Agent 처리
→ Agent 추가 = 프롬프트 파일 추가만
```

---

## 📋 Agent 프롬프트 형식

### 예시: `agents/prompts/review_agent.md`

```markdown
---
name: Review Agent
role: Requirements & Design Reviewer
version: 1.0
model: gemini-2.0-flash-exp
temperature: 0.3
---

# Role
당신은 숙련된 소프트웨어 요구사항 검토자입니다.

# Responsibilities
- Spec/Plan/Tasks 문서의 품질 검증
- 논리적 오류 및 모순 발견
- 구체적이고 실행 가능한 개선 제안
- 테스트 가능성 평가

# Review Criteria

## Spec 검토 시
1. **완전성**: 필수 섹션 존재 (User Stories, Requirements, Success Criteria)
2. **명확성**: 모호한 표현 없이 구체적
3. **테스트 가능성**: Acceptance Criteria가 측정 가능
4. **일관성**: Issue 요구사항과 일치
5. **품질**: 전문적이고 구조화됨

## Plan 검토 시
1. **기술적 타당성**: 선택한 기술 스택이 적절
2. **실행 가능성**: Phase가 현실적
3. **확장성**: 미래 변경에 대응 가능
4. **명확성**: 구현 방향이 명확

# Output Format (JSON)
{
    "score": 0.85,
    "approved": true,
    "summary": "전반적 평가",
    "issues": ["발견된 문제들"],
    "suggestions": ["개선 제안들"],
    "strengths": ["잘된 점들"]
}

# Examples

## Good Spec
- Given-When-Then 형식의 명확한 User Story
- 구체적인 FR-001 요구사항
- 측정 가능한 Success Criteria

## Bad Spec
- 모호한 표현 ("빠르게", "잘", "좋게")
- 측정 불가능한 기준
- 누락된 섹션
```

---

## 🔧 범용 Agent Executor

### `agents/agent_executor.py`

```python
"""
Prompt 기반 Agent 실행기

단일 실행기가 모든 Agent를 처리
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import json


class AgentExecutor:
    """범용 Agent 실행기"""
    
    def __init__(self, prompts_dir: str = "agents/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.agents = self._load_agents()
    
    def _load_agents(self) -> Dict[str, dict]:
        """모든 Agent 프롬프트 로드"""
        agents = {}
        for prompt_file in self.prompts_dir.glob("*.md"):
            agent_config = self._parse_agent_prompt(prompt_file)
            if agent_config:
                agents[agent_config['name']] = agent_config
        return agents
    
    def _parse_agent_prompt(self, file_path: Path) -> Optional[dict]:
        """Agent 프롬프트 파싱 (YAML frontmatter + 내용)"""
        content = file_path.read_text(encoding='utf-8')
        
        # YAML frontmatter 추출
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                prompt_content = parts[2].strip()
                
                return {
                    **frontmatter,
                    'prompt_template': prompt_content,
                    'file': str(file_path)
                }
        return None
    
    def execute_agent(self, 
                     agent_name: str, 
                     task: str, 
                     context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent 실행
        
        Args:
            agent_name: Agent 이름 (예: "Review Agent")
            task: 수행할 작업 설명
            context: 컨텍스트 데이터 (spec_content, issue_title 등)
            
        Returns:
            Agent 실행 결과
        """
        # Agent 로드
        agent_config = self.agents.get(agent_name)
        if not agent_config:
            raise ValueError(f"Agent '{agent_name}' not found")
        
        # 프롬프트 생성
        prompt = self._build_prompt(agent_config, task, context)
        
        # LLM 호출 (Gemini CLI)
        result = self._call_llm(
            prompt=prompt,
            model=agent_config.get('model', 'gemini-2.0-flash-exp'),
            temperature=agent_config.get('temperature', 0.7)
        )
        
        return result
    
    def _build_prompt(self, 
                     agent_config: dict, 
                     task: str, 
                     context: Dict[str, Any]) -> str:
        """프롬프트 구성"""
        prompt_template = agent_config['prompt_template']
        
        # 컨텍스트 변수 치환
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            if placeholder in prompt_template:
                prompt_template = prompt_template.replace(placeholder, str(value))
        
        # Task 추가
        full_prompt = f"""{prompt_template}

---

# Current Task
{task}
"""
        return full_prompt
    
    def _call_llm(self, 
                 prompt: str, 
                 model: str, 
                 temperature: float) -> Dict[str, Any]:
        """LLM 호출 (Gemini CLI)"""
        try:
            result = subprocess.run(
                ["gemini", "chat", 
                 "--model", model,
                 "--temperature", str(temperature),
                 "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {"error": result.stderr}
            
            # JSON 파싱 시도
            output = result.stdout.strip()
            
            # Markdown 코드 블록 제거
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0].strip()
            elif "```" in output:
                output = output.split("```")[1].split("```")[0].strip()
            
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                # JSON이 아니면 텍스트 그대로 반환
                return {"response": output}
                
        except Exception as e:
            return {"error": str(e)}


# 사용 예시
if __name__ == "__main__":
    executor = AgentExecutor()
    
    # Review Agent 실행
    result = executor.execute_agent(
        agent_name="Review Agent",
        task="다음 Spec을 검토하세요",
        context={
            "spec_content": "...",
            "issue_title": "사용자 로그인",
            "issue_body": "..."
        }
    )
    
    print(result)
```

---

## 🎯 장점

### 1. 확장성
```python
# Agent 추가 = 프롬프트 파일 추가만!
agents/prompts/deployment_agent.md  # 새로운 Agent
```

### 2. 유지보수
```markdown
# 프롬프트 수정만으로 Agent 행동 변경
agents/prompts/review_agent.md 편집
→ 코드 수정 없음!
```

### 3. 버전 관리
```markdown
---
name: Review Agent
version: 2.0  # 버전 업그레이드
changes:
  - 더 엄격한 검증 기준 추가
  - 보안 체크 추가
---
```

### 4. 협업
```markdown
# 각 팀원이 자신의 Agent 작성
agents/prompts/security_agent.md     # 보안팀
agents/prompts/performance_agent.md  # 성능팀
agents/prompts/ux_agent.md           # 디자인팀
```

---

## 📊 기존 vs 새로운 방식

### 기존 (코드 기반)
```python
# 새 Agent 추가
# 1. 파일 생성: src/agents/deployment_agent.py
# 2. 클래스 작성 (200줄)
# 3. 인터페이스 구현
# 4. 테스트 작성
# 5. main.py에 등록

→ 시간: 2-3시간
→ 코드: +200줄
```

### 새로운 (프롬프트 기반)
```markdown
# 새 Agent 추가
# 1. 파일 생성: agents/prompts/deployment_agent.md
# 2. 프롬프트 작성

→ 시간: 10-20분
→ 코드: 0줄
```

---

## 🚀 구현 계획

### Phase 1: Agent Executor 구현
```python
src/agents/
├── __init__.py
├── agent_executor.py    # 범용 실행기
└── prompts/
    ├── review_agent.md
    ├── ra_agent.md
    └── architect_agent.md
```

### Phase 2: 기존 Agent 마이그레이션
```bash
# 기존 코드 제거
rm src/workflow/review_agent.py

# 프롬프트로 대체
agents/prompts/review_agent.md 작성
```

### Phase 3: Orchestrator 통합
```python
# src/workflow/orchestrator.py
from agents.agent_executor import AgentExecutor

executor = AgentExecutor()

# Agent 실행
result = executor.execute_agent(
    "Review Agent",
    task="Spec 검토",
    context={"spec_content": content}
)
```

---

## 💡 고급 기능

### 1. Agent 체이닝
```python
# Agent → Agent 워크플로우
result1 = executor.execute_agent("RA Agent", ...)
result2 = executor.execute_agent("Review Agent", ..., 
                                context={"previous": result1})
```

### 2. Agent 협업
```python
# 여러 Agent가 동일 Task 검토
reviews = [
    executor.execute_agent("Review Agent", ...),
    executor.execute_agent("Security Agent", ...),
    executor.execute_agent("Performance Agent", ...)
]
# 다수결 또는 가중 평균
```

### 3. Dynamic Agent 로딩
```python
# 런타임에 새 Agent 발견 및 로드
executor.reload_agents()
```

---

## 🎯 다음 단계

1. **AgentExecutor 구현** (1시간)
2. **Review Agent 프롬프트 작성** (30분)
3. **기존 코드 마이그레이션** (1시간)
4. **테스트** (30분)

**지금 바로 시작할까요?**
