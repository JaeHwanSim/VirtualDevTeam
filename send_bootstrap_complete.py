"""
Bootstrap 프로세스 완료 알림
"""
import requests

webhook_url = "https://hooks.slack.com/services/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"

message = {
    "text": "🎉 Bootstrap 프로세스 완료!",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🎉 자율 개발 시스템 Bootstrap 완료!",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*모든 Phase 완료* ✅\n\n✅ Phase 1: Constitution v1.1.0\n✅ Phase 2: Spec (4개 User Stories)\n✅ Phase 3: Plan (4단계 구현 플랜)\n✅ Phase 4: Tasks (28개 태스크)\n✅ Walkthrough & README 작성"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🚀 *다음 단계:* Phase 2 (Foundational) 구현 시작\n\n자세한 내용은 `tasks.md` 참조"
            }
        }
    ]
}

print("📤 Slack 완료 알림 전송 중...")
response = requests.post(webhook_url, json=message)

if response.status_code == 200:
    print("✅ Bootstrap 프로세스 완료 알림 전송 성공! 🎉")
    print("📱 Slack을 확인하세요.")
else:
    print(f"❌ 전송 실패: {response.status_code}")
    print(f"   {response.text}")
