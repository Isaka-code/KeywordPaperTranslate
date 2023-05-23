import requests
from xml.etree import ElementTree as ET
from translate import translate_text


class PubMed:
    def __init__(self, keywords):
        self.keywords = keywords

    def search(self):
        # PubMed APIのURLを定義
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        # パラメータを定義
        params = {
            "db": "pubmed",
            "term": self.keywords,
            "retmax": 10,  # 最大抽出数
            "sort": "relevance",
            "retmode": "json",
        }

        # APIリクエストを送信
        response = requests.get(base_url, params=params)
        data = response.json()

        # PubMed IDのリストを取得
        id_list = data["esearchresult"]["idlist"]

        # 各PubMed IDに対して、論文の詳細を取得
        base_url_efetch = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        )

        # データを保存するためのリストを作成
        data_list = []

        for id in id_list:
            params_efetch = {"db": "pubmed", "id": id, "retmode": "xml"}
            response_efetch = requests.get(
                base_url_efetch, params=params_efetch
            )
            paper_data = response_efetch.text  # XMLをパースする

            # XMLから情報を抽出
            root = ET.fromstring(paper_data)
            title = root.find(".//ArticleTitle").text
            year = root.find(".//PubDate/Year").text
            authors_elements = root.findall(".//Author")
            try:
                authors = ", ".join(
                    [
                        f"{author.find('ForeName').text} {author.find('LastName').text}"
                        for author in authors_elements
                    ]
                )
            except:
                authors = ""
            abstract = root.find(".//AbstractText").text

            # 要約を日本語に翻訳
            try:
                abstract_translated = translate_text(
                    abstract, src_lang="en", dest_lang="ja"
                )
            except:
                abstract_translated = None

            # リンクを作成
            link = f"https://pubmed.ncbi.nlm.nih.gov/{id}/"

            # データをリストに追加
            data_list.append(
                [link, title, year, authors, abstract, abstract_translated]
            )

        return data_list
