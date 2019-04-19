from flask import Blueprint, render_template, make_response, redirect, request, abort, url_for

from appconfig import AppConfig
from dao.shop_dao import is_registered, load_shop
from util.shopify_api import ShopifyApi

root_blueprint = Blueprint('root_blueprint', __name__)


@root_blueprint.route('/', methods=['GET', 'POST'])
def root():

    if request.args.get("shop") is not None:
        name = request.args.get("shop").replace('.myshopify.com', '')

        if is_registered(name):
            shop = load_shop(name)
            api = ShopifyApi(shop)
            if api.token_valid():
                if api.activate_billing() == 422:
                    return make_response(render_template('422.html'), 422)
                r = make_response(render_template('index.html', url=AppConfig.url, shop=shop))
                r.set_cookie('shop-name', shop.name)
                r.set_cookie('shop-token', shop.token)
                r.headers.set('X-Shopify-Access-Token', shop.token)
                return r

        return redirect(url_for("install_blueprint.install_redirect", shop=name), code=302)
    else:
        abort(404)
