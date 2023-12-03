from news_keywords.keywords_extract import KeywordsExtract
from hazm import *
import pandas as pd
import streamlit as st
import json


st.set_page_config(layout='wide')

col_name_input_style = '''
    <style>
    input[aria-label="col_name"] {
        text-align : center;
    } 
    .st-emotion-cache-1qnt2ew > div:nth-child(2) > div {
        box-width : 100px;
    }
    </style>
'''

page_bg_img = '''
    <style>
    .stApp {
        background-image: linear-gradient( 95.2deg, rgba(173,252,234,1) 26.8%, rgba(192,229,246,1) 64% );
        background-size: cover;
    }
    </style>
    '''

st.markdown(page_bg_img, unsafe_allow_html=True)


@st.cache_data
def show_title():
    title_style = "<style>h1 {text-align: center;}</style>"
    st.markdown(title_style, unsafe_allow_html=True)
    st.columns(3)[2].header("استخراج کلیدواژه از متن اخبار")


def show_dict_in_streamlit(the_dict_or_list: dict | list):

    if the_dict_or_list is not None:
        df = pd.DataFrame(the_dict_or_list)
        df.rename(columns={"sentence": "جمله", "keywords":"کلیدواژه"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, column_order={"کلیدواژه", "جمله"})


show_title()

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


keyword_extract = KeywordsExtract(Normalizer(), POSTagger('pos_tagger.model'))
list_of_keywords_dict = []
sentences = input_st.split(",")

if uploaded_file is None:
    list_of_keywords_dict = keyword_extract.extract_keywords_of_list_to_dict(sentences)

    show_dict_in_streamlit(list_of_keywords_dict)

else:
    col_name_input = st.text_input(placeholder="نام ستون جملات", label="col_name", label_visibility="hidden")

    st.markdown(col_name_input_style, unsafe_allow_html=True)

    if col_name_input == "":
        st.text("نام ستون خالی است. لطفا وارد کنید.")

    else:
        dict_of_uploaded = json.load(uploaded_file)
        list_of_keywords_dict = keyword_extract.extract_keywords_of_json_to_dict(dict_of_uploaded, col_name_input)

        show_dict_in_streamlit(list_of_keywords_dict)

        json_string = json.dumps(list_of_keywords_dict)
        st.download_button(data=json_string, label="JSON دانلود فایل به صورت", file_name="sentence_keywords.json", use_container_width=True)
