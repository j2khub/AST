"""
로깅 설정 및 관리

JSON 포맷 로거를 설정하고 파일/콘솔 출력을 관리합니다.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from datetime import datetime


def setup_logger(name="kiwoom", log_level=None, log_dir=None):
    """
    로거 설정

    Args:
        name: 로거 이름
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)
        log_dir: 로그 디렉토리 경로

    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    from config import Config

    # 로그 레벨 설정
    if log_level is None:
        log_level = Config.LOG_LEVEL

    # 로그 디렉토리 설정
    if log_dir is None:
        log_dir = Config.LOG_DIR

    # 로그 디렉토리 생성
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    # 이미 핸들러가 있으면 제거 (중복 방지)
    if logger.handlers:
        logger.handlers.clear()

    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # JSON 포맷 설정
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        timestamp=True
    )

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 파일 핸들러 (일반 로그)
    today = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(log_dir, f"{name}_{today}.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # JSON 파일 핸들러 (구조화된 로그)
    json_log_file = os.path.join(log_dir, f"{name}_{today}.json")
    json_file_handler = RotatingFileHandler(
        json_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    json_file_handler.setLevel(getattr(logging, log_level))
    json_file_handler.setFormatter(json_formatter)
    logger.addHandler(json_file_handler)

    logger.info(f"로거 설정 완료: {name} (레벨: {log_level})")

    return logger


def get_logger(name="kiwoom"):
    """
    기존 로거 가져오기 또는 새로 생성

    Args:
        name: 로거 이름

    Returns:
        logging.Logger: 로거 인스턴스
    """
    logger = logging.getLogger(name)

    # 로거가 설정되지 않았으면 새로 설정
    if not logger.handlers:
        return setup_logger(name)

    return logger


if __name__ == "__main__":
    # 로거 테스트
    logger = setup_logger("test")

    logger.debug("디버그 메시지")
    logger.info("정보 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
