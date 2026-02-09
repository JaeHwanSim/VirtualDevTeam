"""
Review Agent Mock

문서 검토를 수행하는 Mock Review Agent
실제로는 Gemini CLI를 호출하지만, 여기서는 간단한 검증만 수행
"""
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class ReviewResult:
    """리뷰 결과"""
    approved: bool
    comments: str
    score: float  # 0.0 ~ 1.0
    
    @property
    def status(self) -> str:
        """승인 상태 문자열"""
        return "APPROVED" if self.approved else "REJECTED"


class ReviewAgent:
    """Review Agent Mock"""
    
    def __init__(self, auto_approve: bool = False):
        """
        Args:
            auto_approve: 자동 승인 여부 (테스트용)
        """
        self.auto_approve = auto_approve
    
    def review_spec(self, content: str, issue_title: str) -> ReviewResult:
        """
        Spec 문서 리뷰
        
        Args:
            content: spec.md 내용
            issue_title: Issue 제목
            
        Returns:
            ReviewResult
        """
        if self.auto_approve:
            return ReviewResult(
                approved=True,
                comments="자동 승인 모드",
                score=1.0
            )
        
        # 간단한 검증
        checks = {
            'has_user_stories': '## User Scenarios' in content or 'User Story' in content,
            'has_requirements': 'Requirements' in content or 'Functional Requirements' in content,
            'has_success_criteria': 'Success Criteria' in content,
            'min_length': len(content) > 500
        }
        
        score = sum(checks.values()) / len(checks)
        approved = score >= 0.75
        
        comments = self._generate_comments(checks, "Spec")
        
        return ReviewResult(
            approved=approved,
            comments=comments,
            score=score
        )
    
    def review_plan(self, content: str, spec_content: str) -> ReviewResult:
        """
        Plan 문서 리뷰
        
        Args:
            content: plan.md 내용
            spec_content: spec.md 내용 (참조용)
            
        Returns:
            ReviewResult
        """
        if self.auto_approve:
            return ReviewResult(
                approved=True,
                comments="자동 승인 모드",
                score=1.0
            )
        
        # 간단한 검증
        checks = {
            'has_technical_context': 'Technical Context' in content or '기술 스택' in content,
            'has_implementation_phases': 'Phase' in content or 'Implementation' in content,
            'has_project_structure': 'Project Structure' in content or '프로젝트 구조' in content,
            'has_verification': 'Verification' in content or 'Test' in content or '검증' in content,
            'min_length': len(content) > 800
        }
        
        score = sum(checks.values()) / len(checks)
        approved = score >= 0.75
        
        comments = self._generate_comments(checks, "Plan")
        
        return ReviewResult(
            approved=approved,
            comments=comments,
            score=score
        )
    
    def review_tasks(self, content: str, plan_content: str) -> ReviewResult:
        """
        Tasks 문서 리뷰
        
        Args:
            content: tasks.md 내용
            plan_content: plan.md 내용 (참조용)
            
        Returns:
            ReviewResult
        """
        if self.auto_approve:
            return ReviewResult(
                approved=True,
                comments="자동 승인 모드",
                score=1.0
            )
        
        # 간단한 검증
        checks = {
            'has_phases': 'Phase' in content,
            'has_task_ids': '- [ ]' in content or '- [x]' in content,
            'has_dependencies': 'Dependencies' in content or '의존성' in content,
            'has_checkpoints': 'Checkpoint' in content or 'checkpoint' in content,
            'min_length': len(content) > 1000
        }
        
        score = sum(checks.values()) / len(checks)
        approved = score >= 0.75
        
        comments = self._generate_comments(checks, "Tasks")
        
        return ReviewResult(
            approved=approved,
            comments=comments,
            score=score
        )
    
    def _generate_comments(self, checks: Dict[str, bool], doc_type: str) -> str:
        """
        검증 결과를 기반으로 코멘트 생성
        
        Args:
            checks: 검증 항목 및 결과
            doc_type: 문서 타입
            
        Returns:
            코멘트 문자열
        """
        passed = [key for key, value in checks.items() if value]
        failed = [key for key, value in checks.items() if not value]
        
        comments = f"{doc_type} 리뷰 결과:\n\n"
        comments += f"✅ 통과 ({len(passed)}/{len(checks)}):\n"
        for item in passed:
            comments += f"  - {item}\n"
        
        if failed:
            comments += f"\n❌ 미통과:\n"
            for item in failed:
                comments += f"  - {item}\n"
        
        return comments
