import logging
from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default="-")

class LevelFilter(logging.Filter) :
    def __init__(self, level) :
        self.level = level
    def filter(self, record) :
        return record.levelno == self.level

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True

root_logger = logging.getLogger()
# 하위 모듈 로거에서 오는 로그들 중 DEBUG 이상의 로그 처리 (사실 모든 레벨의 로그 모두 수집)
root_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [%(request_id)s] [%(name)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# RequestIdFilter 인스턴스 생성
request_id_filter = RequestIdFilter()

# DEBUG
debug_handler = logging.FileHandler("./log/debug.log")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
debug_handler.addFilter(request_id_filter)
debug_handler.addFilter(LevelFilter(logging.DEBUG))
root_logger.addHandler(debug_handler)

# INFO
info_handler = logging.FileHandler("./log/info.log")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
info_handler.addFilter(request_id_filter)
info_handler.addFilter(LevelFilter(logging.INFO))
root_logger.addHandler(info_handler)

# WARNING
warning_handler = logging.FileHandler("./log/warning.log")
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)
warning_handler.addFilter(request_id_filter)
warning_handler.addFilter(LevelFilter(logging.WARNING))
root_logger.addHandler(warning_handler)

# ERROR
error_handler = logging.FileHandler("./log/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
error_handler.addFilter(request_id_filter)
error_handler.addFilter(LevelFilter(logging.ERROR))
root_logger.addHandler(error_handler)