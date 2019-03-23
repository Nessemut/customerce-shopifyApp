import requests
from json import dumps, loads
from appconfig import AppConfig
from model.shop import Shop
from dao.shop_dao import save_shop
from util.script_tag_builder import build_script


class ShopifyApi:
    shop = Shop
    url = AppConfig.get("shop_admin_url")

    def get_url(self, context):
        return self.url.format(self.shop.name, context)

    def get_header(self):
        header = {'X-Shopify-Access-Token': self.shop.token}
        return header

    def confirm_installation(self, auth):
        r = requests.post(
            AppConfig.get("access_token_url").format(self.shop.name),
            data={
                'client_id': AppConfig.get("API_KEY"),
                'client_secret': AppConfig.get("API_SECRET"),
                'code': auth
            }
        )

        self.shop.token = (r.json()["access_token"])

    def redirect_to_install_confirmation(self):
        url = AppConfig.get("redirect_url").format(
            self.shop.name,
            AppConfig.get("API_KEY"),
            "{}/install/confirm".format(AppConfig.url),
            AppConfig.get("scopes"))
        return url

    def update_sticky_bar(self, shop):
        url = self.get_url('script_tags.json')
        header = self.get_header()
        header['Content-Type'] = 'application/json'
        build_script(shop)

        if shop.script_tag_id is None:

            r = requests.post(
                url,
                data=dumps({
                    "script_tag": {
                        "event": "onload",
                        "src": AppConfig.url + '/shop_scripts'
                    }
                }),
                headers=header
            )

            if r.status_code == 201:
                shop.script_tag_id = loads(r.content)['script_tag']['id']
                save_shop(shop)
