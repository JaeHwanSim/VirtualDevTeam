"""
Goose 기반 Agent 실행기

Goose Session에 역할 프롬프트를 전달하여 모든 Agent 작업 처리
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import json
import tempfile


class GooseAgentExecutor:
    """Goose Session 기반 Agent 실행기"""
    
    def __init__(self, prompts_dir: str = "agents/prompts"):
        """
        Args:
            prompts_dir: Agent 프롬프트 디렉토리
        """
        self.prompts_dir = Path(prompts_dir)
        self.agents = {}
        self.goose_available = self._check_goose()
        
        if self.goose_available:
            self._load_agents()
    
    def _check_goose(self) -> bool:
        """Goose CLI 설치 확인"""
        try:
            result = subprocess.run(
                ["goose", "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print("✅ Goose CLI 활성화")
                return True
            else:
                print("⚠️ Goose CLI not found")
                return False
        except Exception as e:
            print(f"⚠️ Goose CLI check failed: {e}")
            return False
    
    def _load_agents(self):
        """모든 Agent 프롬프트 로드"""
        if not self.prompts_dir.exists():
            print(f"⚠️ Prompts 디렉토리 없음: {self.prompts_dir}")
            self.prompts_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for prompt_file in self.prompts_dir.glob("*.md"):
            agent_config = self._parse_agent_prompt(prompt_file)
            if agent_config:
                agent_name = agent_config['name']
                self.agents[agent_name] = agent_config
                print(f"✅ Agent 로드: {agent_name}")
    
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
                    # YAML 파싱 (수동)
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
            
            # frontmatter 없으면 전체를 프롬프트로
            return {
                'name': file_path.stem.replace('_', ' ').title(),
                'prompt_template': content,
                'file': str(file_path)
            }
            
        except Exception as e:
            print(f"⚠️ Agent 파싱 오류 ({file_path}): {e}")
            return None
    
    def execute_agent(self,
                     agent_name: str,
                     task: str,
                     context: Dict[str, Any],
                     issue_number: Optional[int] = None,
                     timeout: int = 120) -> Dict[str, Any]:
        """
        Agent 실행 (Goose Session 활용)
        
        Args:
            agent_name: Agent 이름 (예: "Review Agent")
            task: 수행할 작업
            context: 컨텍스트 데이터
            issue_number: Issue 번호 (선택)
            timeout: Timeout (초)
            
        Returns:
            실행 결과
        """
        from utils.logger import workflow_logger
        
        if not self.goose_available:
            workflow_logger.warning("⚠️ Goose CLI 미사용 - Fallback 필요")
            return {"error": "Goose CLI not available"}
        
        # Agent 로드
        if agent_name not in self.agents:
            available = list(self.agents.keys())
            workflow_logger.error(f"❌ Agent '{agent_name}' not found. Available: {available}")
            return {"error": f"Agent '{agent_name}' not found"}
        
        agent_config = self.agents[agent_name]
        workflow_logger.info(f"🤖 {agent_name} 실행 중...")
        
        # 역할 프롬프트 로드
        role_prompt = agent_config['prompt_template']
        
        # Session 이름 생성
        session_name = self._create_session_name(agent_name, issue_number)
        workflow_logger.debug(f"  Session: {session_name}")
        
        # Goose Session 실행
        try:
            result = self._run_goose_session(
                session_name=session_name,
                role_prompt=role_prompt,
                task=task,
                context=context,
                timeout=timeout
            )
            
            if result.get('success'):
                workflow_logger.info(f"✅ {agent_name} 완료")
            else:
                workflow_logger.error(f"❌ {agent_name} 실패: {result.get('error', 'Unknown')}")
            
            return result
            
        except Exception as e:
            workflow_logger.error(f"❌ {agent_name} 오류: {e}")
            return {"error": str(e)}
    
    def _create_session_name(self, agent_name: str, issue_number: Optional[int]) -> str:
        """Session 이름 생성"""
        base_name = agent_name.lower().replace(' ', '-')
        if issue_number:
            return f"{base_name}-issue-{issue_number}"
        else:
            import time
            return f"{base_name}-{int(time.time())}"
    
    def _run_goose_session(self,
                          session_name: str,
                          role_prompt: str,
                          task: str,
                          context: Dict[str, Any],
                          timeout: int = 120) -> Dict[str, Any]:
        """
        Goose Session 실행
        
        Goose에게 역할 프롬프트 + Task 전달
        """
        from utils.logger import workflow_logger
        
        # 전체 프롬프트 구성
        full_prompt = self._build_prompt(role_prompt, task, context)
        
        workflow_logger.debug(f"  프롬프트 길이: {len(full_prompt)} 글자")
        
        # 프롬프트를 임시 파일에 저장
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', 
                                         suffix='.md', delete=False) as f:
            f.write(full_prompt)
            prompt_file = f.name
        
        try:
            # Goose Session 실행
            workflow_logger.debug(f"  Goose 실행 중... (timeout: {timeout}s)")
            
            result = subprocess.run(
                ["goose", "session", "start", session_name,
                 "--plan", prompt_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(Path.cwd())
            )
            
            # 임시 파일 삭제
            Path(prompt_file).unlink(missing_ok=True)
            
            if result.returncode != 0:
                workflow_logger.warning(f"  Goose stderr: {result.stderr[:200]}")
                return {
                    "success": False,
                    "error": result.stderr,
                    "output": result.stdout
                }
            
            workflow_logger.debug(f"  Goose 출력 길이: {len(result.stdout)} 글자")
            
            return {
                "success": True,
                "output": result.stdout,
                "session": session_name
            }
            
        except subprocess.TimeoutExpired:
            workflow_logger.error(f"  ⏱️ Timeout ({timeout}초 초과)")
            Path(prompt_file).unlink(missing_ok=True)
            return {"success": False, "error": f"Timeout ({timeout}s)"}
        except Exception as e:
            workflow_logger.error(f"  ❌ 예외: {e}")
            Path(prompt_file).unlink(missing_ok=True)
            return {"success": False, "error": str(e)}
    
    def _build_prompt(self,
                     role_prompt: str,
                     task: str,
                     context: Dict[str, Any]) -> str:
        """프롬프트 구성"""
        # 컨텍스트 변수 치환
        prompt = role_prompt
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        
        # Task 추가
        full_prompt = f"""{prompt}

