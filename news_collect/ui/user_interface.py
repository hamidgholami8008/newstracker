import streamlit as st
from news_keywords.database_crud import DBOperations
from news_keywords.keywords_extract import KeywordsExtract
import pandas as pd
import sys
sys.path.append("..")

st.set_page_config(layout='wide')

#title
title_style = "<style>h1 {text-align: center;}</style>"
st.markdown(title_style, unsafe_allow_html=True)
st.columns(3)[2].header("تگ خبری")


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: start;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)
col1, col2 = st.columns(2)
with col1:
    sentence = st.text_input(placeholder="مانند:  بانک سینا تعهدات تکلیفی سال اول خود در خصوص نهضت ملی مسکن را اجرایی کرده است", label="ورودی تگ", max_chars=20, label_visibility="collapsed", help="تگ")

with col2:
    """
    .نگ را وارد کرده تا اخبار مرتبط با آن را ببینید
    """



# keyword_extract = KeywordsExtract()

# keyword_extract.get_tokenized_text(sentence)

db = DBOperations()
df = db.get_cursor_find("news_list")
df = pd.DataFrame(df, columns=("link", "summary", "title"))
st.dataframe(df, height=600, hide_index=True)
