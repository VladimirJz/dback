from settings import Hasher
from .base import *
DATABASES = {
    "default": {
        "ENGINE": "sql_server.pyodbc",
        "NAME": "dba",
        "USER": "sa",
        "PASSWORD": "#1Qazse4",
        "HOST": "172.16.20.3",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",  #SQL Server Native Client 11.0
        },
    },
}
