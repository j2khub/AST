#!/usr/bin/env python3
"""
키움 API 자동매매 시스템

실시간 조건검색 기반 자동매매 시스템 메인 실행 파일

주요 기능:
1. 토큰 자동 발급/갱신
2. 실시간 조건검색 모니터링
3. 조건 편입 종목 자동 매수
4. 계좌 및 주문 관리
"""

import sys
import signal
from config import get_current_config, Config
from auth.token_manager import TokenManager
from utils.logger import setup_logger


class KiwoomAutoTrader:
    """키움 자동매매 시스템"""

    def __init__(self):
        """초기화"""
        self.logger = setup_logger("main", log_level=Config.LOG_LEVEL)
        self.config = None
        self.token_manager = None
        self.running = False

        # 시그널 핸들러 등록 (Ctrl+C 등)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """시그널 핸들러"""
        self.logger.info("종료 시그널을 받았습니다.")
        self.stop()

    def initialize(self):
        """시스템 초기화"""
        self.logger.info("=" * 60)
        self.logger.info("키움 API 자동매매 시스템 시작")
        self.logger.info("=" * 60)

        try:
            # 설정 로드
            self.config = get_current_config()
            self.logger.info(f"모드: {self.config['mode']}")
            self.logger.info(f"Base URL: {self.config['base_url']}")
            self.logger.info(f"자동매매: {'활성화' if Config.AUTO_TRADE_ENABLED else '비활성화'}")

            # 토큰 매니저 초기화
            self.token_manager = TokenManager(
                base_url=self.config["base_url"],
                appkey=self.config["appkey"],
                secretkey=self.config["secretkey"]
            )

            # 기존 토큰 확인
            if self.config["token"]:
                self.logger.info("기존 토큰을 로드했습니다.")
                self.token_manager.token = self.config["token"]
                self.token_manager.client.update_token(self.config["token"])

                # 토큰 유효성 확인
                if not self.token_manager.is_token_valid():
                    self.logger.warning("토큰이 만료되었습니다. 새로 발급합니다.")
                    self.issue_new_token()
                else:
                    self.logger.info("토큰이 유효합니다.")
            else:
                self.logger.info("토큰이 없습니다. 새로 발급합니다.")
                self.issue_new_token()

            self.logger.info("시스템 초기화 완료")
            return True

        except Exception as e:
            self.logger.error(f"초기화 실패: {e}", exc_info=True)
            return False

    def issue_new_token(self):
        """새 토큰 발급"""
        try:
            self.logger.info("토큰 발급 요청...")
            token_info = self.token_manager.issue_token()
            self.logger.info(f"토큰 발급 성공 (만료: {token_info['expires_dt']})")

            # TODO: .env 파일에 토큰 자동 저장 (선택사항)
            self.logger.info("토큰을 수동으로 .env 파일에 저장하려면 issue_token.py를 실행하세요.")

        except Exception as e:
            self.logger.error(f"토큰 발급 실패: {e}", exc_info=True)
            raise

    def start(self):
        """시스템 시작"""
        if not self.initialize():
            self.logger.error("초기화 실패로 시스템을 시작할 수 없습니다.")
            return False

        self.running = True
        self.logger.info("=" * 60)
        self.logger.info("시스템이 시작되었습니다.")
        self.logger.info("=" * 60)

        try:
            # TODO: 실시간 조건검색 모니터링 시작
            # TODO: 자동매매 로직 실행

            self.logger.info("현재는 토큰 발급까지만 구현되어 있습니다.")
            self.logger.info("실시간 조건검색 및 자동매매 기능은 추후 구현됩니다.")

            # 임시: 토큰 정보 출력
            token_info = self.token_manager.get_token_info()
            self.logger.info(f"토큰 정보: {token_info}")

            return True

        except Exception as e:
            self.logger.error(f"시스템 실행 중 오류: {e}", exc_info=True)
            return False

    def stop(self):
        """시스템 종료"""
        self.logger.info("시스템 종료 중...")
        self.running = False

        # TODO: 실시간 조건검색 해제
        # TODO: 리소스 정리

        # 토큰 폐기 (선택사항)
        if self.token_manager and self.token_manager.get_token():
            try:
                revoke = input("토큰을 폐기하시겠습니까? (y/n): ").lower()
                if revoke == 'y':
                    self.token_manager.revoke_token()
                    self.logger.info("토큰이 폐기되었습니다.")
            except:
                pass

        self.logger.info("=" * 60)
        self.logger.info("시스템 종료 완료")
        self.logger.info("=" * 60)


def main():
    """메인 함수"""
    trader = KiwoomAutoTrader()

    try:
        success = trader.start()
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n키보드 인터럽트를 받았습니다.")
        trader.stop()
        return 0

    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        trader.stop()
        return 1


if __name__ == "__main__":
    sys.exit(main())
