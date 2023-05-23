from googletrans import Translator


def translate_text(text, src_lang="ja", dest_lang="en"):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text


if __name__ == "__main__":
    # 使用例
    # ユーザーからの入力を受け取ります
    japanese_text = input("キーワードを入力してください（日本語OK）：")  # 例："胃癌　手術　栄養"
    english_text = translate_text(japanese_text)
    print(english_text)  # 例：Gastric cancer surgical nutrition
