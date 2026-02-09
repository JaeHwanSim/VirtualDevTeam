"""
Gemini CLI Client

Gemini CLI를 Python에서 호출하여 AI 문서 생성
"""
import subprocess
import os
from pathlib import Path
from typing import Optional
from models.issue import GitHubIssue


class GeminiClient:
    """Gemini CLI 클라이언트"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Args:
            prompts_dir: 프롬프트 템플릿 디렉토리
        """
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Gemini CLI 설치 확인
        self.gemini_available = self._check_gemini_cli()
    
    def _check_gemini_cli(self) -> bool:
        """Gemini CLI 설치 여부 확인"""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️ Gemini CLI not found. Using template fallback.")
            return False
    
    def generate_spec(self, issue: GitHubIssue) -> Optional[str]:
        """
        Issue → Spec 생성
        
        Args:
            issue: GitHub Issue
            
        Returns:
            생성된 Spec 내용 또는 None
        """
        if not self.gemini_available:
            return None
        
        # 프롬프트 생성
        prompt = self._create_spec_prompt(issue)
        
        # Gemini CLI 호출
        return self._call_gemini_cli(prompt)
    
    def generate_plan(self, spec_content: str, issue_title: str) -> Optional[str]:
        """
        Spec → Plan 생성
        
        Args:
            spec_content: Spec 내용
            issue_title: Issue 제목
            
        Returns:
            생성된 Plan 내용 또는 None
        """
        if not self.gemini_available:
            return None
        
        prompt = self._create_plan_prompt(spec_content, issue_title)
        return self._call_gemini_cli(prompt)
    
    def generate_tasks(self, plan_content: str, spec_content: str) -> Optional[str]:
        """
        Plan → Tasks 생성
        
        Args:
            plan_content: Plan 내용
            spec_content: Spec 내용 (참고용)
            
        Returns:
            생성된 Tasks 내용 또는 None
        """
        if not self.gemini_available:
            return None
        
        prompt = self._create_tasks_prompt(plan_content, spec_content)
        return self._call_gemini_cli(prompt)
    
    def _call_gemini_cli(self, prompt: str) -> Optional[str]:
        """
        Gemini CLI 호출
        
        Args:
            prompt: 프롬프트 내용
            
        Returns:
            Gemini 응답 또는 None
        """
        try:
            # Gemini CLI 실행
            result = subprocess.run(
                ["gemini", prompt],
                capture_output=True,
                text=True,
                timeout=60  # 1분 타임아웃
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Gemini CLI 오류: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("Gemini CLI 타임아웃")
            return None
        except Exception as e:
            print(f"Gemini CLI 호출 오류: {e}")
            return None
    
    def _create_spec_prompt(self, issue: GitHubIssue) -> str:
        """Spec 생성 프롬프트 생성"""
        template_path = self.prompts_dir / "spec_generation.md"
        
        if template_path.exists():
            template = template_path.read_text(encoding='utf-8')
            return template.format(
                issue_title=issue.title,
                issue_body=issue.body,
                issue_number=issue.number
            )
        
        # 기본 프롬프트
        return f"""당신은 소프트웨어 요구사항 분석가입니다.
다음 GitHub Issue를 기반으로 상세한 Feature Specification 문서를 작성하세요.

Issue #{issue.number}: {issue.title}
{issue.body}

출력 형식 (Markdown):
# Feature Specification: {issue.title}

**Created**: (현재 날짜)
**Status**: Draft
**Issue**: #{issue.number}

## User Scenarios & Testing

### User Story 1 - (제목) (Priority: P1)

(Issue 내용을 User Story 형식으로 변환)

**Acceptance Scenarios**:

1. **Given** [초기 상태], **When** [액션], **Then** [예상 결과]

---

## Requirements

### Functional Requirements

- **FR-001**: (요구사항 1)
- **FR-002**: (요구사항 2)

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: (성공 기준 1)
- **SC-002**: (성공 기준 2)
"""
    
    def _create_plan_prompt(self, spec_content: str, issue_title: str) -> str:
        """Plan 생성 프롬프트 생성"""
        template_path = self.prompts_dir / "plan_generation.md"
        
        if template_path.exists():
            template = template_path.read_text(encoding='utf-8')
            return template.format(
                spec_content=spec_content,
                issue_title=issue_title
            )
        
        return f"""당신은 소프트웨어 아키텍트입니다.
다음 Spec 문서를 기반으로 Implementation Plan을 작성하세요.

Spec 문서:
{spec_content}

출력 형식 (Markdown):
# Implementation Plan: {issue_title}

## Technical Context

**Language/Version**: (기술 스택)
**Primary Dependencies**: (주요 라이브러리)
**Testing**: (테스트 도구)

## Implementation Phases

### Phase 1: Setup
- [ ] 의존성 설치
- [ ] 프로젝트 구조 생성

### Phase 2: Core Implementation
- [ ] 핵심 기능 구현
- [ ] 테스트 작성

---

## Verification Plan

### Automated Tests
(테스트 명령어)

### Manual Testing
(수동 테스트 절차)
"""
    
    def _create_tasks_prompt(self, plan_content: str, spec_content: str) -> str:
        """Tasks 생성 프롬프트 생성"""
        template_path = self.prompts_dir / "tasks_generation.md"
        
        if template_path.exists():
            template = template_path.read_text(encoding='utf-8')
            return template.format(
                plan_content=plan_content,
                spec_content=spec_content
            )
        
        return f"""당신은 프로젝트 매니저입니다.
다음 Implementation Plan을 기반으로 상세한 Task 목록을 작성하세요.

Plan:
{plan_content}

출력 형식 (Markdown):
# Tasks

**Input**: plan.md

## Phase 1: Setup

- [ ] T001 프로젝트 구조 생성
- [ ] T002 의존성 설치

## Phase 2: Implementation

- [ ] T003 핵심 기능 구현
- [ ] T004 테스트 작성

## Phase 3: Verification

- [ ] T005 통합 테스트
- [ ] T006 문서 작성

---

## Dependencies & Execution Order

(의존성 및 실행 순서 설명)
"""
