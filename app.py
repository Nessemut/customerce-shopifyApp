from firebase_admin import credentials, initialize_app
from flask import Flask
import logging
import sys

from appconfig import AppConfig
from model.shop import Shop



try:
    cred = credentials.Certificate('db_credentials.json')
    initialize_app(cred, {
        'databaseURL': AppConfig.get("db_url")
    })
except FileNotFoundError:
    logging.error('Database credentials file not found')
    sys.exit()


app = Flask(__name__, static_folder="static", template_folder="static/templates")
