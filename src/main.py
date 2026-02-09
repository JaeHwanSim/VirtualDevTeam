"""
FastAPI 서버 - Slack & GitHub Webhook Integration
"""
import json
import os
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# 프로젝트 모듈
from integrations.slack_bot import SlackBot
from integrations.github_client import GitHubClient
from integrations.gemini_client import GeminiClient
from integrations.spec_kit_client import SpecKitClient
from agents.goose_agent_executor import GooseAgentExecutor
from models.issue import GitHubIssue
from utils.file_manager import FileManager
from workflow.review_agent import ReviewAgent
from workflow.stage_executor import StageExecutor
from workflow.orchestrator import WorkflowOrchestrator

load_dotenv()

app = FastAPI(title="Virtual Dev Team - Autonomous Development System")

# 컴포넌트 초기화
bot = None
github_client = None
orchestrator = None

try:
    bot = SlackBot()
    print("✅ SlackBot 초기화 완료")
except Exception as e:
    print(f"⚠️ SlackBot 초기화 실패: {e}")

try:
    github_client = GitHubClient()
    print("✅ GitHubClient 초기화 완료")
except Exception as e:
    print(f"⚠️ GitHubClient 초기화 실패 (GitHub 기능 제한): {e}")

# FileManager, ReviewAgent, StageExecutor는 항상 생성 가능
file_manager = FileManager()
review_agent = ReviewAgent(auto_approve=False)
print("✅ 기본 컴포넌트 초기화 완료")

# Spec-kit Client 초기화
spec_kit_client = SpecKitClient()
print("✅ SpecKitClient 초기화 완료")

# Goose Agent Executor 초기화
goose_executor = GooseAgentExecutor()
if goose_executor.goose_available:
    print("✅ GooseAgentExecutor 초기화 완료 (Goose CLI 사용 가능)")
else:
    print("⚠️ GooseAgentExecutor 초기화 완료 (Goose CLI 미사용)")

# StageExecutor에 관련 클라이언트 전달
stage_executor = StageExecutor(
    file_manager=file_manager, 
    review_agent=review_agent, 
    spec_kit_client=spec_kit_client,
    goose_executor=goose_executor
)

# Orchestrator는 SlackBot이 있으면 생성
if bot:
    orchestrator = WorkflowOrchestrator(stage_executor, bot)
    print("✅ WorkflowOrchestrator 초기화 완료")
else:
    print("⚠️ WorkflowOrchestrator 초기화 실패 (SlackBot 필요)")

# 승인 상태 저장 (실제로는 DB나 파일로 저장)
approval_status: Dict[str, str] = {}


def on_approval_decision(callback_id: str) -> None:
    """승인/거부 콜백 핸들러"""
    def callback(action: str):
        approval_status[callback_id] = action
        print(f"[INFO] {callback_id}: {action}")
        
        # 여기에 추가 로직 (예: 다음 Phase 자동 시작)
        if action == "approved":
            print(f"[INFO] {callback_id} 승인됨 - 다음 단계 진행")
        else:
            print(f"[INFO] {callback_id} 거부됨 - 수정 필요")
    
    return callback


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "service": "Virtual Dev Team Slack Bot"}


@app.post("/slack/interactive")
async def slack_interactive(request: Request):
    """
    Slack Interactive Components Callback 엔드포인트
    """
    # 서명 검증
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    body = await request.body()
    
    if not bot.verify_signature(timestamp, body.decode("utf-8"), signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Payload 파싱 (form-urlencoded)
    form_data = await request.form()
    payload_str = form_data.get("payload")
    
    if not payload_str:
        raise HTTPException(status_code=400, detail="No payload")
    
    payload = json.loads(payload_str)
    
    # 이벤트 처리
    response = bot.handle_interaction(payload)
    
    return JSONResponse(content=response)


# Pydantic 모델 추가
from pydantic import BaseModel

class ApprovalRequest(BaseModel):
    channel: str
    phase: str
    title: str
    description: str
    callback_id: str


@app.post("/api/send-approval")
async def send_approval(request: ApprovalRequest):
    """
    승인 요청 메시지 전송 API
    
    Example:
        POST /api/send-approval
        {
            "channel": "#dev-team",
            "phase": "Phase 1: Constitution 업데이트",
            "title": "Review Agent 리뷰 완료",
            "description": "Constitution v1.1.0 업데이트 완료",
            "callback_id": "phase1_constitution"
        }
    """
    # 콜백 등록
    bot.register_approval_callback(request.callback_id, on_approval_decision(request.callback_id))
    
    # 메시지 전송
    ts = bot.send_approval_request(
        request.channel, 
        request.phase, 
        request.title, 
        request.description, 
        request.callback_id
    )
    
    if ts:
        return {"status": "sent", "timestamp": ts, "callback_id": request.callback_id}
    else:
        raise HTTPException(status_code=500, detail="Failed to send message")


@app.get("/api/approval-status/{callback_id}")
async def get_approval_status(callback_id: str):
    """승인 상태 조회"""
    status = approval_status.get(callback_id, "pending")
    return {"callback_id": callback_id, "status": status}


@app.post("/github/webhook")
async def github_webhook(request: Request):
    """
    GitHub Webhook 엔드포인트
    
    Issue 생성 이벤트를 수신하여 워크플로우 시작
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        # Webhook 페이로드 파싱
        payload = await request.json()
        
        # Issue 이벤트만 처리
        event_type = request.headers.get("X-GitHub-Event")
        if event_type != "issues":
            return {"status": "ignored", "reason": f"Not an issue event: {event_type}"}
        
        # Issue 생성 또는 라벨 추가 이벤트만 처리
        action = payload.get("action")
        if action not in ["opened", "labeled"]:
            return {"status": "ignored", "reason": f"Action '{action}' not handled"}
        
        # Issue 데이터 추출
        issue_data = payload.get("issue")
        if not issue_data:
            raise HTTPException(status_code=400, detail="No issue data in payload")
        
        # GitHubIssue 모델로 변환
        issue = GitHubIssue.from_github_api(issue_data)
        
        # 워크플로우 시작
        channel = os.getenv("SLACK_CHANNEL", "#dev-team")
        success = orchestrator.start_workflow(issue, channel)
        
        if success:
            return {
                "status": "success",
                "message": f"Workflow started for issue #{issue.number}",
                "issue_number": issue.number,
                "issue_title": issue.title
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to start workflow")
    
    except Exception as e:
        print(f"GitHub Webhook 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/approve/{issue_number}")
async def approve_issue(issue_number: int):
    """
    수동 승인 API (테스트용)
    
    Args:
        issue_number: Issue 번호
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    channel = os.getenv("SLACK_CHANNEL", "#dev-team")
    success = orchestrator.approve_and_continue(issue_number, channel)
    
    if success:
        return {"status": "approved", "issue_number": issue_number}
    else:
        raise HTTPException(status_code=404, detail=f"Workflow not found for issue #{issue_number}")


if __name__ == "__main__":
    print("🚀 FastAPI 서버 시작 - http://localhost:8000")
    print("📝 ngrok으로 터널링: ngrok http 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
