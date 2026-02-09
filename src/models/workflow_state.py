"""
Workflow State Model

워크플로우의 각 단계 상태를 관리하는 모델
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class WorkflowStage(Enum):
    """워크플로우 단계"""
    CONSTITUTION = "constitution"
    SPEC = "spec"
    PLAN = "plan"
    TASKS = "tasks"
    IMPLEMENTATION = "implementation"


class ApprovalStatus(Enum):
    """승인 상태"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class WorkflowState:
    """워크플로우 상태"""
    
    issue_number: int
    current_stage: WorkflowStage
    approval_status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    spec_path: Optional[str] = None
    plan_path: Optional[str] = None
    tasks_path: Optional[str] = None
    implementation_status: Optional[str] = None
    error_message: Optional[str] = None
    
    def advance_to_next_stage(self) -> bool:
        """
        다음 단계로 진행
        
        Returns:
            성공 여부
        """
        stage_order = [
            WorkflowStage.CONSTITUTION,
            WorkflowStage.SPEC,
            WorkflowStage.PLAN,
            WorkflowStage.TASKS,
            WorkflowStage.IMPLEMENTATION
        ]
        
        try:
            current_index = stage_order.index(self.current_stage)
            if current_index < len(stage_order) - 1:
                self.current_stage = stage_order[current_index + 1]
                self.approval_status = ApprovalStatus.PENDING
                self.updated_at = datetime.now()
                return True
            return False
        except ValueError:
            return False
    
    def approve(self):
        """현재 단계 승인"""
        self.approval_status = ApprovalStatus.APPROVED
        self.updated_at = datetime.now()
    
    def reject(self, reason: str):
        """현재 단계 거부"""
        self.approval_status = ApprovalStatus.REJECTED
        self.error_message = reason
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            'issue_number': self.issue_number,
            'current_stage': self.current_stage.value,
            'approval_status': self.approval_status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'spec_path': self.spec_path,
            'plan_path': self.plan_path,
            'tasks_path': self.tasks_path,
            'error_message': self.error_message
        }
