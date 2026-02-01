"""
Scheduler Service
定期実行ジョブ管理
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from typing import Optional

from app.db.session import get_db
from app.models.favorite import Favorite
from app.models.company import Company
from app.services.buffett_code_client import buffett_code_client

# ロガー設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchedulerService:
    """スケジューラーサービス"""

    def __init__(self):
        self.scheduler: Optional[AsyncIOScheduler] = None

    def start(self):
        """スケジューラー起動"""
        if self.scheduler is not None:
            logger.warning("Scheduler already started")
            return

        self.scheduler = AsyncIOScheduler()

        # 深夜3時に決算データ更新ジョブを実行
        self.scheduler.add_job(
            self.update_financial_data_job,
            CronTrigger(hour=3, minute=0),
            id="update_financial_data",
            name="決算データ自動更新",
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("Scheduler started successfully")

    def stop(self):
        """スケジューラー停止"""
        if self.scheduler:
            self.scheduler.shutdown()
            self.scheduler = None
            logger.info("Scheduler stopped")

    async def update_financial_data_job(self):
        """
        決算データ自動更新ジョブ
        お気に入り銘柄の決算データを更新
        """
        logger.info(f"Starting financial data update job at {datetime.now()}")

        try:
            db = next(get_db())

            # お気に入り銘柄を取得
            favorites = db.query(Favorite).all()

            if not favorites:
                logger.info("No favorite companies found")
                return

            updated_count = 0
            error_count = 0

            for favorite in favorites:
                try:
                    company = db.query(Company).filter(
                        Company.id == favorite.company_id
                    ).first()

                    if not company:
                        continue

                    # 決算データ更新
                    success = await self._update_company_financials(
                        db, company.stock_code
                    )

                    if success:
                        updated_count += 1
                        logger.info(
                            f"Updated financial data for {company.name} ({company.stock_code})"
                        )
                    else:
                        error_count += 1
                        logger.error(
                            f"Failed to update financial data for {company.stock_code}"
                        )

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error updating company {favorite.company_id}: {e}")
                    continue

            logger.info(
                f"Financial data update job completed. "
                f"Updated: {updated_count}, Errors: {error_count}"
            )

        except Exception as e:
            logger.error(f"Financial data update job failed: {e}")

    async def _update_company_financials(self, db, stock_code: str) -> bool:
        """
        企業の決算データを更新

        Args:
            db: データベースセッション
            stock_code: 銘柄コード

        Returns:
            成功時True
        """
        try:
            # バフェット・コードAPIから決算データ取得
            financial_data = buffett_code_client.get_financial_data(stock_code)

            if not financial_data:
                return False

            # TODO: データベースへの保存処理
            # 実装は既存のAPIエンドポイントのロジックを再利用

            return True

        except Exception as e:
            logger.error(f"Error fetching financial data for {stock_code}: {e}")
            return False

    def trigger_update_now(self):
        """手動で決算データ更新を実行"""
        if self.scheduler:
            self.scheduler.add_job(
                self.update_financial_data_job,
                id="manual_update_financial_data",
                replace_existing=True
            )
            logger.info("Manual financial data update triggered")


# Singleton instance
scheduler_service = SchedulerService()
