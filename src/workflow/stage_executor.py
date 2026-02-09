"""
Stage Executor

각 워크플로우 단계(Spec, Plan, Tasks)를 실행하는 로직
"""
from pathlib import Path
from typing import Optional
from models.issue import GitHubIssue
from utils.file_manager import FileManager
from workflow.review_agent import ReviewAgent, ReviewResult


class StageExecutor:
    """워크플로우 단계 실행기"""
    
    def __init__(self, file_manager: FileManager, review_agent: ReviewAgent, gemini_client=None):
        """
        Args:
            file_manager: 파일 관리자
            review_agent: Review Agent
            gemini_client: Gemini Client (선택)
        """
        self.file_manager = file_manager
        self.review_agent = review_agent
        self.gemini_client = gemini_client
    
    def create_spec(self, issue: GitHubIssue) -> tuple[Optional[Path], Optional[ReviewResult]]:
        """
        Spec 생성
        
        Args:
            issue: GitHub Issue
            
        Returns:
            (spec 파일 경로, 리뷰 결과) 또는 (None, None)
        """
        try:
            # Issue 디렉토리 생성
            issue_dir = self.file_manager.create_issue_directory(
                issue.number, 
                issue.title
            )
            
            # Spec 내용 생성 (Gemini 우선, 템플릿은 fallback)
            spec_content = None
            if self.gemini_client:
                print("🤖 Gemini CLI로 Spec 생성 중...")
                spec_content = self.gemini_client.generate_spec(issue)
            
            if not spec_content:
                print("📝 템플릿으로 Spec 생성 중...")
                spec_content = self._generate_spec_content(issue)
            
            # Spec 파일 생성
            spec_path = self.file_manager.create_spec_file(issue_dir, spec_content)
            
            # Review Agent 리뷰
            review_result = self.review_agent.review_spec(spec_content, issue.title)
            
            return spec_path, review_result
            
        except Exception as e:
            print(f"Spec 생성 오류: {e}")
            return None, None
    
    def create_plan(self, issue_dir: Path, spec_path: Path) -> tuple[Optional[Path], Optional[ReviewResult]]:
        """
        Plan 생성
        
        Args:
            issue_dir: Issue 디렉토리
            spec_path: Spec 파일 경로
            
        Returns:
            (plan 파일 경로, 리뷰 결과) 또는 (None, None)
        """
        try:
            # Spec 읽기
            spec_content = self.file_manager.read_file(spec_path)
            if not spec_content:
                return None, None
            
            # Plan 내용 생성 (Gemini 우선, 템플릿은 fallback)
            plan_content = None
            if self.gemini_client:
                print("🤖 Gemini CLI로 Plan 생성 중...")
                issue_title = issue_dir.name.split('-', 1)[1] if '-' in issue_dir.name else "Feature"
                plan_content = self.gemini_client.generate_plan(spec_content, issue_title)
            
            if not plan_content:
                print("📝 템플릿으로 Plan 생성 중...")
                plan_content = self._generate_plan_content(spec_content)
            
            # Plan 파일 생성
            plan_path = self.file_manager.create_plan_file(issue_dir, plan_content)
            
            # Review Agent 리뷰
            review_result = self.review_agent.review_plan(plan_content, spec_content)
            
            return plan_path, review_result
            
        except Exception as e:
            print(f"Plan 생성 오류: {e}")
            return None, None
    
    def create_tasks(self, issue_dir: Path, plan_path: Path) -> tuple[Optional[Path], Optional[ReviewResult]]:
        """
        Tasks 생성
        
        Args:
            issue_dir: Issue 디렉토리
            plan_path: Plan 파일 경로
            
        Returns:
            (tasks 파일 경로, 리뷰 결과) 또는 (None, None)
        """
        try:
            # Plan 읽기
            plan_content = self.file_manager.read_file(plan_path)
            if not plan_content:
                return None, None
            
            # Spec도 읽기 (Gemini에 참고용)
            spec_path = issue_dir / "spec.md"
            spec_content = self.file_manager.read_file(spec_path) if spec_path.exists() else ""
            
            # Tasks 내용 생성 (Gemini 우선, 템플릿은 fallback)
            tasks_content = None
            if self.gemini_client:
                print("🤖 Gemini CLI로 Tasks 생성 중...")
                tasks_content = self.gemini_client.generate_tasks(plan_content, spec_content)
            
            if not tasks_content:
                print("📝 템플릿으로 Tasks 생성 중...")
                tasks_content = self._generate_tasks_content(plan_content)
            
            # Tasks 파일 생성
            tasks_path = self.file_manager.create_tasks_file(issue_dir, tasks_content)
            
            # Review Agent 리뷰
            review_result = self.review_agent.review_tasks(tasks_content, plan_content)
            
            return tasks_path, review_result
            
        except Exception as e:
            print(f"Tasks 생성 오류: {e}")
            return None, None
    
    def _generate_spec_content(self, issue: GitHubIssue) -> str:
        """
        Spec 내용 생성 (템플릿 기반)
        
        Args:
            issue: GitHub Issue
            
        Returns:
            Spec 내용
        """
        # 간단한 템플릿 기반 생성
        # 실제로는 Gemini CLI를 호출해야 함
        content = f"""# Feature Specification: {issue.title}

**Created**: {issue.created_at.strftime('%Y-%m-%d')}  
**Status**: Draft  
**Issue**: #{issue.number}

## User Scenarios & Testing

### User Story 1 - {issue.title} (Priority: P1)

{issue.body}

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

## Requirements

### Functional Requirements

- **FR-001**: [요구사항 1]
- **FR-002**: [요구사항 2]

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: [성공 기준 1]
- **SC-002**: [성공 기준 2]
"""
        return content
    
    def _generate_plan_content(self, spec_content: str) -> str:
        """
        Plan 내용 생성 (템플릿 기반)
        
        Args:
            spec_content: Spec 내용
            
        Returns:
            Plan 내용
        """
        # 간단한 템플릿 기반 생성
        content = f"""# Implementation Plan

**Date**: Generated from Spec

## Summary

[Spec에서 추출한 요약]

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: [의존성]  
**Testing**: pytest  

## Implementation Phases

### Phase 1: Setup

- [ ] 의존성 설치
- [ ] 프로젝트 구조 생성

### Phase 2: Implementation

- [ ] 핵심 기능 구현
- [ ] 테스트 작성

---

## Verification Plan

### Automated Tests

```bash
pytest tests/ -v
```
"""
        return content
    
    def _generate_tasks_content(self, plan_content: str) -> str:
        """
        Tasks 내용 생성 (템플릿 기반)
        
        Args:
            plan_content: Plan 내용
            
        Returns:
            Tasks 내용
        """
        # 간단한 템플릿 기반 생성
        content = f"""# Tasks

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
"""
        return content
