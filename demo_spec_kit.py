"""
Spec-kit 통합 데모

Spec-kit TOML 프롬프트를 사용하여 문서를 생성하는 예제
"""
import sys
from pathlib import Path

# src 경로 추가
sys.path.insert(0, str(Path.cwd() / "src"))

from models.issue import GitHubIssue
from integrations.spec_kit_client import SpecKitClient

def main():
    print("\n" + "="*70)
    print("Spec-kit 통합 데모")
    print("="*70 + "\n")
    
    from agents.goose_agent_executor import GooseAgentExecutor
    
    # Goose Executor 초기화
    goose_executor = GooseAgentExecutor()
    
    # SpecKitClient 초기화 (Goose 연결)
    client = SpecKitClient(goose_executor=goose_executor)
    
    from datetime import datetime
    
    # 1. Spec 생성 테스트
    issue = GitHubIssue(
        number=999,
        title="사용자 프로필 이미지 업로드",
        body="사용자는 자신의 프로필 이미지를 업로드하고 변경할 수 있어야 한다. 이미지 크기는 5MB로 제한된다.",
        state="open",
        labels=["enhancement"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        url="http://github.com/demo/issue/999",
        author="demo-user"
    )
    
    print(f"📌 Issue: {issue.title}")
    print("-" * 50)
    
    spec_content = client.generate_spec(issue)
    
    if spec_content:
        print("\n✅ Spec 생성 성공!")
        print(f"길이: {len(spec_content)} 글자")
        print("내용 미리보기:")
        print(spec_content[:200] + "...\n")
    else:
        print("\n❌ Spec 생성 실패 (TOML 파일이 없거나 Gemini 오류)")
        return

    # 2. Plan 생성 테스트
    print("-" * 50)
    plan_content = client.generate_plan(spec_content)
    
    if plan_content:
        print("\n✅ Plan 생성 성공!")
        print(f"길이: {len(plan_content)} 글자")
        print("내용 미리보기:")
        print(plan_content[:200] + "...\n")
    else:
        print("\n❌ Plan 생성 실패")
        return

    # 3. Tasks 생성 테스트
    print("-" * 50)
    tasks_content = client.generate_tasks(plan_content)
    
    if tasks_content:
        print("\n✅ Tasks 생성 성공!")
        print(f"길이: {len(tasks_content)} 글자")
        print("내용 미리보기:")
        print(tasks_content[:200] + "...\n")
    else:
        print("\n❌ Tasks 생성 실패")

if __name__ == "__main__":
    main()
