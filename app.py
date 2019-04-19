import logging
import sys
from flask import Flask

from appconfig import AppConfig

from firebase_admin import credentials, initialize_app

try:
    cred = credentials.Certificate('db_credentials.json')
    initialize_app(cred, {
        'databaseURL': AppConfig.get("db_url")
    })
except FileNotFoundError:
    logging.error('Database credentials file not found')
    sys.exit()


app = Flask(__name__, static_folder="static", template_folder="static/templates")

from api.admin_blueprint import admin_blueprint
from api.install_blueprint import install_blueprint
from api.root_blueprint import root_blueprint
from api.script_blueprint import script_blueprint


app.register_blueprint(root_blueprint)
app.register_blueprint(install_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(script_blueprint)


if __name__ == '__main__':
    app.run(
        ssl_context=AppConfig.get("ssl_context"),
        host=AppConfig.get("app_listen_host"),
        port=AppConfig.get("app_port"),
    )
