import re


def split_kanji_kana(text):
    if text is None:
        return [], []
    kanji_list = re.findall(r'[\u4E00-\u9FAF]+', text)  # 匹配汉字
    kana_list = re.findall(r'[\u3040-\u309F\u30A0-\u30FF]+', text)  # 匹配假名
    return kanji_list, kana_list

if __name__ == '__main__':
    kanji_list, kana_list = split_kanji_kana('')
    print()