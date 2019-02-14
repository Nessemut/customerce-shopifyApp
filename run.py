from api.root_blueprint import root_blueprint
from api.install_blueprint import install_blueprint
from api.admin_blueprint import admin_blueprint
from appconfig import AppConfig
from app import app


app.register_blueprint(root_blueprint)
app.register_blueprint(install_blueprint)
app.register_blueprint(admin_blueprint)

if __name__ == '__main__':
    app.run(
        ssl_context=AppConfig.get("ssl_context"),
        host=AppConfig.get("app_host"),
        port=AppConfig.get("app_port"),
    )
