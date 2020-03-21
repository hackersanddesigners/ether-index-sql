import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pymysql.cursors
import get_from_db
from datetime import datetime

# -- load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# -- setup db connection
connection = pymysql.connect(host=os.getenv('DB_HOST'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'),
                             db=os.getenv('DB_NAME'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

