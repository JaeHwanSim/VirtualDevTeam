"""
Phase 1 승인 요청 테스트 스크립트
"""
import requests

# 테스트용 API 호출
url = "http://localhost:8000/api/send-approval"

data = {
    "channel": "#dev-team",  # 실제 채널명으로 변경
    "phase": "Phase 1: Constitution 업데이트",
    "title": "Review Agent 리뷰 완료 ✅",
    "description": (
        "*변경 내용:*\n"
        "• VI. Issue-Driven Workflow 원칙 추가\n"
        "• VII. Slack-Based Confirmation 원칙 추가\n"
        "• 버전 1.0.0 → 1.1.0 업그레이드\n\n"
        "사용자 승인을 기다립니다."
    ),
    "callback_id": "phase1_constitution_v1"
}

print("📤 승인 요청 메시지 전송 중...")
response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print(f"✅ 전송 성공!")
    print(f"   - Callback ID: {result['callback_id']}")
    print(f"   - Timestamp: {result['timestamp']}")
    print("\n📱 Slack에서 메시지를 확인하고 버튼을 클릭하세요.")
    print(f"\n🔍 승인 상태 확인: http://localhost:8000/api/approval-status/{result['callback_id']}")
else:
    print(f"❌ 전송 실패: {response.status_code}")
    print(f"   {response.text}")
