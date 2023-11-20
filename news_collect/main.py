from news_keywords.database_crud import DBOperations
from news_keywords.keywords_extract import KeywordsExtract
from hazm import *
import pandas as pd
import streamlit as st
import json


st.set_page_config(layout='wide')

#title
title_style = "<style>h1 {text-align: center;}</style>"
st.markdown(title_style, unsafe_allow_html=True)
st.columns(3)[2].header("استخراج کلیدواژه از متن اخبار")


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: end;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: center;
        } 
        div[data-testid="column"]:nth-of-type(3)
        {
            text-align: start;
        } 
    </style>
    """,unsafe_allow_html=True
)
col1, col2, col3 = st.columns(3)
with col1:
    input_st = st.text_input(placeholder="مانند:  جمله اول,جمله دوم,جمله سوم", label="ورودی تگ", max_chars=500, label_visibility="collapsed", help="تگ")

with col2:
    """
    .متن را وارد کرده تا کلیدواژه های آن را ببینید
    """
with col3:
    uploaded_file = st.file_uploader(label="فرستادن فایل", type="json", label_visibility="hidden")


# keyword_extract = KeywordsExtract()

# keyword_extract.get_tokenized_text(sentence)

# db = DBOperations()
# cur = db.get_cursor_find('news_list')
# for doc in cur:
#     keywords = keyword_extract.find_keywords_of_sentence(doc['title'])
#     noun_keywords = keyword_extract.get_noun_keywords_from_list(keywords)
#     keywords_dict = {'sentence': doc['title'], 'keywords': noun_keywords}
#     list_of_keywords_dict.append(keywords_dict)

keyword_extract = KeywordsExtract(Normalizer(), POSTagger('pos_tagger.model'))
keywords_dict = {}
list_of_keywords_dict = []
sentences = input_st.split(",")

if uploaded_file is None:
    for sentence in sentences:
        keywords = keyword_extract.find_keywords_of_sentence(sentence)
        noun_keywords = keyword_extract.get_noun_keywords_from_list(keywords)
        keywords_dict = {'sentence': sentence, 'keywords': noun_keywords}
        list_of_keywords_dict.append(keywords_dict)

    if list_of_keywords_dict is not None:
        df = pd.DataFrame(list_of_keywords_dict)
        df.rename(columns={"sentence": "جمله", "keywords":"کلیدواژه"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, column_order={"کلیدواژه", "جمله"})
else:
    dict_of_uploaded = json.load(uploaded_file)
    for doc in dict_of_uploaded:
        keywords = keyword_extract.find_keywords_of_sentence(doc['title'])
        noun_keywords = keyword_extract.get_noun_keywords_from_list(keywords)
        keywords_dict = {'sentence': doc['title'], 'keywords': noun_keywords}
        list_of_keywords_dict.append(keywords_dict)

    if list_of_keywords_dict is not None:
        df = pd.DataFrame(list_of_keywords_dict)
        df.rename(columns={"sentence": "جمله", "keywords":"کلیدواژه"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, column_order={"کلیدواژه", "جمله"})


