from flask import Blueprint, redirect, request

from dao.shop_dao import save_shop
from model.shopify_api import ShopifyApi

install_blueprint = Blueprint('install_blueprint', __name__, url_prefix='/install')
api = ShopifyApi()


@install_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():
    auth = request.args.get("code")
    api.confirm_installation(auth)
    save_shop(api.shop)
    return redirect(api.get_url('apps'), code=302)


@install_blueprint.route('/redirect', methods=['GET', 'POST'])
def install_redirect():
    api.shop.name = request.args['shop']
    return redirect(api.redirect_to_install_confirmation(), code=302)
