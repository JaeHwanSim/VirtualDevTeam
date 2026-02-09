"""
Webhook 전용 - Phase 1 승인 요청 알림
"""
import requests

webhook_url = "https://hooks.slack.com/services/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"

message = {
    "text": "📋 Phase 1: Constitution 업데이트 완료",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📋 Phase 1: Constitution 업데이트",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Review Agent 리뷰 완료* ✅\n\n*변경 내용:*\n• VI. Issue-Driven Workflow 원칙 추가\n• VII. Slack-Based Confirmation 원칙 추가\n• 버전 1.0.0 → 1.1.0 업그레이드"
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
