import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD='django.db.models.AutoField'


DATABASES = {
    "default": {
        "ENGINE": "sql_server.pyodbc",
        "NAME": "dba",
        "USER": "monitor",
        "PASSWORD": "#1Qazse4#",
        "HOST": "10.186.11.11\MSSQLServer2",
        "PORT": "1414",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",  #SQL Server Native Client 11.0
        },
    },
}

INSTALLED_APPS = ("db",)
