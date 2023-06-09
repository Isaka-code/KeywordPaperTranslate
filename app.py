import streamlit as st
from main import main


st.title("PubMed Paper Searcher")

# ユーザーからの入力を受け取る
japanese_keywords = st.text_input("キーワードを入力してください（日本語OK）：")

if st.button("Search"):
    if japanese_keywords:
        filename = "papers.xlsx"

        # メイン関数を実行
        st.write("Searching papers...")
        main(japanese_keywords, filename)
        st.success("Excel file has been created successfully.")

        # ダウンロードボタンを作成
        with open(filename, "rb") as f:
            bytes_data = f.read()
        st.download_button(
            label="Download Excel file",
            data=bytes_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.error("Please input keywords.")
