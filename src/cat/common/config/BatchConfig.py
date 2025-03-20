import logging
import os
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler


class Batch:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "http://localhost:8080")

    def get(self, service_url):
        try:
            response = requests.get(service_url)
            response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError 异常
            logging.getLogger(__name__).info(f"HTTP request successful at {datetime.now()}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.getLogger(__name__).info(f"HTTP request failed at {datetime.now()}: {e}")

    def pull_sina_data(self):
        url = self.base_url + "/price/pull_sina"  # 替换为你的本地 HTTP 服务接口
        self.get(url)

    def pull_tushare_data(self):
        current = datetime.now().strftime("%Y%m%d")  # 获取当前
        url = self.base_url + f"/price/pull_tushare?start_date={current}&end_date={current}"  # 替换为你的本地 HTTP 服务接口
        self.get(url)

    def pull_tushare_ths_data(self):
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")
        current = datetime.now().strftime("%Y%m%d")  # 获取当前
        url = self.base_url + f"/price/tushare/pull_ths_data?start_date={start_date}&end_date={current}"  # 替换为你的本地 HTTP 服务接口
        self.get(url)

    def pull_tushare_index(self):
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")
        current = datetime.now().strftime("%Y%m%d")  # 获取当前
        url = self.base_url + f"/index/pull?start_date={start_date}&end_date={current}"  # 替换为你的本地 HTTP 服务接口
        self.get(url)

    def init_scheduler(self) -> BackgroundScheduler:
        logging.getLogger(__name__).info("init_scheduler")
        scheduler = BackgroundScheduler()

        # 每周一到周五的 9:30-11:30 和 13:00-15:00 期间每两分钟执行一次任务
        for hour in [9, 10, 11, 13, 14]:
            start_minute = 30 if hour == 9 else 0
            end_minute = 30 if hour == 11 else 60
            for minute in range(start_minute, end_minute, 3):
                pass
                # scheduler.add_job(self.pull_sina_data, 'cron', day_of_week='mon-fri', hour=hour, minute=minute)

        # 每周一到周五的每天晚上 17:00 执行一次任务
        # scheduler.add_job(self.pull_tushare_data, 'cron', day_of_week='mon-fri', hour=16, minute=30)

        # 每周一到周五的每天晚上 18:00 执行一次任务
        # scheduler.add_job(self.run_strategy_limit_up, 'cron', day_of_week='mon-fri', hour=17, minute=00)

        # 每周一到周五的每天晚上 19:00 执行一次任务
        # scheduler.add_job(self.run_strategy_adjust_macd_kdj, 'cron', day_of_week='mon-fri', hour=17, minute=20)

        # scheduler.add_job(self.run_strategy_sharp_w, 'cron', day_of_week='mon-fri', hour=17, minute=40)

        # 每周一到周五的每天晚上 20:00 执行一次任务
        # scheduler.add_job(self.run_trade_append_current, 'cron', day_of_week='mon-fri', hour=17, minute=30)

        # 每周一到周五的每天晚上 20:00 执行一次任务
        # scheduler.add_job(self.pull_tushare_ths_data, 'cron', day_of_week='mon-fri', hour=18, minute=30)

        # 每周一到周五的每天晚上 21:00 执行一次任务
        # scheduler.add_job(self.pull_tushare_index, 'cron', day_of_week='mon-fri', hour=20, minute=30)

        # 启动调度器
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

        return scheduler
