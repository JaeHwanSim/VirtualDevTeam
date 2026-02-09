"""
Issue Data Model

GitHub Issue 데이터를 표현하는 모델
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class GitHubIssue:
    """GitHub Issue 데이터 모델"""
    
    number: int
    title: str
    body: str
    state: str  # 'open', 'closed'
    labels: List[str]
    created_at: datetime
    updated_at: datetime
    url: str
    author: str
    
    @classmethod
    def from_github_api(cls, issue_data: dict) -> 'GitHubIssue':
        """
        GitHub API 응답에서 GitHubIssue 인스턴스 생성
        
        Args:
            issue_data: GitHub API의 Issue 객체
            
        Returns:
            GitHubIssue 인스턴스
        """
        return cls(
            number=issue_data['number'],
            title=issue_data['title'],
            body=issue_data.get('body', ''),
            state=issue_data['state'],
            labels=[label['name'] for label in issue_data.get('labels', [])],
            created_at=datetime.fromisoformat(issue_data['created_at'].replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(issue_data['updated_at'].replace('Z', '+00:00')),
            url=issue_data['html_url'],
            author=issue_data['user']['login']
        )
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            'number': self.number,
            'title': self.title,
            'body': self.body,
            'state': self.state,
            'labels': self.labels,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'url': self.url,
            'author': self.author
        }
