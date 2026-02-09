"""
LLM 기반 Review Agent

Gemini를 사용한 고도의 문서 리뷰
"""
from typing import Optional
from dataclasses import dataclass
from pathlib import Path
import subprocess
import json


@dataclass
class ReviewResult:
    """리뷰 결과"""
    approved: bool
    comments: str
    score: float  # 0.0 ~ 1.0
    suggestions: list[str]  # 개선 제안
    issues: list[str]  # 발견된 문제
    
    @property
    def status(self) -> str:
        return "APPROVED" if self.approved else "REJECTED"


class LLMReviewAgent:
    """LLM 기반 Review Agent (Gemini 사용)"""
    
    def __init__(self, use_llm: bool = True, approval_threshold: float = 0.7):
        """
        Args:
            use_llm: LLM 사용 여부 (False면 Mock 모드)
            approval_threshold: 승인 기준 점수
        """
        self.use_llm = use_llm
        self.approval_threshold = approval_threshold
        self.gemini_available = self._check_gemini_cli()
        
        if use_llm and not self.gemini_available:
            print("⚠️ Gemini CLI 없음 - Mock 모드로 전환")
            self.use_llm = False
    
    def _check_gemini_cli(self) -> bool:
        """Gemini CLI 설치 확인"""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def review_spec(self, content: str, issue_title: str, issue_body: str = "") -> ReviewResult:
        """
        Spec 문서 리뷰
        
        Args:
            content: Spec 내용
            issue_title: Issue 제목
            issue_body: Issue 본문 (선택)
            
        Returns:
            ReviewResult
        """
        from utils.logger import review_logger
        
        review_logger.info(f"📋 Spec 리뷰 시작: '{issue_title}'")
        
        if self.use_llm and self.gemini_available:
            review_logger.info("  🤖 Gemini LLM으로 고급 리뷰 수행...")
            return self._llm_review_spec(content, issue_title, issue_body)
        else:
            review_logger.info("  📝 Mock 모드로 기본 검증 수행...")
            return self._mock_review_spec(content, issue_title)
    
    def _llm_review_spec(self, content: str, issue_title: str, issue_body: str) -> ReviewResult:
        """Gemini LLM으로 Spec 리뷰"""
        from utils.logger import review_logger
        
        # Gemini 프롬프트 생성
        prompt = f"""당신은 숙련된 소프트웨어 요구사항 분석가입니다.
다음 Feature Specification 문서를 검토하고 상세한 리뷰를 제공하세요.

## 원본 Issue
제목: {issue_title}
내용:
{issue_body if issue_body else "N/A"}

## 작성된 Spec
{content}

## 검토 항목
1. **완전성**: 모든 필수 섹션이 있는가? (User Stories, Requirements, Success Criteria)
2. **명확성**: 요구사항이 구체적이고 모호하지 않은가?
3. **테스트 가능성**: Acceptance Criteria가 측정 가능한가?
4. **일관성**: Issue의 요구사항과 Spec이 일치하는가?
5. **품질**: 전문적이고 구조화되어 있는가?

## 출력 형식 (JSON)
{{
    "score": 0.85,  // 0.0 ~ 1.0
    "approved": true,  // score >= 0.7
    "summary": "전반적으로 우수한 Spec입니다.",
    "issues": [
        "FR-002가 너무 모호합니다",
        "Success Criteria에 측정 방법이 없습니다"
    ],
    "suggestions": [
        "FR-002에 구체적인 응답 시간 기준 추가",
        "SC-001에 측정 도구 명시"
    ],
    "strengths": [
        "User Story가 Given-When-Then 형식으로 명확함",
        "요구사항이 구체적임"
    ]
}}
"""
        
        try:
            # Gemini CLI 호출
            review_logger.debug("  Gemini CLI 호출 중...")
            result = subprocess.run(
                ["gemini", "chat", "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                review_logger.warning(f"  Gemini 오류: {result.stderr}")
                return self._mock_review_spec(content, issue_title)
            
            # JSON 파싱
            output = result.stdout.strip()
            review_logger.debug(f"  Gemini 응답 길이: {len(output)}자")
            
            # JSON 추출 (마크다운 코드 블록 제거)
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0].strip()
            elif "```" in output:
                output = output.split("```")[1].split("```")[0].strip()
            
            data = json.loads(output)
            
            score = float(data.get("score", 0.5))
            approved = data.get("approved", score >= self.approval_threshold)
            issues = data.get("issues", [])
            suggestions = data.get("suggestions", [])
            strengths = data.get("strengths", [])
            
            review_logger.info(f"  Gemini 리뷰 완료 - 점수: {score:.2f}")
            review_logger.debug(f"  발견된 이슈: {len(issues)}개")
            review_logger.debug(f"  개선 제안: {len(suggestions)}개")
            
            # 코멘트 생성
            comments = f"""Gemini LLM 리뷰 결과:

점수: {score:.2f}/1.0
상태: {'✅ 승인' if approved else '❌ 거부'}

{data.get('summary', '')}

"""
            if strengths:
                comments += "\n**강점**:\n"
                for s in strengths:
                    comments += f"  ✓ {s}\n"
            
            if issues:
                comments += "\n**발견된 문제**:\n"
                for i in issues:
                    comments += f"  ⚠️ {i}\n"
            
            if suggestions:
                comments += "\n**개선 제안**:\n"
                for s in suggestions:
                    comments += f"  💡 {s}\n"
            
            return ReviewResult(
                approved=approved,
                score=score,
                comments=comments,
                suggestions=suggestions,
                issues=issues
            )
            
        except Exception as e:
            review_logger.error(f"  Gemini 리뷰 오류: {e}")
            return self._mock_review_spec(content, issue_title)
    
    def _mock_review_spec(self, content: str, issue_title: str) -> ReviewResult:
        """Mock 모드 Spec 리뷰 (키워드 체크)"""
        from utils.logger import review_logger
        
        review_logger.debug("  검증 항목 체크...")
        
        checks = {
            'has_user_stories': '## User Scenarios' in content or 'User Story' in content,
            'has_requirements': 'Requirements' in content or 'Functional Requirements' in content,
            'has_success_criteria': 'Success Criteria' in content,
            'min_length': len(content) > 500
        }
        
        issues = []
        suggestions = []
        
        for name, passed in checks.items():
            review_logger.debug(f"  [{name}]: {'✓' if passed else '✗'}")
            if not passed:
                if name == 'has_user_stories':
                    issues.append("User Stories 섹션이 없습니다")
                    suggestions.append("User Story를 Given-When-Then 형식으로 추가하세요")
                elif name == 'has_requirements':
                    issues.append("Requirements 섹션이 없습니다")
                    suggestions.append("Functional Requirements를 FR-001 형식으로 추가하세요")
                elif name == 'has_success_criteria':
                    issues.append("Success Criteria 섹션이 없습니다")
                    suggestions.append("측정 가능한 성공 기준을 추가하세요")
                elif name == 'min_length':
                    issues.append(f"문서가 너무 짧습니다 ({len(content)}자)")
                    suggestions.append("더 상세한 설명을 추가하세요")
        
        score = sum(checks.values()) / len(checks)
        approved = score >= self.approval_threshold
        
        review_logger.info(f"  총점: {score:.2f}/1.0")
        
        comments = f"""Mock 리뷰 결과:

점수: {score:.2f}/1.0
상태: {'✅ 승인' if approved else '❌ 거부'}

검증 항목: {sum(checks.values())}/{len(checks)} 통과
"""
        
        if issues:
            comments += "\n**발견된 문제**:\n"
            for i in issues:
                comments += f"  ⚠️ {i}\n"
        
        if suggestions:
            comments += "\n**개선 제안**:\n"
            for s in suggestions:
                comments += f"  💡 {s}\n"
        
        return ReviewResult(
            approved=approved,
            score=score,
            comments=comments,
            suggestions=suggestions,
            issues=issues
        )
