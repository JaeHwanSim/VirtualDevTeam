"""
전체 워크플로우 테스트 스크립트

GitHub Issue → Spec → Plan → Tasks 전체 자동 생성 테스트
"""
import requests
import json
import time

# FastAPI 서버 URL
BASE_URL = "http://localhost:8000"

def test_full_workflow():
    """전체 워크플로우 테스트 (Issue → Spec → Plan → Tasks)"""
    
    # 가상의 GitHub Issue Webhook 페이로드
    payload = {
        "action": "opened",
        "issue": {
            "number": 2,
            "title": "사용자 프로필 기능",
            "body": """
## 기능 설명
사용자가 자신의 프로필을 조회하고 수정할 수 있어야 합니다.

## 요구사항
- 프로필 조회 API
- 프로필 수정 API
- 프로필 사진 업로드

## 기술 스택
- FastAPI
- SQLAlchemy
- PostgreSQL
            """,
            "state": "open",
            "labels": [],
            "created_at": "2026-02-09T13:00:00Z",
            "updated_at": "2026-02-09T13:00:00Z",
            "html_url": "https://github.com/test/repo/issues/2",
            "user": {
                "login": "testuser"
            }
        }
    }
    
    headers = {
        "X-GitHub-Event": "issues",
        "Content-Type": "application/json"
    }
    
    print("=== 전체 워크플로우 테스트 ===\n")
    print(f"📤 Issue #{payload['issue']['number']}: {payload['issue']['title']}")
    print(f"   {payload['issue']['body'][:100]}...\n")
    
    # GitHub Webhook 전송
    print("1️⃣ Spec 생성 중...")
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
    
    # 잠시 대기 (처리 시간)
    print("\n⏳ 워크플로우 처리 중...\n")
    time.sleep(3)
    
    # 결과 확인
    issue_number = payload['issue']['number']
    print(f"📂 생성된 파일 확인:")
    print(f"   - specs/{issue_number}-사용자-프로필-기능/spec.md")
    print(f"   - specs/{issue_number}-사용자-프로필-기능/plan.md")
    print(f"   - specs/{issue_number}-사용자-프로필-기능/tasks.md")
    
    print("\n✅ 전체 워크플로우 테스트 완료!")
    print("\n💡 서버 로그를 확인하여 각 단계 진행 상황을 확인하세요.")
    
    return True


if __name__ == "__main__":
    test_full_workflow()
