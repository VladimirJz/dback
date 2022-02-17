from .base import *
DATABASES = {
    "default": {
        "ENGINE": "sql_server.pyodbc",
        "NAME": "dba",
        "USER": "monitor",
        "PASSWORD": "#1Qazse4#",
        "HOST": "10.186.11.11\MSSQLServer2",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",  #SQL Server Native Client 11.0
        },
    },
}
