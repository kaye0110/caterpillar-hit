import logging
import os
from logging.handlers import TimedRotatingFileHandler


class LoggerMgmt:
    # 创建一个日志格式器
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    # 创建一个控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    output_path = os.getenv('LOG_PATH', None)

    if output_path is None or len(output_path) == 0:
        # 创建一个文件处理器
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
        output_path = os.path.join(project_root, 'logs')
    elif output_path.endswith(".log") is False:
        output_path = os.path.join(output_path, 'logs')
        pass

    info_output_path = os.path.join(os.path.dirname(output_path), 'logs', 'info.log')
    # 按日拆分主日志文件
    file_handler = TimedRotatingFileHandler(info_output_path, when='D', interval=1, backupCount=7)
    file_handler.setFormatter(formatter)

    # 按日拆分 error 日志文件
    error_output_path = os.path.join(os.path.dirname(output_path), 'logs', 'error.log')
    error_handler = TimedRotatingFileHandler(error_output_path, when='D', interval=1, backupCount=7)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # 按日拆分 warning 日志文件
    warning_output_path = os.path.join(os.path.dirname(output_path), 'logs', 'warning.log')
    warning_handler = TimedRotatingFileHandler(warning_output_path, when='D', interval=1, backupCount=7)
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)

    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # 将处理器添加到根日志记录器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(warning_handler)
