from pubmed import PubMed
from excel_writer import ExcelWriter
from translate import translate_text


def main(japanese_keywords: str, filename: str):
    # キーワードを英語に翻訳
    keywords = translate_text(japanese_keywords, src_lang="ja", dest_lang="en")

    # PubMedで検索
    pubmed = PubMed(keywords)
    papers = pubmed.search()

    # Excelに書き出し
    writer = ExcelWriter(japanese_keywords)
    writer.write(papers, filename)

    print(
        f"Excel file has been created for the keywords: {japanese_keywords}."
    )


if __name__ == "__main__":
    # ユーザーからの入力を受け取る
    japanese_keywords = input("キーワードを入力してください（日本語OK）：")
    main(japanese_keywords)
