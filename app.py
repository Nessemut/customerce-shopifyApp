import firebase_admin
from flask import Flask
from appconfig import AppConfig
import pyrebase
from model.shop import Shop


app = Flask(__name__, static_folder="static", template_folder="static/templates")
shop = Shop

'''
firebase_admin.initialize_app(options={
    'databaseURL': 'https://customerce-e8bd4.firebaseio.com'
})'''