from flask import Blueprint, redirect, request

from dao.shop_dao import save_shop, load_shop
from model.shop import Shop
from util.shopify_api import ShopifyApi

install_blueprint = Blueprint('install_blueprint', __name__, url_prefix='/install')


@install_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():
    shop = Shop()
    shop.name = request.args['shop'].replace('.myshopify.com', '')
    api = ShopifyApi(shop)
    auth = request.args.get("code")
    api.confirm_installation(auth)

    try:
        token = shop.token
        shop = load_shop(shop.name)
        shop.token = token
    except TypeError:
        pass

    last_billing = shop.billing_id
    url = api.add_billing(last_billing)
    return redirect(url, code=302)


@install_blueprint.route('/redirect', methods=['GET', 'POST'])
def install_redirect():
    shop = Shop()
    shop.name = request.args['shop']
    api = ShopifyApi(shop)
    return redirect(api.redirect_to_install_confirmation(), code=302)
