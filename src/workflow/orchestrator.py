"""
Workflow Orchestrator

전체 워크플로우를 조율하는 오케스트레이터
"""
from typing import Optional
from pathlib import Path
from models.issue import GitHubIssue
from models.workflow_state import WorkflowState, WorkflowStage, ApprovalStatus
from workflow.stage_executor import StageExecutor
from integrations.slack_bot import SlackBot


class WorkflowOrchestrator:
    """워크플로우 오케스트레이터"""
    
    def __init__(self, stage_executor: StageExecutor, slack_bot: SlackBot):
        """
        Args:
            stage_executor: 단계 실행기
            slack_bot: Slack Bot
        """
        self.stage_executor = stage_executor
        self.slack_bot = slack_bot
        self.workflow_states = {}  # issue_number -> WorkflowState
    
    def start_workflow(self, issue: GitHubIssue, channel: str = "#dev-team") -> bool:
        """
        워크플로우 시작 (Issue → Spec)
        
        Args:
            issue: GitHub Issue
            channel: Slack 채널
            
        Returns:
            성공 여부
        """
        try:
            # 워크플로우 상태 초기화
            state = WorkflowState(
                issue_number=issue.number,
                current_stage=WorkflowStage.SPEC
            )
            self.workflow_states[issue.number] = state
            
            # Spec 생성
            spec_path, review_result = self.stage_executor.create_spec(issue)
            
            if not spec_path or not review_result:
                state.reject("Spec 생성 실패")
                return False
            
            state.spec_path = str(spec_path)
            
            # Slack 알림 전송
            message = self._create_approval_message(
                stage="Spec",
                issue=issue,
                review_result=review_result,
                file_path=spec_path
            )
            
            self.slack_bot.send_message(channel, message)
            
            # 자동 승인 모드인 경우 다음 단계로
            if review_result.approved:
                print(f"✅ Spec 리뷰 통과 (#{issue.number})")
                # 자동으로 Plan 생성 진행
                print(f"🔄 Plan 단계 자동 시작 (#{issue.number})")
                self.approve_and_continue(issue.number, channel)
            else:
                print(f"❌ Spec 리뷰 실패 (#{issue.number})")
                state.reject(review_result.comments)
            
            return True
            
        except Exception as e:
            print(f"워크플로우 시작 오류: {e}")
            return False
    
    def approve_and_continue(self, issue_number: int, channel: str = "#dev-team") -> bool:
        """
        현재 단계 승인 및 다음 단계 진행
        
        Args:
            issue_number: Issue 번호
            channel: Slack 채널
            
        Returns:
            성공 여부
        """
        state = self.workflow_states.get(issue_number)
        if not state:
            print(f"워크플로우 상태 없음: #{issue_number}")
            return False
        
        # 현재 단계 승인
        state.approve()
        
        # 다음 단계로 진행
        if not state.advance_to_next_stage():
            print(f"마지막 단계 완료: #{issue_number}")
            return True
        
        # 다음 단계 실행
        if state.current_stage == WorkflowStage.PLAN:
            return self._execute_plan_stage(state, channel)
        elif state.current_stage == WorkflowStage.TASKS:
            return self._execute_tasks_stage(state, channel)
        elif state.current_stage == WorkflowStage.IMPLEMENTATION:
            return self._execute_implementation_stage(state, channel)
        
        return False
    
    def reject(self, issue_number: int, reason: str) -> bool:
        """
        현재 단계 거부
        
        Args:
            issue_number: Issue 번호
            reason: 거부 사유
            
        Returns:
            성공 여부
        """
        state = self.workflow_states.get(issue_number)
        if not state:
            return False
        
        state.reject(reason)
        print(f"❌ 단계 거부: #{issue_number} - {reason}")
        return True
    
    def _execute_plan_stage(self, state: WorkflowState, channel: str) -> bool:
        """Plan 단계 실행"""
        try:
            issue_dir = Path(state.spec_path).parent
            spec_path = Path(state.spec_path)
            
            plan_path, review_result = self.stage_executor.create_plan(issue_dir, spec_path)
            
            if not plan_path or not review_result:
                state.reject("Plan 생성 실패")
                return False
            
            state.plan_path = str(plan_path)
            
            # Slack 알림
            message = f"📋 Plan 생성 완료\n\n{review_result.comments}\n\n파일: `{plan_path}`"
            self.slack_bot.send_message(channel, message)
            
            if review_result.approved:
                print(f"✅ Plan 리뷰 통과 (#{state.issue_number})")
                # 자동으로 Tasks 생성 진행
                print(f"🔄 Tasks 단계 자동 시작 (#{state.issue_number})")
                self.approve_and_continue(state.issue_number, channel)
            else:
                state.reject(review_result.comments)
            
            return True
            
        except Exception as e:
            print(f"Plan 실행 오류: {e}")
            state.reject(str(e))
            return False
    
    def _execute_tasks_stage(self, state: WorkflowState, channel: str) -> bool:
        """Tasks 단계 실행"""
        try:
            issue_dir = Path(state.spec_path).parent
            plan_path = Path(state.plan_path)
            
            tasks_path, review_result = self.stage_executor.create_tasks(issue_dir, plan_path)
            
            if not tasks_path or not review_result:
                state.reject("Tasks 생성 실패")
                return False
            
            state.tasks_path = str(tasks_path)
            
            # Slack 알림
            message = f"✓ Tasks 생성 완료\n\n{review_result.comments}\n\n파일: `{tasks_path}`"
            self.slack_bot.send_message(channel, message)
            
            if review_result.approved:
                print(f"✅ Tasks 리뷰 통과 (#{state.issue_number})")
                # 자동으로 구현 단계 진행 (Goose)
                print(f"🔄 구현 단계 자동 시작 (#{state.issue_number})")
                self.approve_and_continue(state.issue_number, channel)
            else:
                state.reject(review_result.comments)
            
            return True
            
        except Exception as e:
            print(f"Tasks 실행 오류: {e}")
            state.reject(str(e))
            return False
    
    def _execute_implementation_stage(self, state: WorkflowState, channel: str) -> bool:
        """구현 단계 실행 (Goose)"""
        try:
            # Goose Client가 있는지 확인
            from integrations.goose_client import GooseClient
            
            goose_client = GooseClient()
            
            if not goose_client.goose_available:
                message = "⚠️ Goose CLI를 사용할 수 없습니다. 수동 구현이 필요합니다."
                self.slack_bot.send_message(channel, message)
                print(f"⚠️ Goose 미사용 - 수동 구현 필요 (#{state.issue_number})")
                return True
            
            tasks_path = Path(state.tasks_path)
            
            # Goose로 Tasks 실행
            print(f"🤖 Goose로 구현 시작 (#{state.issue_number})")
            result = goose_client.execute_tasks(tasks_path, state.issue_number)
            
            # 결과 저장
            state.implementation_status = result['status']
            
            # Slack 알림
            if result['status'] == 'success':
                message = f"✅ 구현 완료!\n\n완료된 태스크: {result['completed_tasks']}개"
                print(f"✅ 구현 완료 (#{state.issue_number})")
            elif result['status'] == 'skipped':
                message = f"⚠️ Goose 미사용\n\n{result['message']}"
            else:
                message = f"❌ 구현 실패\n\n{result.get('message', '알 수 없는 오류')}"
                state.reject(result.get('message', '구현 실패'))
            
            self.slack_bot.send_message(channel, message)
            
            return result['status'] in ['success', 'skipped']
            
        except Exception as e:
            print(f"구현 실행 오류: {e}")
            state.reject(str(e))
            return False
    
    def _create_approval_message(self, stage: str, issue: GitHubIssue, 
                                 review_result, file_path: Path) -> str:
        """승인 요청 메시지 생성"""
        status_emoji = "✅" if review_result.approved else "❌"
        
        message = f"""📋 {stage} 생성 완료 - Issue #{issue.number}

**제목**: {issue.title}
**상태**: {status_emoji} {review_result.status}
**점수**: {review_result.score:.2f}

**리뷰 결과**:
{review_result.comments}

**파일**: `{file_path}`

승인하시려면 Antigravity 대화창에서 '승인'을 입력하세요.
"""
        return message
