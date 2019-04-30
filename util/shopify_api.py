import datetime
from json import dumps, loads

import requests

from appconfig import AppConfig
from dao.shop_dao import save_shop
from util.script_tag_builder import build_script


class ShopifyApi:

    def __init__(self, shop):
        self.shop = shop

    url = AppConfig.get("shop_admin_url")

    def get_url(self, context):
        return self.url.format(self.shop.name, context)

    def get_header(self):
        header = {'X-Shopify-Access-Token': self.shop.token}
        return header

    def token_valid(self):
        url = self.get_url('shop.json')
        header = self.get_header()
        r = requests.get(url, headers=header)
        return not r.status_code == 401

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

    def update_sticky_bar(self):
        url = self.get_url('script_tags.json')
        header = self.get_header()
        header['Content-Type'] = 'application/json'
        build_script(self.shop)

        if self.shop.script_tag_id is None:

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
                self.shop.script_tag_id = loads(r.content)['script_tag']['id']

    def add_billing(self, last_billing):
        url = self.get_url('recurring_application_charges.json')
        header = self.get_header()
        header['Content-Type'] = 'application/json'
        trial_days = self.get_trial_period(last_billing)

        r = requests.post(
            url,
            data=dumps({
                "recurring_application_charge": {
                    "name": "Recurring charge",
                    "price": 2.99,
                    "test": AppConfig.get("environment") == "development",
                    "trial_days": trial_days,
                    "return_url": "http://{}.myshopify.com/admin/apps".format(self.shop.name)
                }
            }),
            headers=header
        )

        if r.status_code == 201:
            rdict = loads(r.content)['recurring_application_charge']
            self.shop.billing_id = rdict['id']
            save_shop(self.shop)
            return rdict['confirmation_url']

        return None

    def activate_billing(self):
        url = self.get_url('recurring_application_charges/{}/activate.json'.format(self.shop.billing_id))
        header = self.get_header()
        header['Content-Type'] = 'application/json'
        r = requests.post(url, headers=header)
        return r.status_code

    def get_trial_period(self, last_billing):
        default_trial_period = AppConfig.get("default_trial_period")
        if last_billing is None:
            return default_trial_period

        url = self.get_url('recurring_application_charges/{}.json'.format(last_billing))
        header = self.get_header()
        header['Content-Type'] = 'application/json'

        r = requests.get(url, headers=header)
        try:
            rdict = loads(r.content)['recurring_application_charge']
        except KeyError:
            return default_trial_period

        activated = datetime.datetime.strptime(rdict['activated_on'], '%Y-%m-%d')
        today = datetime.datetime.today()
        period = default_trial_period - (today-activated).days

        if period < 0:
            return 0
        if period > default_trial_period:
            return default_trial_period
        return period
