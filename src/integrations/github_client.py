"""
GitHub API Client

GitHub API와 통신하는 클라이언트
"""
import os
from typing import Optional, List
from github import Github, GithubException
from models.issue import GitHubIssue


class GitHubClient:
    """GitHub API 클라이언트"""
    
    def __init__(self, token: Optional[str] = None, repo_name: Optional[str] = None):
        """
        Args:
            token: GitHub Personal Access Token
            repo_name: 저장소 이름 (예: "owner/repo")
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name or os.getenv("GITHUB_REPO")
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN이 설정되지 않았습니다.")
        if not self.repo_name:
            raise ValueError("GITHUB_REPO가 설정되지 않았습니다.")
        
        self.github = Github(self.token)
        self.repo = self.github.get_repo(self.repo_name)
    
    def get_issue(self, issue_number: int) -> Optional[GitHubIssue]:
        """
        Issue 조회
        
        Args:
            issue_number: Issue 번호
            
        Returns:
            GitHubIssue 또는 None
        """
        try:
            issue = self.repo.get_issue(issue_number)
            return GitHubIssue.from_github_api(issue.raw_data)
        except GithubException as e:
            print(f"GitHub API 오류: {e}")
            return None
    
    def get_recent_issues(self, limit: int = 10) -> List[GitHubIssue]:
        """
        최근 Issue 목록 조회
        
        Args:
            limit: 최대 개수
            
        Returns:
            GitHubIssue 리스트
        """
        try:
            issues = self.repo.get_issues(state='open', sort='created', direction='desc')
            result = []
            for issue in issues[:limit]:
                if not issue.pull_request:  # Pull Request 제외
                    result.append(GitHubIssue.from_github_api(issue.raw_data))
            return result
        except GithubException as e:
            print(f"GitHub API 오류: {e}")
            return []
    
    def add_comment(self, issue_number: int, comment: str) -> bool:
        """
        Issue에 코멘트 추가
        
        Args:
            issue_number: Issue 번호
            comment: 코멘트 내용
            
        Returns:
            성공 여부
        """
        try:
            issue = self.repo.get_issue(issue_number)
            issue.create_comment(comment)
            return True
        except GithubException as e:
            print(f"GitHub API 오류: {e}")
            return False
    
    def add_label(self, issue_number: int, label: str) -> bool:
        """
        Issue에 라벨 추가
        
        Args:
            issue_number: Issue 번호
            label: 라벨 이름
            
        Returns:
            성공 여부
        """
        try:
            issue = self.repo.get_issue(issue_number)
            issue.add_to_labels(label)
            return True
        except GithubException as e:
            print(f"GitHub API 오류: {e}")
            return False
    
    def close_issue(self, issue_number: int) -> bool:
        """
        Issue 닫기
        
        Args:
            issue_number: Issue 번호
            
        Returns:
            성공 여부
        """
        try:
            issue = self.repo.get_issue(issue_number)
            issue.edit(state='closed')
            return True
        except GithubException as e:
            print(f"GitHub API 오류: {e}")
            return False
