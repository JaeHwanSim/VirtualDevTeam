"""
Goose CLI Client

Goose CLI를 Python에서 호출하여 Tasks 자동 실행
"""
import subprocess
import re
from pathlib import Path
from typing import Optional, List, Dict


class GooseClient:
    """Goose CLI 클라이언트"""
    
    def __init__(self, project_root: str = "."):
        """
        Args:
            project_root: 프로젝트 루트 디렉토리
        """
        self.project_root = Path(project_root)
        
        # Goose CLI 설치 확인
        self.goose_available = self._check_goose_cli()
    
    def _check_goose_cli(self) -> bool:
        """Goose CLI 설치 여부 확인"""
        try:
            result = subprocess.run(
                ["goose", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️ Goose CLI not found. Tasks execution will be skipped.")
            return False
    
    def execute_tasks(self, tasks_path: Path, issue_number: int) -> Dict[str, any]:
        """
        Tasks 파일을 읽고 Goose로 실행
        
        Args:
            tasks_path: Tasks 파일 경로
            issue_number: Issue 번호
            
        Returns:
            실행 결과
        """
        if not self.goose_available:
            return {
                'status': 'skipped',
                'message': 'Goose CLI not available'
            }
        
        try:
            # Tasks 파싱
            tasks = self._parse_tasks(tasks_path)
            
            if not tasks:
                return {
                    'status': 'error',
                    'message': 'No tasks found'
                }
            
            print(f"📋 총 {len(tasks)}개 태스크 발견")
            
            # Goose 세션 생성
            session_name = f"issue-{issue_number}"
            
            # Tasks 실행
            results = []
            for i, task in enumerate(tasks, 1):
                print(f"\n🔨 Task {i}/{len(tasks)}: {task['description']}")
                
                result = self._run_goose_task(task, session_name)
                results.append(result)
                
                if not result['success']:
                    print(f"❌ Task 실패: {task['description']}")
                    return {
                        'status': 'failed',
                        'task': task['description'],
                        'results': results
                    }
                
                print(f"✅ Task 완료: {task['description']}")
            
            return {
                'status': 'success',
                'completed_tasks': len(results),
                'results': results
            }
            
        except Exception as e:
            print(f"Goose 실행 오류: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _parse_tasks(self, tasks_path: Path) -> List[Dict[str, str]]:
        """
        Tasks 파일 파싱
        
        Args:
            tasks_path: Tasks 파일 경로
            
        Returns:
            태스크 목록
        """
        try:
            content = tasks_path.read_text(encoding='utf-8')
            
            # 체크박스 형식의 태스크 추출
            # 예: - [ ] T001 프로젝트 구조 생성
            pattern = r'- \[ \] (T\d+)(.*?)(?=\n|$)'
            matches = re.findall(pattern, content, re.MULTILINE)
            
            tasks = []
            for task_id, description in matches:
                tasks.append({
                    'id': task_id.strip(),
                    'description': description.strip()
                })
            
            return tasks
            
        except Exception as e:
            print(f"Tasks 파싱 오류: {e}")
            return []
    
    def _run_goose_task(self, task: Dict[str, str], session_name: str) -> Dict[str, any]:
        """
        Goose로 단일 태스크 실행
        
        Args:
            task: 태스크 정보
            session_name: Goose 세션 이름
            
        Returns:
            실행 결과
        """
        try:
            # Goose 프롬프트 생성
            prompt = f"{task['id']}: {task['description']}"
            
            # Goose 실행
            # goose session start [session_name] --prompt [prompt]
            result = subprocess.run(
                ["goose", "session", "run", session_name, "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=300,  # 5분 타임아웃
                cwd=self.project_root
            )
            
            return {
                'success': result.returncode == 0,
                'task_id': task['id'],
                'output': result.stdout[:500] if result.stdout else '',  # 처음 500자만
                'error': result.stderr[:500] if result.stderr else ''
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'task_id': task['id'],
                'error': 'Timeout (5분 초과)'
            }
        except Exception as e:
            return {
                'success': False,
                'task_id': task['id'],
                'error': str(e)
            }
    
    def create_goose_session(self, session_name: str, context: str) -> bool:
        """
        Goose 세션 생성
        
        Args:
            session_name: 세션 이름
            context: 컨텍스트 (Spec, Plan 내용)
            
        Returns:
            성공 여부
        """
        if not self.goose_available:
            return False
        
        try:
            # Goose 세션 시작
            subprocess.run(
                ["goose", "session", "start", session_name],
                capture_output=True,
                timeout=10,
                cwd=self.project_root
            )
            
            return True
            
        except Exception as e:
            print(f"Goose 세션 생성 오류: {e}")
            return False
