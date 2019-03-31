from urllib import parse
from os import remove
from appconfig import AppConfig


def build_text_script(shop):
    var = (
            "var div = document.createElement('a');\n"
            "div.className = 'customerce-button';\n"
            "div.style.width = '190px';\n"
            "div.style.heigth = '25px';\n"
            "div.style.textAlign = 'center';\n"
            "div.style.position = 'fixed';\n"
            "div.style.bottom = '1em';\n"
            "div.style.borderRadius = '18px'\n"
            "div.style.float = '" + shop.button_pos + "';\n"
            "div.style." + shop.button_pos + " = '1em';\n"
            "div.style.background = '#" + shop.sticky_bar_color + "';\n"
            "div.href = \"https://api.whatsapp.com/send?phone=" +
            shop.phone + "&text=" + parse.quote(shop.predefined_text) + "\";\n"
            "div.innerHTML ="
            "\"<font color='#" + shop.sticky_bar_text_color + "'>" +
            shop.sticky_label_text + "</font>\";\n"
            "document.getElementsByTagName(\"body\")[0].appendChild(div);\n"
    )
    return var


def build_whatsapp_button_script(shop):
    var = (
            "var div = document.createElement('a');\n"
            "div.className = 'customerce-button';\n"
            "div.style.width = '64px';\n"
            "div.style.heigth = '64px';\n"
            "div.style.position = 'fixed';\n"
            "div.style.bottom = '1em';\n"
            "div.style.float = '" + shop.button_pos + "';\n"
            "div.style." + shop.button_pos + " = '1em';\n"
            "div.href = \"https://api.whatsapp.com/send?phone=" +
            shop.phone + "&text=" + parse.quote(shop.predefined_text) + "\";\n"                                                
            "div.innerHTML =\"<img src='" + AppConfig.url + '/shop_scripts/whatsappicon' + "'>\";\n"
            "document.getElementsByTagName(\"body\")[0].appendChild(div);\n"
    )
    return var


def build_script(shop):
    if shop.sticky_bar_enabled:
        if shop.sticky_label_text is not None and shop.sticky_label_text != '':
            var = build_text_script(shop)
        else:
            var = build_whatsapp_button_script(shop)
    else:
        var = ''

    path = AppConfig.get("shop_scripts_directory") + '{}.js'.format(shop.name)

    try:
        remove(path)
    except FileNotFoundError:
        pass

    f = open(path, 'a')
    f.write(var)
