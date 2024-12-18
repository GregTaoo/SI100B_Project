import json

LANG = 0
# 0: Chinese Simplified, 1: Chinese Traditional, 2: English

STRINGS = {}
LANG_DICT = {
    0: 'zh_cn',
    1: 'zh_tr',
    2: 'en_us',
    3: 'jp_jp'
}


def set_language(lang: int):
    global LANG
    LANG = lang
    load_strings()


def load_strings():
    with open('assets/lang/' + LANG_DICT[LANG] + '.json', 'r', encoding='utf-8') as file:
        global STRINGS
        STRINGS = json.load(file)


def text(string: str):
    return TranslatableText(string)


def literal(string: str):
    return Text(string)


class Text:

    def __init__(self, string):
        self.string = string

    def format(self, *args):
        return self.string.format(*args)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def get(self):
        return self.string


class TranslatableText(Text):

    def __init__(self, key):
        super().__init__(key)

    def format(self, *args):
        return STRINGS[self.string].format(*args) or '?'

    def __str__(self):
        return STRINGS[self.string] or '?'

    def __repr__(self):
        return STRINGS[self.string] or '?'

    def get(self):
        return STRINGS[self.string] or '?'