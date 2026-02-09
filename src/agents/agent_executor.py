"""
Prompt 기반 Agent 실행기

단일 실행기가 모든 Agent 프롬프트를 읽고 실행
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import json
import re


class AgentExecutor:
    """범용 Agent 실행기"""
    
    def __init__(self, prompts_dir: str = "agents/prompts"):
        """
        Args:
            prompts_dir: Agent 프롬프트 디렉토리
        """
        self.prompts_dir = Path(prompts_dir)
        self.agents = {}
        self._load_agents()
    
    def _load_agents(self):
        """모든 Agent 프롬프트 로드"""
        if not self.prompts_dir.exists():
            print(f"⚠️ Prompts 디렉토리 없음: {self.prompts_dir}")
            return
        
        for prompt_file in self.prompts_dir.glob("*.md"):
            agent_config = self._parse_agent_prompt(prompt_file)
            if agent_config:
                agent_name = agent_config['name']
                self.agents[agent_name] = agent_config
                print(f"✅ Agent 로드: {agent_name} (v{agent_config.get('version', '1.0')})")
    
    def _parse_agent_prompt(self, file_path: Path) -> Optional[dict]:
        """
        Agent 프롬프트 파싱 (YAML frontmatter + 프롬프트)
        
        Args:
            file_path: 프롬프트 파일 경로
            
        Returns:
            Agent 설정 딕셔너리
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # YAML frontmatter 추출
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    # YAML 파싱 (수동 - yaml 라이브러리 없이)
                    frontmatter_text = parts[1].strip()
                    frontmatter = {}
                    
                    for line in frontmatter_text.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # 타입 변환
                            if value.lower() == 'true':
                                value = True
                            elif value.lower() == 'false':
                                value = False
                            elif value.replace('.', '').isdigit():
                                value = float(value) if '.' in value else int(value)
                            
                            frontmatter[key] = value
                    
                    prompt_content = parts[2].strip()
                    
                    return {
                        **frontmatter,
                        'prompt_template': prompt_content,
                        'file': str(file_path)
                    }
            
            return None
            
        except Exception as e:
            print(f"⚠️ Agent 파싱 오류 ({file_path}): {e}")
            return None
    
    def execute_agent(self, 
                     agent_name: str, 
                     task: str, 
                     context: Dict[str, Any],
                     use_llm: bool = True) -> Dict[str, Any]:
        """
        Agent 실행
        
        Args:
            agent_name: Agent 이름
            task: 수행할 작업
            context: 컨텍스트 데이터
            use_llm: LLM 사용 여부 (False면 Mock)
            
        Returns:
            실행 결과
        """
        from utils.logger import review_logger
        
        # Agent 로드
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Available: {list(self.agents.keys())}")
        
        agent_config = self.agents[agent_name]
        review_logger.info(f"🤖 {agent_name} 실행 중...")
        
        # 프롬프트 생성
        prompt = self._build_prompt(agent_config, task, context)
        review_logger.debug(f"  프롬프트 길이: {len(prompt)} 글자")
        
        if not use_llm:
            review_logger.info("  📝 Mock 모드 (LLM 미사용)")
            return self._mock_execution(agent_config, context)
        
        # LLM 호출
        review_logger.debug(f"  모델: {agent_config.get('model', 'gemini-2.0-flash-exp')}")
        result = self._call_llm(
            prompt=prompt,
            model=agent_config.get('model', 'gemini-2.0-flash-exp'),
            temperature=agent_config.get('temperature', 0.7)
        )
        
        if 'error' in result:
            review_logger.error(f"  ❌ LLM 오류: {result['error']}")
            review_logger.info("  📝 Mock 모드로 대체...")
            return self._mock_execution(agent_config, context)
        
        review_logger.info(f"  ✅ {agent_name} 완료")
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

# Task
{task}

Context Data:
{json.dumps(context, indent=2, ensure_ascii=False)}
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
            
            # JSON 파싱
            output = result.stdout.strip()
            
            # Markdown 코드 블록 제거
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0].strip()
            elif "```" in output:
                output = output.split("```")[1].split("```")[0].strip()
            
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                # JSON이 아니면 텍스트로 반환
                return {"response": output}
                
        except subprocess.TimeoutExpired:
            return {"error": "Timeout (60초 초과)"}
        except FileNotFoundError:
            return {"error": "Gemini CLI not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def _mock_execution(self, agent_config: dict, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock 실행 (LLM 없이 기본 검증)
        
        Review Agent의 경우 간단한 키워드 체크
        """
        content = context.get('content', '')
        doc_type = context.get('document_type', 'spec')
        
        if agent_config['name'] == 'Review Agent':
            # 간단한 검증
            checks = {}
            
            if doc_type == 'spec':
                checks = {
                    'has_user_stories': 'User Story' in content,
                    'has_requirements': 'Requirements' in content,
                    'has_success_criteria': 'Success Criteria' in content,
                    'min_length': len(content) > 500
                }
            elif doc_type == 'plan':
                checks = {
                    'has_phases': 'Phase' in content,
                    'has_structure': 'Project Structure' in content or '구조' in content,
                    'has_verification': 'Verification' in content or 'Test' in content,
                    'min_length': len(content) > 800
                }
            
            score = sum(checks.values()) / len(checks) if checks else 0.5
            approved = score >= 0.7
            
            issues = [key for key, value in checks.items() if not value]
            
            return {
                "score": score,
                "approved": approved,
                "summary": f"Mock 검증 완료 ({sum(checks.values())}/{len(checks)} 통과)",
                "issues": [f"{issue} 미통과" for issue in issues] if issues else [],
                "suggestions": ["더 상세한 내용 추가" if not approved else "없음"],
                "strengths": [key for key, value in checks.items() if value]
            }
        
        # 다른 Agent는 기본 응답
        return {
            "response": f"{agent_config['name']} Mock 실행 완료",
            "status": "success"
        }
    
    def list_agents(self) -> list[str]:
        """사용 가능한 Agent 목록"""
        return list(self.agents.keys())
    
    def reload_agents(self):
        """Agent 재로드"""
        self.agents.clear()
        self._load_agents()
