"""
Review Agent 생각 과정 확인용 데모
"""
import sys
sys.path.insert(0, 'src')

from workflow.review_agent import ReviewAgent

print("\n" + "="*70)
print("Review Agent의 생각 과정 데모")
print("="*70 + "\n")

# 테스트용 Spec 내용
spec_content = """
# Feature Specification: 사용자 로그인

## User Scenarios & Testing

### User Story 1 - 로그인 (Priority: P1)

사용자가 이메일과 비밀번호로 로그인할 수 있어야 합니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 로그인 페이지에 있을 때,
   **When** 올바른 이메일과 비밀번호를 입력하면,
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

# Review Agent 생성
agent = ReviewAgent(auto_approve=False)

print("\n📝 Spec 내용:")
print(f"  - 길이: {len(spec_content)} 글자")
print(f"  - User Stories: {'✓' if 'User Story' in spec_content else '✗'}")
print(f"  - Requirements: {'✓' if 'Requirements' in spec_content else '✗'}")
print(f"  - Success Criteria: {'✓' if 'Success Criteria' in spec_content else '✗'}")

print("\n" + "-"*70)
print("Review Agent 검토 중...")
print("-"*70 + "\n")

# 리뷰 실행 (로그가 콘솔에 출력됨)
result = agent.review_spec(spec_content, "사용자 로그인")

print("\n" + "="*70)
print("최종 결과:")
print("="*70)
print(f"\n{result.comments}\n")
print(f"점수: {result.score:.2f}/1.0")
print(f"상태: {'✅ 승인' if result.approved else '❌ 거부'}")

print("\n" + "="*70)
print("로그 파일 위치:")
print("="*70)
print("📁 logs/workflow_20260209.log")
print("\n💡 위 파일에도 동일한 내용이 기록되어 있습니다!")
print("\n")
