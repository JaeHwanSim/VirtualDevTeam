"""
Phase 2 Spec 승인 요청 알림
"""
import requests

webhook_url = "https://hooks.slack.com/services/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"

message = {
    "text": "📋 Phase 2: Spec 업데이트 완료",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📋 Phase 2: Spec 업데이트",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Review Agent 리뷰 완료* ✅\n\n*작성 내용:*\n• 4개 User Stories (P1-P4)\n• Functional Requirements (FR-001 ~ FR-007)\n• Success Criteria (SC-001 ~ SC-004)\n• Edge Cases 정의"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🔹 Antigravity 대화창에서 *'승인'* 또는 *'거부'*를 입력해주세요."
            }
        }
    ]
}

print("📤 Slack 알림 전송 중...")
response = requests.post(webhook_url, json=message)

if response.status_code == 200:
    print("✅ Slack 알림 전송 성공!")
    print("📱 Slack을 확인하고, Antigravity 대화창에서 '승인' 또는 '거부'를 입력하세요.")
else:
    print(f"❌ 전송 실패: {response.status_code}")
    print(f"   {response.text}")
