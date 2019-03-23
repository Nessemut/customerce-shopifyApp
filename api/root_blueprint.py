from flask import Blueprint, render_template, make_response, redirect, request, abort, url_for, send_from_directory

from appconfig import AppConfig
from dao.shop_dao import is_registered, load_shop
from model.shop import Shop

root_blueprint = Blueprint('root_blueprint', __name__)
current_shop = Shop


@root_blueprint.route('/', methods=['GET', 'POST'])
def root():
    if request.args.get("shop") is not None:
        current_shop.name = request.args.get("shop").replace('.myshopify.com', '')

        # TODO: handle app's uninstall
        if is_registered(current_shop.name):
            shop = load_shop(current_shop.name)
            r = make_response(render_template('index.html', url=AppConfig.url, shop=shop))
            r.set_cookie('shop-name', shop.name)
            r.set_cookie('shop-token', shop.token)
            r.headers.set('X-Shopify-Access-Token', shop.token)

            return r

        else:
            return redirect(url_for("install_blueprint.install_redirect", shop=current_shop.name), code=302)
    else:
        abort(404)
