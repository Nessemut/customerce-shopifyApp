import json
import logging


class AppConfig:
    dictdump = {}
    url = None

    @classmethod
    def __init__(cls):
        try:
            cls.dictdump = json.loads(open('app_config.json').read())
        except FileNotFoundError:
            logging.error('Config file not found')
        AppConfig.url = AppConfig.generate_url()

    @classmethod
    def get(cls, p):
        try:
            return cls.dictdump[p]
        except KeyError:
            logging.error('Incorrect key {}'.format(p))
            return None

    @classmethod
    def generate_url(cls):
        if AppConfig.get("ssl_enabled"):
            protocol = "https"
        else:
            protocol = "http"

        host = AppConfig.get("app_host")
        port = AppConfig.get("app_port")

        url = "{}://{}:{}".format(protocol, host, port)
        return url


AppConfig.__init__()
