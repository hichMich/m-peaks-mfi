from starlette.config import Config
from starlette.datastructures import Secret

# Config will be read from environment variables and/or ".env" files.
config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default="DEBUG")
LOG_FORMAT = config("LOG_FORMAT", default="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
ACCESS_LOG_FORMAT = config(
    "ACCESS_LOG_FORMAT",
    default="%(asctime)s | %(name)s | %(levelname)s | %(client_addr)s | %(request_line)s %(status_code)s",
)

HTTP_HOST = config("HTTP_HOST", default="0.0.0.0")
HTTP_PORT = config("HTTP_PORT", cast=int, default=5001)

VERSION = config("VERSION", default='1.0')

DB_PROCOTOL = config('DB_PROCOTOL', default='postgresql')
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', cast=int, default=5432)
DB_SCHEMA = config('DB_SCHEMA', default='peaks')
DB_USER = config('DB_USER', default='mfi')
DB_PASS = config('DB_PASS', cast=Secret, default="mfi")
DB_URL = f"{DB_PROCOTOL}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
DB_SQLALCHEMY_ECHO = config("DB_SQLALCHEMY_ECHO", cast=bool, default=False)
