"""
Prompt 기반 Agent 시스템 데모

Agent Executor 사용 예시
"""
import sys
sys.path.insert(0, 'src')

from agents.agent_executor import AgentExecutor

print("\n" + "="*70)
print("Prompt 기반 Agent 시스템 데모")
print("="*70 + "\n")

# Agent Executor 초기화
print("📂 Agent Executor 초기화 중...")
executor = AgentExecutor()

# 사용 가능한 Agent 목록
print(f"\n사용 가능한 Agent: {executor.list_agents()}\n")

# 테스트 Spec
spec_content = """
# Feature Specification: 사용자 로그인

## User Scenarios & Testing

### User Story 1 - 로그인 (Priority: P1)

사용자가 이메일과 비밀번호로 로그인할 수 있어야 합니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 로그인 페이지에 있을 때,
   **When** 올바른 이메일과 비밀번호를 입력하면,
   **Then** 2초 이내에 대시보드로 리다이렉트된다

## Requirements

### Functional Requirements

- **FR-001**: 이메일 형식 검증 (RFC 5322)
- **FR-002**: 비밀번호 해싱 (bcrypt, cost=12)

## Success Criteria

### Measurable Outcomes

- **SC-001**: 로그인 성공률 95% 이상
- **SC-002**: 응답 시간 1.5초 이하
"""

print("-"*70)
print("Review Agent 실행")
print("-"*70 + "\n")

# Review Agent 실행 (Mock 모드)
result = executor.execute_agent(
    agent_name="Review Agent",
    task="다음 Spec을 검토하세요",
    context={
        "document_type": "spec",
        "content": spec_content,
        "issue_title": "사용자 로그인",
        "issue_body": "사용자가 로그인할 수 있어야 합니다"
    },
    use_llm=False  # Mock 모드
)

print("\n" + "="*70)
print("검토 결과")
print("="*70 + "\n")

print(f"점수: {result['score']:.2f}/1.0")
print(f"승인: {'✅ Yes' if result['approved'] else '❌ No'}")
print(f"\n요약: {result['summary']}\n")

if result.get('issues'):
    print("발견된 문제:")
    for issue in result['issues']:
        print(f"  ⚠️ {issue}")
    print()

if result.get('suggestions'):
    print("개선 제안:")
    for suggestion in result['suggestions']:
        print(f"  💡 {suggestion}")
    print()

if result.get('strengths'):
    print("강점:")
    for strength in result['strengths']:
        print(f"  ✓ {strength}")
    print()

print("="*70)
print("\n💡 LLM 모드 사용:")
print("   use_llm=True로 설정 + Gemini CLI 설치")
print("   → 고급 AI 검토 가능!\n")
