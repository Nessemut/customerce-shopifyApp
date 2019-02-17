from firebase_admin import db

from model.shop import Shop

ref = db.reference('shop')


def save_shop(shop):
    ref.set({
        shop.name: {
            'name': shop.name,
            'token': shop.token,
            'phone': shop.phone,
            'predefined_text': shop.predefined_text,
            'button_pos': shop.button_pos,
            'sticky_bar_enabled': shop.sticky_bar_enabled,
            'sticky_bar_color': shop.sticky_bar_color,
            'sticky_label_text': shop.sticky_label_text,
            'sticky_bar_text_color': shop.sticky_bar_text_color,
        }
    })


def load_shop(name):
    shop = Shop
    data = ref.child(name).get()

    shop.name = data['name']
    shop.token = data['token']
    shop.button_pos = data['button_pos']
    shop.sticky_bar_enabled = data['sticky_bar_enabled']

    try:
        shop.phone = data['phone']
    except KeyError:
        shop.phone = None
    try:
        shop.predefined_text = data['predefined_text']
    except KeyError:
        shop.predefined_text = None
    try:
        shop.sticky_label_text = data['sticky_label_text']
    except KeyError:
        shop.sticky_label_text = None
    try:
        shop.sticky_bar_color = data['sticky_bar_color']
    except KeyError:
        shop.sticky_bar_color = '33CC33'
    try:
        shop.sticky_bar_text_color = data['sticky_bar_text_color']
    except KeyError:
        shop.sticky_bar_text_color = 'FFFFFF'
    return shop


def is_registered(name):
    return ref.child(name).get() is not None
