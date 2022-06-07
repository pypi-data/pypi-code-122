import re
import json
import urllib.parse


def bracket_content(text):
    if not isinstance(text, str):
        text = str(text)
    inner_text = re.findall(r'[(](.*?)[)]', text)
    if inner_text:
        return inner_text[0]
    return ''


def cn_brackets_content(text):
    if not isinstance(text, str):
        text = str(text)
    inner_text = re.findall(r'[（](.*)[）$]', text)
    if inner_text:
        return inner_text[0]
    return ''


def get_characters(text):
    if not isinstance(text, str):
        text = str(text)
    characters = re.findall(r'[\u4e00-\u9fa5]', text)
    return ''.join(characters)


def get_num(text, origin=False):
    if not isinstance(text, str):
        text = str(text)
    num = re.findall(r'\d+\.?\d*', text)
    if num:
        if origin:
            return num[0]
        return float(num[0])
    return 0


def multi_get(value, li, default=None):
    if isinstance(value, dict):
        for key in li:
            value = value.get(key)
            index = li.index(key) + 1
            if not value:
                return default
            if index < len(li):
                return multi_get(value, li[index:])
            else:
                return value

    if not isinstance(value, dict):
        return value


def multi_get_num(value, li, origin=False):
    text = multi_get(value, li)
    return get_num(text, origin)


def url2dict(url=''):
    try:
        d = urllib.parse.urlparse(url)
        dat = urllib.parse.parse_qs(d.query)
        dat['urlparse_ParseResult'] = d
        return dat
    except:
        return url


def new_json_loads(wait_load):
    if wait_load == "null":
        return json.loads(wait_load)

    if wait_load == "true":
        return json.loads(wait_load)

    if wait_load == "false":
        return json.loads(wait_load)

    if isinstance(wait_load, float):
        return wait_load

    if isinstance(wait_load, int):
        return wait_load

    if isinstance(wait_load, str):
        try:
            elem_loaded = json.loads(wait_load)
            if isinstance(elem_loaded, str):
                return elem_loaded
            return new_json_loads(elem_loaded)
        except:
            return wait_load

    if isinstance(wait_load, dict):
        item = {}
        for x, y in wait_load.items():
            item[x] = new_json_loads(y)
        return item

    if isinstance(wait_load, list):
        item = []
        for x in wait_load:
            item.append(new_json_loads(x))
        return item
