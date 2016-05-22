import os
from base64 import b64encode


DEBUG = True  # Flask debug, set it to False on production
APP_DEBUG = False  # Non-flask debug
LOG_FILE = 'debug.log'


DB_DRIVER = 'postgresql'
DB_USER = 'alex'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_NAME = 'filmadvisor'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = ""

secret_file = os.path.join(BASE_DIR, '.secret')
if os.path.exists(secret_file):
    # Read SECRET_KEY from .secret file
    f = open(secret_file, 'rb')
    SECRET_KEY = b64encode(f.read().strip()).decode()
    f.close()
else:
    # Generate SECRET_KEY & save it away
    temp = os.urandom(32)
    f = open(secret_file, 'wb')
    f.write(temp)
    f.close()
    SECRET_KEY = b64encode(temp).decode()
    # Modify .gitignore to include .secret file
    gitignore_file = os.path.join(BASE_DIR, '../.gitignore')
    f = open(gitignore_file, 'a+')
    if '.secret' not in f.readlines() and '.secret\n' not in f.readlines():
        f.write('.secret\n')
    f.close()
