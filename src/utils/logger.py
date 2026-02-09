"""
로깅 시스템

Agent들의 생각과 진행 과정을 상세히 기록
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, level=logging.INFO, log_to_file=True):
    """
    로거 설정
    
    Args:
        name: 로거 이름
        level: 로그 레벨
        log_to_file: 파일에도 저장할지 여부
        
    Returns:
        설정된 로거
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 기존 핸들러 제거 (중복 방지)
    logger.handlers.clear()
    
    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러
    if log_to_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 날짜별 로그 파일
        log_file = log_dir / f"workflow_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def setup_detailed_logger(name: str, issue_number: int = None):
    """
    상세 로깅을 위한 로거 (각 워크플로우별)
    
    Args:
        name: 로거 이름
        issue_number: Issue 번호 (선택)
        
    Returns:
        설정된 로거
    """
    logger = logging.getLogger(f"{name}.{issue_number}" if issue_number else name)
    logger.setLevel(logging.DEBUG)
    
    logger.handlers.clear()
    
    # 더 상세한 포맷
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d | [%(levelname)s] %(name)s\n'
        '  └─ %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # 콘솔
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 (Issue별)
    if issue_number:
        log_dir = Path("logs") / f"issue_{issue_number}"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 기본 로거들
main_logger = setup_logger("main")
github_logger = setup_logger("github")
slack_logger = setup_logger("slack")
gemini_logger = setup_logger("gemini")
goose_logger = setup_logger("goose")
review_logger = setup_logger("review", level=logging.DEBUG)
workflow_logger = setup_logger("workflow", level=logging.DEBUG)
