from flask import Blueprint, redirect, request, url_for
from appconfig import AppConfig
from dao.shop_dao import load_shop, save_shop
import api.root_blueprint

admin_blueprint = Blueprint('admin_blueprint', __name__, url_prefix='/admin')


# TODO: add token security here
@admin_blueprint.route('/button_settings', methods=['GET', 'POST'])
def button_settings():
    shop = load_shop(request.args.get("shop"))

    phone = request.form.get("phone")
    message = request.form.get("message")
    position = request.form.get("position")

    shop.button_pos = position
    shop.phone = phone
    shop.predefined_text = message

    save_shop(shop)
    return redirect(url_for('root_blueprint.root', shop=shop.name), code=302)


@admin_blueprint.route('/sticky_bar_settings', methods=['GET', 'POST'])
def sticky_bar_settings():
    shop = load_shop(request.args.get("shop"))

    sticky_bar_enabled = request.form.get("sticky_bar_enabled")
    sticky_bar_color = request.form.get("sticky_bar_color")
    sticky_label_text = request.form.get("sticky_label_text")
    sticky_bar_text_color = request.form.get("sticky_bar_text_color")

    shop.sticky_bar_enabled = (sticky_bar_enabled == "enable")
    shop.sticky_bar_color = sticky_bar_color
    shop.sticky_label_text = sticky_label_text
    shop.sticky_bar_text_color = sticky_bar_text_color

    save_shop(shop)
    return redirect(url_for('root_blueprint.root', shop=shop.name), code=302)
