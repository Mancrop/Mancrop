import opencc
import unicodedata

def string_normalize(text: str) -> str:
    text = unicodedata.normalize('NFKC', text)
    text = opencc.OpenCC('t2s').convert(text)
    opencc.OpenCC()
    return text

if __name__ == "__main__":
    s1 = "我的青春戀愛物語果然有問題"
    print(string_normalize(s1))