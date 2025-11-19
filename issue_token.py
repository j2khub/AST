#!/usr/bin/env python3
"""
토큰 발급 스크립트

키움 API 접근 토큰을 발급하고 .env 파일에 저장합니다.

사용법:
    python issue_token.py
"""

import os
import sys
from dotenv import load_dotenv, set_key
from config import get_current_config, Config
from auth.token_manager import TokenManager
from utils.logger import setup_logger


def update_env_token(token: str, expires_dt: str):
    """
    .env 파일에 토큰 업데이트

    Args:
        token: 발급받은 토큰
        expires_dt: 만료 일시
    """
    env_file = os.path.join(os.path.dirname(__file__), '.env')

    # .env 파일이 없으면 .env.example을 복사
    if not os.path.exists(env_file):
        example_file = os.path.join(os.path.dirname(__file__), '.env.example')
        if os.path.exists(example_file):
            import shutil
            shutil.copy(example_file, env_file)
            print(f".env 파일이 생성되었습니다: {env_file}")
        else:
            print("경고: .env.example 파일이 없습니다.")
            return

    # 현재 모드에 따라 적절한 키 선택
    if Config.is_real_mode():
        token_key = "REAL_TOKEN"
    else:
        token_key = "VIRTUAL_TOKEN"

    # 토큰 저장
    set_key(env_file, token_key, token)
    print(f"{token_key}이(가) .env 파일에 저장되었습니다.")
    print(f"만료 일시: {expires_dt}")


def main():
    """메인 실행 함수"""
    # 로거 설정
    logger = setup_logger("token_issue", log_level="INFO")

    print("=" * 60)
    print("키움 API 접근 토큰 발급")
    print("=" * 60)
    print()

    try:
        # 설정 로드
        config = get_current_config()

        print(f"모드: {config['mode']}")
        print(f"Base URL: {config['base_url']}")
        print(f"APPKEY: {config['appkey'][:8]}..." if config['appkey'] else "APPKEY: (미설정)")
        print(f"SECRETKEY: {config['secretkey'][:8]}..." if config['secretkey'] else "SECRETKEY: (미설정)")
        print()

        # 토큰 매니저 생성
        manager = TokenManager(
            base_url=config["base_url"],
            appkey=config["appkey"],
            secretkey=config["secretkey"]
        )

        # 토큰 발급
        print("토큰 발급을 시작합니다...")
        print()

        token_info = manager.issue_token()

        print("=" * 60)
        print("✅ 토큰 발급 성공!")
        print("=" * 60)
        print(f"토큰: {token_info['token'][:20]}...")
        print(f"토큰 타입: {token_info['token_type']}")
        print(f"만료 일시: {token_info['expires_dt']}")
        print()

        # .env 파일에 토큰 저장
        save = input(".env 파일에 토큰을 저장하시겠습니까? (y/n): ").lower()
        if save == 'y':
            update_env_token(token_info['token'], token_info['expires_dt'])
            print("✅ 토큰이 저장되었습니다.")
        else:
            print("토큰 저장을 건너뜁니다.")
            print()
            print("수동으로 .env 파일에 다음 값을 설정하세요:")
            if Config.is_real_mode():
                print(f"REAL_TOKEN={token_info['token']}")
            else:
                print(f"VIRTUAL_TOKEN={token_info['token']}")

        print()
        print("=" * 60)

        return 0

    except ValueError as e:
        logger.error(f"설정 오류: {e}")
        print(f"❌ 오류: {e}")
        print()
        print(".env 파일에 APPKEY와 SECRETKEY를 설정해주세요.")
        return 1

    except Exception as e:
        logger.error(f"토큰 발급 실패: {e}", exc_info=True)
        print(f"❌ 토큰 발급 실패: {e}")
        print()
        print("상세 오류는 로그 파일을 확인해주세요.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
