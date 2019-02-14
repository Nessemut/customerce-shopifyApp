from flask import Blueprint, render_template, make_response, redirect, request, abort
from app import shop
from appconfig import AppConfig

root_blueprint = Blueprint('root_blueprint', __name__)


@root_blueprint.route('/', methods=['GET', 'POST'])
def root():
    token = shop.token

    if token is not None:
        r = make_response(render_template('index.html', url=AppConfig.url, shop=shop))
        r.headers.set('X-Shopify-Access-Token', shop.token)
        return r
    elif request.args.get("shop") is not None:
        shop.name = request.args.get("shop").replace('.myshopify.com', '')
        return redirect((AppConfig.url + "/install"), code=302)
    else:
        # TODO: think of a solution for this uncommon case
        abort(404)
