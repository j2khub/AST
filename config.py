"""
키움 API 자동매매 시스템 설정 관리

실전투자와 모의투자를 환경변수를 통해 구분하여 관리합니다.
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """기본 설정"""

    # 운영 모드 (real: 실전투자, virtual: 모의투자)
    MODE = os.getenv("MODE", "virtual")

    # 공통 설정
    ACCOUNT_NO = os.getenv("ACCOUNT_NO", "")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 자동매매 설정
    AUTO_TRADE_ENABLED = os.getenv("AUTO_TRADE_ENABLED", "false").lower() == "true"
    MAX_BUY_AMOUNT = int(os.getenv("MAX_BUY_AMOUNT", "1000000"))
    MAX_POSITION_COUNT = int(os.getenv("MAX_POSITION_COUNT", "5"))

    # 로그 디렉토리
    LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")

    @classmethod
    def get_api_config(cls):
        """
        현재 모드에 따라 API 설정 반환

        Returns:
            dict: API 설정 정보
        """
        if cls.MODE == "real":
            return RealConfig.get_config()
        else:
            return VirtualConfig.get_config()

    @classmethod
    def is_real_mode(cls):
        """실전투자 모드인지 확인"""
        return cls.MODE == "real"

    @classmethod
    def is_virtual_mode(cls):
        """모의투자 모드인지 확인"""
        return cls.MODE == "virtual"


class RealConfig:
    """실전투자 설정"""

    # 실전투자 API 인증 정보
    APPKEY = os.getenv("REAL_APPKEY", "")
    SECRETKEY = os.getenv("REAL_SECRETKEY", "")
    TOKEN = os.getenv("REAL_TOKEN", "")

    # 실전투자 API URL (API 가이드 기준)
    API_BASE_URL = os.getenv("REAL_API_URL", "https://api.kiwoom.com")

    @classmethod
    def get_config(cls):
        """실전투자 API 설정 반환"""
        return {
            "appkey": cls.APPKEY,
            "secretkey": cls.SECRETKEY,
            "token": cls.TOKEN,
            "base_url": cls.API_BASE_URL,
            "mode": "real"
        }

    @classmethod
    def validate(cls):
        """실전투자 설정 검증"""
        if not cls.APPKEY or not cls.SECRETKEY:
            raise ValueError("실전투자 APPKEY와 SECRETKEY가 설정되지 않았습니다.")
        return True


class VirtualConfig:
    """모의투자 설정"""

    # 모의투자 API 인증 정보
    APPKEY = os.getenv("VIRTUAL_APPKEY", "")
    SECRETKEY = os.getenv("VIRTUAL_SECRETKEY", "")
    TOKEN = os.getenv("VIRTUAL_TOKEN", "")

    # 모의투자 API URL (API 가이드 기준)
    API_BASE_URL = os.getenv("VIRTUAL_API_URL", "https://mockapi.kiwoom.com")

    @classmethod
    def get_config(cls):
        """모의투자 API 설정 반환"""
        return {
            "appkey": cls.APPKEY,
            "secretkey": cls.SECRETKEY,
            "token": cls.TOKEN,
            "base_url": cls.API_BASE_URL,
            "mode": "virtual"
        }

    @classmethod
    def validate(cls):
        """모의투자 설정 검증"""
        if not cls.APPKEY or not cls.SECRETKEY:
            raise ValueError("모의투자 APPKEY와 SECRETKEY가 설정되지 않았습니다.")
        return True


# 현재 설정 가져오기 (편의 함수)
def get_current_config():
    """
    현재 모드에 맞는 설정 반환

    Returns:
        dict: API 설정 정보
    """
    config = Config.get_api_config()

    # 설정 검증
    if Config.is_real_mode():
        RealConfig.validate()
    else:
        VirtualConfig.validate()

    return config


# 디버그용: 현재 설정 출력 (민감한 정보 마스킹)
def print_current_config():
    """현재 설정 정보 출력 (디버깅용)"""
    config = Config.get_api_config()

    print(f"=== 현재 설정 ===")
    print(f"모드: {config['mode']}")
    print(f"Base URL: {config['base_url']}")
    print(f"APPKEY: {config['appkey'][:8]}..." if config['appkey'] else "APPKEY: (미설정)")
    print(f"SECRETKEY: {config['secretkey'][:8]}..." if config['secretkey'] else "SECRETKEY: (미설정)")
    print(f"TOKEN: {'설정됨' if config['token'] else '미설정'}")
    print(f"계좌번호: {Config.ACCOUNT_NO}")
    print(f"자동매매: {'활성화' if Config.AUTO_TRADE_ENABLED else '비활성화'}")
    print(f"최대 매수금액: {Config.MAX_BUY_AMOUNT:,}원")
    print(f"최대 보유종목: {Config.MAX_POSITION_COUNT}개")
    print("=" * 30)


if __name__ == "__main__":
    # 설정 테스트
    print_current_config()
