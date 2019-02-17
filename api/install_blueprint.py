import requests
from flask import Blueprint, redirect, request
from appconfig import AppConfig
from model.shop import Shop
from dao.shop_dao import save_shop

install_blueprint = Blueprint('install_blueprint', __name__, url_prefix='/install')
current_shop = Shop


@install_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():

    auth = request.args.get("code")

    r = requests.post(
        AppConfig.get("access_token_url").format(current_shop.name),
        data={
            'client_id': AppConfig.get("API_KEY"),
            'client_secret': AppConfig.get("API_SECRET"),
            'code': auth
        }
    )

    current_shop.token = (r.json()["access_token"])
    save_shop(current_shop)
    return redirect(AppConfig.get("shop_apps_url").format(current_shop.name), code=302)


@install_blueprint.route('/redirect', methods=['GET', 'POST'])
def install_redirect():
    name = request.args['shop']
    current_shop.name = name

    return redirect(
        AppConfig.get("redirect_url").format(
            current_shop.name,
            AppConfig.get("API_KEY"),
            "{}/install/confirm".format(AppConfig.url),
            "read_customers"
        ), code=302)
