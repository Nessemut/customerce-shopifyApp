from flask import Blueprint, redirect, request, url_for, make_response, render_template

from dao.shop_dao import load_shop, save_shop
from model.shopify_api import ShopifyApi

admin_blueprint = Blueprint('admin_blueprint', __name__, url_prefix='/admin')


@admin_blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        shop = load_shop(request.cookies.get("shop-name"))
    except ValueError:
        return make_response(render_template('401.html'), 401)

    if request.cookies.get("shop-token") is None or request.cookies.get("shop-token") != shop.token:
        return make_response(render_template('401.html'), 401)

    shop.phone = request.form.get("phone").replace('+', '')
    shop.predefined_text = request.form.get("message")
    shop.button_pos = request.form.get("position")
    shop.sticky_bar_enabled = (request.form.get("sticky_bar_enabled") == 'enable')
    shop.sticky_bar_color = request.form.get("sticky_bar_color")
    shop.sticky_label_text = request.form.get("sticky_label_text")[0:40]
    shop.sticky_bar_text_color = request.form.get("sticky_bar_text_color")

    save_shop(shop)
    api = ShopifyApi()
    api.shop = shop
    api.update_sticky_bar(shop)

    return redirect(url_for('root_blueprint.root', shop=shop.name), code=302)
