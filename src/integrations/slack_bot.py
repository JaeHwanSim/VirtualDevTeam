"""
Slack Bot Integration Module

Slack Interactive Components를 사용하여 승인/거부 버튼 기능을 제공합니다.
"""
import os
import json
import hmac
import hashlib
from typing import Dict, Any, Optional, Callable
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()


class SlackBot:
    """Slack Bot - Interactive Button 및 메시지 전송"""
    
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET")
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        
        if not self.bot_token:
            raise ValueError("SLACK_BOT_TOKEN이 설정되지 않았습니다.")
        if not self.signing_secret:
            raise ValueError("SLACK_SIGNING_SECRET이 설정되지 않았습니다.")
            
        self.client = WebClient(token=self.bot_token)
        self.approval_callbacks: Dict[str, Callable] = {}
    
    def verify_signature(self, timestamp: str, body: str, signature: str) -> bool:
        """
        Slack 요청 서명 검증
        
        Args:
            timestamp: X-Slack-Request-Timestamp 헤더
            body: 요청 본문 (raw bytes)
            signature: X-Slack-Signature 헤더
            
        Returns:
            서명 유효 여부
        """
        if abs(int(timestamp) - int(os.time.time())) > 60 * 5:
            return False
            
        sig_basestring = f"v0:{timestamp}:{body}".encode("utf-8")
        my_signature = "v0=" + hmac.new(
            self.signing_secret.encode("utf-8"),
            sig_basestring,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(my_signature, signature)
    
    def send_approval_request(
        self, 
        channel: str, 
        phase: str, 
        title: str, 
        description: str,
        callback_id: str
    ) -> Optional[str]:
        """
        승인 요청 메시지 전송 (Interactive Buttons 포함)
        
        Args:
            channel: 메시지를 보낼 채널 ID 또는 이름
            phase: Phase 이름 (예: "Phase 1: Constitution 업데이트")
            title: 제목
            description: 설명
            callback_id: 콜백 ID (승인/거부 이벤트 식별용)
            
        Returns:
            메시지 timestamp (성공) 또는 None (실패)
        """
        try:
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📋 {phase}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{title}*\n\n{description}"
                    }
                },
                {
                    "type": "actions",
                    "block_id": callback_id,
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "✅ 승인",
                                "emoji": True
                            },
                            "style": "primary",
                            "value": "approved",
                            "action_id": "approval_approved"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "❌ 거부",
                                "emoji": True
                            },
                            "style": "danger",
                            "value": "rejected",
                            "action_id": "approval_rejected"
                        }
                    ]
                }
            ]
            
            response = self.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f"{phase} - 승인 요청"
            )
            
            return response["ts"]
            
        except SlackApiError as e:
            print(f"Slack API 오류: {e.response['error']}")
            return None
    
    def send_message(self, channel: str, text: str) -> bool:
        """
        간단한 텍스트 메시지 전송
        
        Args:
            channel: 채널 ID 또는 이름
            text: 메시지 내용
            
        Returns:
            성공 여부
        """
        try:
            self.client.chat_postMessage(
                channel=channel,
                text=text
            )
            return True
        except SlackApiError as e:
            print(f"Slack API 오류: {e.response['error']}")
            return False
    
    def register_approval_callback(self, callback_id: str, callback: Callable[[str], None]):
        """
        승인/거부 콜백 등록
        
        Args:
            callback_id: 콜백 ID
            callback: 콜백 함수 (action: "approved" 또는 "rejected")
        """
        self.approval_callbacks[callback_id] = callback
    
    def handle_interaction(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interactive Component 이벤트 처리
        
        Args:
            payload: Slack에서 전송한 payload
            
        Returns:
            응답 메시지
        """
        action_id = payload["actions"][0]["action_id"]
        block_id = payload["actions"][0]["block_id"]
        value = payload["actions"][0]["value"]
        user = payload["user"]["name"]
        
        # 콜백 실행
        if block_id in self.approval_callbacks:
            self.approval_callbacks[block_id](value)
        
        # 메시지 업데이트
        if value == "approved":
            response_text = f"✅ *승인됨* (by @{user})"
            emoji = "✅"
        else:
            response_text = f"❌ *거부됨* (by @{user})"
            emoji = "❌"
        
        return {
            "replace_original": True,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": response_text
                    }
                }
            ]
        }
