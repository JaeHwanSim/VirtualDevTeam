"""
로깅 시스템 데모

Agent들의 생각과 진행 과정을 확인하는 방법
"""
import sys
sys.path.insert(0, 'src')

from utils.logger import setup_detailed_logger, review_logger
from models.issue import GitHubIssue
from workflow.review_agent import ReviewAgent
from datetime import datetime

# 로거 설정
demo_logger = setup_detailed_logger("demo", issue_number=999)

print("\n" + "="*70)
print("Agent 로깅 시스템 데모")
print("="*70 + "\n")

# 1. 간단한 로그
demo_logger.info("🎯 데모 시작합니다")
demo_logger.debug("DEBUG 레벨 메시지 (상세 정보)")
demo_logger.info("INFO 레벨 메시지 (일반 정보)")
demo_logger.warning("WARNING 레벨 메시지 (경고)")

# 2. Review Agent 시뮬레이션
print("\n" + "-"*70)
print("Review Agent 리뷰 과정 시뮬레이션")
print("-"*70 + "\n")

spec_content = """
# Feature Specification: 테스트 기능

## User Scenarios & Testing

### User Story 1 - 로그인 (Priority: P1)

사용자가 로그인할 수 있어야 합니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 로그인 페이지에 있을 때, 
   **When** 이메일과 비밀번호를 입력하면, 
   **Then** 홈 페이지로 리다이렉트됩니다

## Requirements

### Functional Requirements

- **FR-001**: 이메일/비밀번호 인증
- **FR-002**: 세션 관리

## Success Criteria

### Measurable Outcomes

- **SC-001**: 로그인 성공률 95% 이상
- **SC-002**: 응답 시간 1초 이내
"""

agent = ReviewAgent(auto_approve=False)
result = agent.review_spec(spec_content, "테스트 기능")

print("\n" + "-"*70)
print("리뷰 결과:")
print("-"*70)
print(result.comments)

print("\n" + "="*70)
print("로그 파일 위치:")
print("="*70)
print("📁 logs/workflow_20260209.log  (전체 로그)")
print("📁 logs/issue_999/workflow_*.log  (Issue별 상세 로그)")
print("\n💡 실제 워크플로우 실행 시 자동으로 로그가 기록됩니다!")
