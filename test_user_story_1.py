"""
User Story 1 테스트 스크립트

GitHub Issue → Spec 자동 생성 워크플로우 테스트
"""
import requests
import json

# FastAPI 서버 URL
BASE_URL = "http://localhost:8000"

def test_github_webhook():
    """GitHub Webhook 시뮬레이션"""
    
    # 가상의 GitHub Issue Webhook 페이로드
    payload = {
        "action": "opened",
        "issue": {
            "number": 1,
            "title": "테스트 기능 구현",
            "body": "사용자가 로그인할 수 있어야 합니다.\n\n- 이메일/비밀번호 인증\n- 소셜 로그인 지원",
            "state": "open",
            "labels": [],
            "created_at": "2026-02-09T12:00:00Z",
            "updated_at": "2026-02-09T12:00:00Z",
            "html_url": "https://github.com/test/repo/issues/1",
            "user": {
                "login": "testuser"
            }
        }
    }
    
    headers = {
        "X-GitHub-Event": "issues",
        "Content-Type": "application/json"
    }
    
    print("📤 GitHub Webhook 이벤트 전송 중...")
    print(f"   Issue: #{payload['issue']['number']} - {payload['issue']['title']}")
    
    response = requests.post(
        f"{BASE_URL}/github/webhook",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 워크플로우 시작 성공!")
        print(f"   상태: {result['status']}")
        print(f"   메시지: {result['message']}")
        print(f"\n📂 생성된 파일을 확인하세요:")
        print(f"   specs/{payload['issue']['number']}-테스트-기능-구현/spec.md")
    else:
        print(f"❌ 오류 발생: {response.status_code}")
        print(f"   {response.text}")
    
    return response.status_code == 200


def test_manual_approval(issue_number: int):
    """수동 승인 테스트"""
    
    print(f"\n📋 Issue #{issue_number} 수동 승인 중...")
    
    response = requests.post(f"{BASE_URL}/api/approve/{issue_number}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 승인 성공!")
        print(f"   상태: {result['status']}")
    else:
        print(f"❌ 오류 발생: {response.status_code}")
        print(f"   {response.text}")
    
    return response.status_code == 200


if __name__ == "__main__":
    print("=== User Story 1 테스트 ===\n")
    
    # 1. GitHub Webhook 시뮬레이션
    if test_github_webhook():
        print("\n⏳ Slack 알림을 확인하고 승인하세요...")
        print("   또는 수동 승인 API를 사용하세요:")
        print("   python -c \"import test_user_story_1; test_user_story_1.test_manual_approval(1)\"")
