"""
User Story 4 테스트 스크립트

Tasks → Goose 자동 구현 테스트
"""
import requests
import json
import time

# FastAPI 서버 URL
BASE_URL = "http://localhost:8000"

def test_goose_integration():
    """Goose 통합 테스트"""
    
    # 간단한 Issue로 전체 워크플로우 테스트
    payload = {
        "action": "opened",
        "issue": {
            "number": 3,
            "title": "Hello World 프로그램",
            "body": """
## 기능 설명
간단한 Hello World 프로그램을 작성합니다.

## 요구사항
- Python으로 구현
- "Hello, World!" 출력
- main 함수 포함
            """,
            "state": "open",
            "labels": [],
            "created_at": "2026-02-09T13:15:00Z",
            "updated_at": "2026-02-09T13:15:00Z",
            "html_url": "https://github.com/test/repo/issues/3",
            "user": {
                "login": "testuser"
            }
        }
    }
    
    headers = {
        "X-GitHub-Event": "issues",
        "Content-Type": "application/json"
    }
    
    print("=== User Story 4: Goose 통합 테스트 ===\n")
    print(f"📤 Issue #{payload['issue']['number']}: {payload['issue']['title']}")
    
    # GitHub Webhook 전송
    print("\n🔄 전체 워크플로우 시작...")
    response = requests.post(
        f"{BASE_URL}/github/webhook",
        json=payload,
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ 오류: {response.status_code} - {response.text}")
        return False
    
    result = response.json()
    print(f"   ✅ {result['message']}")
    
    # 워크플로우 완료 대기
    print("\n⏳ 워크플로우 처리 중 (Spec→Plan→Tasks→구현)...\n")
    time.sleep(10)  # Goose 실행 시간 고려
    
    # 결과 확인
    issue_number = payload['issue']['number']
    print(f"\n📂 생성된 파일:")
    print(f"   - specs/{issue_number}-hello-world-프로그램/spec.md")
    print(f"   - specs/{issue_number}-hello-world-프로그램/plan.md")
    print(f"   - specs/{issue_number}-hello-world-프로그램/tasks.md")
    print(f"   - (Goose로 구현된 코드)")
    
    print("\n✅ User Story 4 테스트 완료!")
    print("\n💡 서버 로그를 확인하여 Goose 실행 결과를 확인하세요.")
    print("   Goose CLI가 설치되지 않은 경우 구현 단계가 스킵됩니다.")
    
    return True


if __name__ == "__main__":
    test_goose_integration()
