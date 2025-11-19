"""
키움 API 클라이언트 베이스

키움 REST API 통신을 위한 기본 클라이언트
API 가이드 기준으로 작성됨
"""

import requests
from typing import Dict, Optional, Any
from utils.logger import get_logger


class KiwoomAPIClient:
    """
    키움 API 클라이언트

    API 가이드 기준:
    - 실전투자: https://api.kiwoom.com
    - 모의투자: https://mockapi.kiwoom.com
    """

    def __init__(self, base_url: str, appkey: str, secretkey: str, token: str = ""):
        """
        Args:
            base_url: API 기본 URL
            appkey: 앱 키
            secretkey: 시크릿 키
            token: 접근 토큰 (선택)
        """
        self.base_url = base_url.rstrip('/')
        self.appkey = appkey
        self.secretkey = secretkey
        self.token = token
        self.logger = get_logger("api_client")

    def _build_headers(
        self,
        api_id: str,
        use_token: bool = True,
        cont_yn: str = "",
        next_key: str = ""
    ) -> Dict[str, str]:
        """
        API 요청 헤더 생성

        Args:
            api_id: API ID (예: au10001)
            use_token: 토큰 사용 여부
            cont_yn: 연속조회 여부
            next_key: 연속조회 키

        Returns:
            Dict[str, str]: 요청 헤더
        """
        headers = {
            "api-id": api_id,
            "Content-Type": "application/json;charset=UTF-8"
        }

        # 토큰이 있고 사용하도록 설정된 경우
        if use_token and self.token:
            headers["authorization"] = f"Bearer {self.token}"

        # 연속조회 헤더
        if cont_yn:
            headers["cont-yn"] = cont_yn
        if next_key:
            headers["next-key"] = next_key

        return headers

    def post(
        self,
        api_id: str,
        url_path: str,
        data: Dict[str, Any],
        use_token: bool = True,
        cont_yn: str = "",
        next_key: str = ""
    ) -> Dict[str, Any]:
        """
        POST 요청 실행

        Args:
            api_id: API ID
            url_path: URL 경로 (예: /oauth2/token)
            data: 요청 바디 데이터
            use_token: 토큰 사용 여부
            cont_yn: 연속조회 여부
            next_key: 연속조회 키

        Returns:
            Dict[str, Any]: 응답 데이터

        Raises:
            requests.exceptions.RequestException: 요청 실패 시
        """
        url = f"{self.base_url}{url_path}"
        headers = self._build_headers(api_id, use_token, cont_yn, next_key)

        self.logger.debug(f"API 요청: {api_id} -> {url}")
        self.logger.debug(f"헤더: {headers}")
        self.logger.debug(f"데이터: {data}")

        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()

            self.logger.debug(f"응답: {result}")

            # 응답 코드 확인
            return_code = result.get("return_code", -1)
            return_msg = result.get("return_msg", "")

            if return_code != 0:
                self.logger.error(f"API 오류: [{return_code}] {return_msg}")
                raise APIError(return_code, return_msg)

            return result

        except requests.exceptions.Timeout:
            self.logger.error(f"API 요청 타임아웃: {url}")
            raise
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP 오류: {e}")
            self.logger.error(f"응답 내용: {e.response.text if e.response else 'N/A'}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"요청 오류: {e}")
            raise

    def get(
        self,
        api_id: str,
        url_path: str,
        params: Optional[Dict[str, Any]] = None,
        use_token: bool = True,
        cont_yn: str = "",
        next_key: str = ""
    ) -> Dict[str, Any]:
        """
        GET 요청 실행

        Args:
            api_id: API ID
            url_path: URL 경로
            params: 쿼리 파라미터
            use_token: 토큰 사용 여부
            cont_yn: 연속조회 여부
            next_key: 연속조회 키

        Returns:
            Dict[str, Any]: 응답 데이터

        Raises:
            requests.exceptions.RequestException: 요청 실패 시
        """
        url = f"{self.base_url}{url_path}"
        headers = self._build_headers(api_id, use_token, cont_yn, next_key)

        self.logger.debug(f"API 요청: {api_id} -> {url}")
        self.logger.debug(f"헤더: {headers}")
        self.logger.debug(f"파라미터: {params}")

        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()

            self.logger.debug(f"응답: {result}")

            # 응답 코드 확인
            return_code = result.get("return_code", -1)
            return_msg = result.get("return_msg", "")

            if return_code != 0:
                self.logger.error(f"API 오류: [{return_code}] {return_msg}")
                raise APIError(return_code, return_msg)

            return result

        except requests.exceptions.Timeout:
            self.logger.error(f"API 요청 타임아웃: {url}")
            raise
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP 오류: {e}")
            self.logger.error(f"응답 내용: {e.response.text if e.response else 'N/A'}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"요청 오류: {e}")
            raise

    def update_token(self, token: str):
        """
        접근 토큰 업데이트

        Args:
            token: 새로운 접근 토큰
        """
        self.token = token
        self.logger.info("접근 토큰이 업데이트되었습니다.")


class APIError(Exception):
    """API 오류 예외"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
