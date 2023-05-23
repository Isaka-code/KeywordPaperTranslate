import requests
from xml.etree import ElementTree as ET
from translate import translate_text


class PaperDataExtractor:
    def __init__(self, id_list):
        self.id_list = id_list

    def extract(self):
        # 各PubMed IDに対して、論文の詳細を取得
        base_url_efetch = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        )

        # データを保存するためのリストを作成
        data_list = []

        for id in self.id_list:
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
            if abstract is None:
                abstract_translated = None
            else:
                abstract_translated = translate_text(
                    abstract, src_lang="en", dest_lang="ja"
                )

            # リンクを作成
            link = f"https://pubmed.ncbi.nlm.nih.gov/{id}/"

            # データをリストに追加
            data_list.append(
                [link, title, year, authors, abstract, abstract_translated]
            )

        # データフレームを作成
        df = pd.DataFrame(
            data_list,
            columns=[
                "Link",
                "Title",
                "Year",
                "Authors",
                "Abstract",
                "Translated Abstract",
            ],
        )

        return df