---

# Current Task

{task}

# Context Data

{self._format_context(context)}
"""
        return full_prompt
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """컨텍스트를 읽기 쉬운 형식으로 변환"""
        lines = []
        for key, value in context.items():
            lines.append(f"## {key}")
            lines.append("")
            
            # 파일 경로인 경우
            if isinstance(value, (str, Path)) and Path(str(value)).exists():
                lines.append(f"파일: `{value}`")
            else:
                lines.append(f"```")
                lines.append(str(value))
                lines.append(f"```")
            
            lines.append("")
        
        return "\n".join(lines)
    
    
    def execute_prompt(self,
                      prompt: str,
                      session_name: str = "custom-session",
                      timeout: int = 120) -> Dict[str, Any]:
        """
        직접 프롬프트 실행 (Agent 설정 없이)
        
        Args:
            prompt: 실행할 프롬프트
            session_name: 세션 이름
            timeout: Timeout
            
        Returns:
            실행 결과
        """
        from utils.logger import workflow_logger
        
        if not self.goose_available:
            return {"error": "Goose CLI not available"}
        
        try:
            workflow_logger.info(f"🤖 Goose 프롬프트 실행 중... (Session: {session_name})")
            result = self._run_goose_session(
                session_name=session_name,
                role_prompt="", # 역할 프롬프트 없음 (전체 프롬프트에 포함됨)
                task=prompt,
                context={}, # 컨텍스트 없음 (전체 프롬프트에 포함됨)
                timeout=timeout
            )
            
            if result.get('success'):
                workflow_logger.info("✅ Goose 실행 완료")
            else:
                workflow_logger.error(f"❌ Goose 실행 실패: {result.get('error', 'Unknown')}")
            
            return result
            
        except Exception as e:
            workflow_logger.error(f"❌ Goose 실행 오류: {e}")
            return {"error": str(e)}

    def list_agents(self) -> list[str]:
        """사용 가능한 Agent 목록"""
        return list(self.agents.keys())
    
    def reload_agents(self):
        """Agent 재로드"""
        self.agents.clear()
        if self.goose_available:
            self._load_agents()
