import os
import pandas as pd


class ExcelWriter:
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    def write(self, papers, filename):
        # データフレームを作成
        df = pd.DataFrame(
            papers,
            columns=[
                "Link",
                "Title",
                "Year",
                "Authors",
                "Abstract",
                "Translated Abstract",
            ],
        )

        if os.path.isfile(filename):
            # Excelファイルが存在する場合、ExcelWriterを使用して新しいシートを追加
            with pd.ExcelWriter(
                filename,
                engine="openpyxl",
                mode="a",
                if_sheet_exists="replace",
            ) as writer:
                df.to_excel(writer, sheet_name=self.sheet_name, index=False)
        else:
            # Excelファイルが存在しない場合、新しいファイルを作成
            df.to_excel(filename, sheet_name=self.sheet_name, index=False)
