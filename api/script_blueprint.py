from flask import Blueprint, send_from_directory, request, abort

from appconfig import AppConfig

script_blueprint = Blueprint('script_blueprint', __name__, url_prefix='/shop_scripts')


@script_blueprint.route('/')
def get_button():
    shop_name = request.args.get("shop")
    if shop_name is not None:
        return send_from_directory(
            AppConfig.get("shop_scripts_directory"),
            '{}.js'.format(shop_name.replace('.myshopify.com', '')))
    else:
        abort(404)


@script_blueprint.route('/whatsappicon')
def get_whatsapp_icon():
    return send_from_directory('static/images', 'whatsapp_button.png')
