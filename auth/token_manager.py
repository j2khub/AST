"""
토큰 관리자

키움 API 접근 토큰 발급 및 폐기를 담당합니다.

API 가이드:
- au10001: 접근토큰 발급
- au10002: 접근토큰 폐기
"""

from datetime import datetime
from typing import Optional, Dict, Any
from utils.api_client import KiwoomAPIClient
from utils.logger import get_logger


class TokenManager:
    """
    접근 토큰 관리자

    토큰 발급, 폐기, 갱신을 처리합니다.
    """

    def __init__(self, base_url: str, appkey: str, secretkey: str):
        """
        Args:
            base_url: API 기본 URL
            appkey: 앱 키
            secretkey: 시크릿 키
        """
        self.base_url = base_url
        self.appkey = appkey
        self.secretkey = secretkey
        self.token = ""
        self.token_type = ""
        self.expires_dt = ""
        self.logger = get_logger("token_manager")

        # API 클라이언트 (토큰 없이 초기화)
        self.client = KiwoomAPIClient(base_url, appkey, secretkey, token="")

    def issue_token(self) -> Dict[str, Any]:
        """
        접근 토큰 발급 (au10001)

        Returns:
            Dict[str, Any]: 토큰 정보
                - token: 접근 토큰
                - token_type: 토큰 타입
                - expires_dt: 만료 일시

        Raises:
            APIError: API 오류 발생 시
        """
        self.logger.info("접근 토큰 발급 요청...")

        # 요청 데이터
        data = {
            "grant_type": "client_credentials",
            "appkey": self.appkey,
            "secretkey": self.secretkey
        }

        try:
            # au10001 API 호출 (토큰 없이 요청)
            response = self.client.post(
                api_id="au10001",
                url_path="/oauth2/token",
                data=data,
                use_token=False
            )

            # 토큰 정보 저장
            self.token = response.get("token", "")
            self.token_type = response.get("token_type", "")
            self.expires_dt = response.get("expires_dt", "")

            # 클라이언트에 토큰 업데이트
            self.client.update_token(self.token)

            self.logger.info(f"토큰 발급 성공 (만료: {self.expires_dt})")

            return {
                "token": self.token,
                "token_type": self.token_type,
                "expires_dt": self.expires_dt
            }

        except Exception as e:
            self.logger.error(f"토큰 발급 실패: {e}")
            raise

    def revoke_token(self, token: Optional[str] = None) -> bool:
        """
        접근 토큰 폐기 (au10002)

        Args:
            token: 폐기할 토큰 (None이면 현재 토큰)

        Returns:
            bool: 성공 여부

        Raises:
            APIError: API 오류 발생 시
        """
        target_token = token or self.token

        if not target_token:
            self.logger.warning("폐기할 토큰이 없습니다.")
            return False

        self.logger.info("접근 토큰 폐기 요청...")

        # 요청 데이터
        data = {
            "appkey": self.appkey,
            "secretkey": self.secretkey,
            "token": target_token
        }

        try:
            # au10002 API 호출
            response = self.client.post(
                api_id="au10002",
                url_path="/oauth2/revoke",
                data=data,
                use_token=True
            )

            # 현재 토큰을 폐기한 경우 초기화
            if target_token == self.token:
                self.token = ""
                self.token_type = ""
                self.expires_dt = ""
                self.client.update_token("")

            self.logger.info("토큰 폐기 성공")
            return True

        except Exception as e:
            self.logger.error(f"토큰 폐기 실패: {e}")
            raise

    def is_token_valid(self) -> bool:
        """
        토큰 유효성 확인

        Returns:
            bool: 토큰이 유효하면 True
        """
        if not self.token:
            return False

        if not self.expires_dt:
            return True  # 만료 시간이 없으면 유효하다고 가정

        try:
            # 만료 시간 파싱 (YYYYMMDDHHmmss)
            expires = datetime.strptime(self.expires_dt, "%Y%m%d%H%M%S")
            now = datetime.now()

            # 만료 시간과 비교
            is_valid = now < expires

            if not is_valid:
                self.logger.warning(f"토큰이 만료되었습니다. (만료: {self.expires_dt})")

            return is_valid

        except ValueError as e:
            self.logger.error(f"만료 시간 파싱 오류: {e}")
            return False

    def get_token(self) -> str:
        """
        현재 토큰 반환

        Returns:
            str: 접근 토큰
        """
        return self.token

    def get_token_info(self) -> Dict[str, str]:
        """
        토큰 정보 반환

        Returns:
            Dict[str, str]: 토큰 정보
        """
        return {
            "token": self.token,
            "token_type": self.token_type,
            "expires_dt": self.expires_dt,
            "is_valid": str(self.is_token_valid())
        }

    def ensure_token(self) -> str:
        """
        유효한 토큰 확보

        토큰이 없거나 만료된 경우 새로 발급합니다.

        Returns:
            str: 유효한 접근 토큰

        Raises:
            APIError: 토큰 발급 실패 시
        """
        if not self.is_token_valid():
            self.logger.info("토큰이 유효하지 않아 새로 발급합니다.")
            self.issue_token()

        return self.token


if __name__ == "__main__":
    # 토큰 매니저 테스트
    from config import get_current_config

    config = get_current_config()

    manager = TokenManager(
        base_url=config["base_url"],
        appkey=config["appkey"],
        secretkey=config["secretkey"]
    )

    print("=== 토큰 매니저 테스트 ===")
    print(f"Base URL: {config['base_url']}")
    print(f"모드: {config['mode']}")
    print()

    # 토큰 발급은 실제 API 호출이 필요하므로 주석 처리
    # token_info = manager.issue_token()
    # print(f"발급된 토큰: {token_info}")
    print("토큰 발급을 테스트하려면 주석을 해제하세요.")
