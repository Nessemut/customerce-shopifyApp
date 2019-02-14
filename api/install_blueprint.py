import requests
from flask import Blueprint, redirect, request
from app import shop
from appconfig import AppConfig

install_blueprint = Blueprint('install_blueprint', __name__, url_prefix='/install')


@install_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():

    auth = request.args.get("code")
    r = requests.post(
        AppConfig.get("access_token_url").format(shop.name),
        data={
            'client_id': AppConfig.get("API_KEY"),
            'client_secret': AppConfig.get("API_SECRET"),
            'code': auth
        }
    )

    shop.token = (r.json()["access_token"])
    return redirect(AppConfig.get("shop_apps_url").format(shop.name), code=302)


@install_blueprint.route('/', methods=['GET', 'POST'])
def install_redirect():

    return redirect(
        AppConfig.get("redirect_url").format(
            shop.name,
            AppConfig.get("API_KEY"),
            "{}/install/confirm".format(AppConfig.url),
            "read_customers"
        ), code=302)
