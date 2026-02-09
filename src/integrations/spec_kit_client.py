"""
Spec-kit Client

.gemini/commands/*.toml 파일에서 프롬프트를 읽고 
Gemini CLI를 통해 문서를 생성하는 클라이언트
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import tomllib
from models.issue import GitHubIssue


from agents.goose_agent_executor import GooseAgentExecutor

class SpecKitClient:
    """Spec-kit 기반 문서 생성 클라이언트"""
    
    def __init__(self, commands_dir: str = ".gemini/commands", goose_executor: Optional[GooseAgentExecutor] = None):
        """
        Args:
            commands_dir: TOML 파일이 있는 디렉토리
            goose_executor: Goose Agent Executor (Gemini CLI 대체용)
        """
        self.commands_dir = Path(commands_dir)
        self.goose_executor = goose_executor
    
    def _read_prompt_from_toml(self, command_name: str) -> Optional[str]:
        """
        TOML 파일에서 프롬프트 읽기
        
        Args:
            command_name: 명령어 이름 (예: "speckit.clarify")
            
        Returns:
            프롬프트 텍스트
        """
        toml_file = self.commands_dir / f"{command_name}.toml"
        if not toml_file.exists():
            print(f"⚠️ TOML 파일 없음: {toml_file}")
            return None
            
        try:
            with open(toml_file, "rb") as f:
                data = tomllib.load(f)
                return data.get("prompt")
        except Exception as e:
            print(f"⚠️ TOML 파싱 오류: {e}")
            return None
    
    def _call_gemini(self, prompt: str, model: str = "gemini-2.0-flash-exp") -> Optional[str]:
        """Gemini CLI 또는 Goose 호출"""
        # 1. Goose Executor 우선 사용
        if self.goose_executor and self.goose_executor.goose_available:
            print("🤖 Goose로 문서 생성 시도...")
            # 임의의 세션 이름 생성
            import time
            session_name = f"spec-kit-{int(time.time())}"
            
            result = self.goose_executor.execute_prompt(
                prompt=prompt,
                session_name=session_name,
                timeout=180
            )
            if result.get('success'):
                return result.get('output')
            else:
                print(f"⚠️ Goose 실행 실패: {result.get('error')}")
        
        # 2. Gemini CLI 시도 (Fallback)
        try:
            print("🤖 Gemini CLI로 문서 생성 시도...")
            result = subprocess.run(
                ["gemini", "chat", 
                 "--model", model,
                 "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"⚠️ Gemini 오류: {result.stderr}")
                return None
            
            return result.stdout.strip()
            
        except Exception as e:
            print(f"⚠️ Gemini 실행 오류: {e}")
            return None

    def generate_spec(self, issue: GitHubIssue) -> Optional[str]:
        """Spec 생성 (speckit.clarify 사용)"""
        prompt_template = self._read_prompt_from_toml("speckit.clarify")
        if not prompt_template:
            return None
            
        # 프롬프트 변수 치환
        prompt = prompt_template.replace("{issue_body}", f"{issue.title}\n\n{issue.body}")
        
        print("🤖 Spec-kit (speckit.clarify)로 Spec 생성 중...")
        return self._call_gemini(prompt)

    def generate_plan(self, spec_content: str) -> Optional[str]:
        """Plan 생성 (speckit.plan 사용)"""
        prompt_template = self._read_prompt_from_toml("speckit.plan")
        if not prompt_template:
            return None
            
        # 프롬프트 변수 치환
        prompt = prompt_template.replace("{spec}", spec_content)
        
        print("🤖 Spec-kit (speckit.plan)으로 Plan 생성 중...")
        return self._call_gemini(prompt)

    def generate_tasks(self, plan_content: str) -> Optional[str]:
        """Tasks 생성 (speckit.task 사용)"""
        prompt_template = self._read_prompt_from_toml("speckit.task")
        if not prompt_template:
            return None
            
        # 프롬프트 변수 치환
        prompt = prompt_template.replace("{plan}", plan_content)
        
        print("🤖 Spec-kit (speckit.task)로 Tasks 생성 중...")
        return self._call_gemini(prompt)
