"""
File Manager Utility

파일 및 디렉토리 생성, 관리를 위한 유틸리티
"""
import os
from pathlib import Path
from typing import Optional


class FileManager:
    """파일 및 디렉토리 관리 유틸리티"""
    
    def __init__(self, base_dir: str = "specs"):
        """
        Args:
            base_dir: 기본 디렉토리 (specs/)
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_issue_directory(self, issue_number: int, issue_title: str) -> Path:
        """
        Issue용 디렉토리 생성
        
        Args:
            issue_number: Issue 번호
            issue_title: Issue 제목
            
        Returns:
            생성된 디렉토리 경로
        """
        # 제목을 파일명으로 사용 가능하게 변환
        safe_title = self._sanitize_filename(issue_title)
        dir_name = f"{issue_number}-{safe_title}"
        issue_dir = self.base_dir / dir_name
        issue_dir.mkdir(parents=True, exist_ok=True)
        return issue_dir
    
    def create_spec_file(self, issue_dir: Path, content: str) -> Path:
        """
        spec.md 파일 생성
        
        Args:
            issue_dir: Issue 디렉토리
            content: 파일 내용
            
        Returns:
            생성된 파일 경로
        """
        spec_path = issue_dir / "spec.md"
        spec_path.write_text(content, encoding='utf-8')
        return spec_path
    
    def create_plan_file(self, issue_dir: Path, content: str) -> Path:
        """
        plan.md 파일 생성
        
        Args:
            issue_dir: Issue 디렉토리
            content: 파일 내용
            
        Returns:
            생성된 파일 경로
        """
        plan_path = issue_dir / "plan.md"
        plan_path.write_text(content, encoding='utf-8')
        return plan_path
    
    def create_tasks_file(self, issue_dir: Path, content: str) -> Path:
        """
        tasks.md 파일 생성
        
        Args:
            issue_dir: Issue 디렉토리
            content: 파일 내용
            
        Returns:
            생성된 파일 경로
        """
        tasks_path = issue_dir / "tasks.md"
        tasks_path.write_text(content, encoding='utf-8')
        return tasks_path
    
    def read_file(self, file_path: Path) -> Optional[str]:
        """
        파일 읽기
        
        Args:
            file_path: 파일 경로
            
        Returns:
            파일 내용 (실패 시 None)
        """
        try:
            return file_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            return None
    
    def file_exists(self, file_path: Path) -> bool:
        """
        파일 존재 여부 확인
        
        Args:
            file_path: 파일 경로
            
        Returns:
            존재 여부
        """
        return file_path.exists() and file_path.is_file()
    
    def _sanitize_filename(self, filename: str, max_length: int = 50) -> str:
        """
        파일명으로 사용 가능하게 변환
        
        Args:
            filename: 원본 파일명
            max_length: 최대 길이
            
        Returns:
            변환된 파일명
        """
        # 특수 문자 제거 및 공백을 하이픈으로
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in filename)
        safe_name = safe_name.replace(' ', '-').lower()
        
        # 연속된 하이픈 제거
        while '--' in safe_name:
            safe_name = safe_name.replace('--', '-')
        
        # 길이 제한
        if len(safe_name) > max_length:
            safe_name = safe_name[:max_length]
        
        # 앞뒤 하이픈 제거
        return safe_name.strip('-')
