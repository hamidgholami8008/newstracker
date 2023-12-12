from keyword_extract.keywords_extract_context import KeywordExtractContext
from keyword_extract.hazm_keywords_extract import HazmKeywordsExtract
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
    div[data-testid="textInputRootElement"] {
        width: 500px
        height: 50px
    }
    </style>
'''

loading_state = '''
    <div class="loader">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
    </div>
'''

loading_state_style = '''
    <style>
    body {
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: #f1f1f1;
    }
    
    .loader {
        position: relative;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: linear-gradient(#f07e6e, #84cdfa, #5ad1cd);
        animation: animate 1.2s linear infinite;
        top: 50%;
        left: 46%;
    }
    
    @keyframes animate {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    .loader span {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: linear-gradient(#f07e6e, #84cdfa, #5ad1cd);
    }
    
    .loader span:nth-child(1) {
        filter: blur(5px);
    }
    
    .loader span:nth-child(2) {
        filter: blur(10px);
    }
    
    .loader span:nth-child(3) {
        filter: blur(25px);
    }
    
    .loader span:nth-child(4) {
        filter: blur(50px);
    }
    
    .loader:after {
        content: '';
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        bottom: 10px;
        background: #f1f1f1;
        border: solid white 10px;
        border-radius: 50%;
    }
    </style>
'''

loading_state_remove = '''
    <style>
        .loader {
            display: none;
        }
    </style>
'''

hint_text_style = '''
    <style>
        .hint_txt {
            height: 50px;
            width: 320px;
            background-color: #ffffff;
            border-radius: 10px;
            text-align : center;
            padding: 13px;
            position: absolute;
            top: 50%;
            left: 41%;
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

streamlit_columns_style = '''
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
'''

streamlit_dataframe_hide_style = '''
    <style>
        .stDataFrame {
            display: none;
        }
    </style>
'''

streamlit_dataframe_show_style = '''
    <style>
        .stDataFrame {
            display: inline;
        }
    </style>
'''

st.markdown(streamlit_dataframe_hide_style, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(hint_text_style, unsafe_allow_html=True)
st.markdown(col_name_input_style, unsafe_allow_html=True)
st.markdown(loading_state_style, unsafe_allow_html=True)


@st.cache_data
def show_title():
    title_style = "<style>h1 {text-align: center;}</style>"
    st.markdown(title_style, unsafe_allow_html=True)
    st.columns(3)[2].header("استخراج کلیدواژه از متن اخبار")


def show_dict_in_streamlit(the_dict_or_list: dict | list):

    if the_dict_or_list is not None:
        df = pd.DataFrame(the_dict_or_list)
        df.rename(columns={"sentence": "جمله", "keywords":"کلیدواژه"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, column_order={"کلیدواژه", "جمله"}, height=300)


def change_dataframe_style(enabled: bool):
    if enabled:
        st.markdown(streamlit_dataframe_show_style, unsafe_allow_html=True)
    else:
        st.markdown(streamlit_dataframe_hide_style, unsafe_allow_html=True)


show_title()

st.markdown(streamlit_columns_style,unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    input_st = st.text_input(placeholder="مانند:  جمله اول,جمله دوم,جمله سوم",
                             label="ورودی تگ",
                             max_chars=500,
                             label_visibility="collapsed",
                             help="تگ")

with col2:
    """
    .متن را وارد کرده تا کلیدواژه های آن را ببینید
    """
with col3:
    uploaded_file = st.file_uploader(label="فرستادن فایل", type="json", label_visibility="hidden")

normalizer = Normalizer()
pos_tag_obj = POSTagger(model='pos_tagger.model')
keyword_extract = KeywordExtractContext(HazmKeywordsExtract(pos_tag_obj))
list_of_keywords_dict = []
sentences = input_st.split(",")

if input_st != "":
    change_dataframe_style(True)

if uploaded_file is None:
    list_of_keywords_dict = keyword_extract.extract_keywords(the_input=sentences)

    show_dict_in_streamlit(list_of_keywords_dict)


else:
    col_name_input = st.text_input(placeholder="نام ستون جملات", label="col_name", label_visibility="hidden")

    if col_name_input == "":
        st.markdown("<div class='hint_txt'><p>.نام ستون خالی است. لطفا وارد کنید</p></div>",
                    unsafe_allow_html=True)

    else:
        try:
            st.markdown(loading_state, unsafe_allow_html=True)

            change_dataframe_style(True)

            dict_of_uploaded = json.load(uploaded_file)
            list_of_keywords_dict = keyword_extract.extract_keywords(the_input=dict_of_uploaded,
                                                                     name_of_sentence_key=col_name_input)
            show_dict_in_streamlit(list_of_keywords_dict)

            st.markdown(loading_state_remove, unsafe_allow_html=True)

            json_string = json.dumps(list_of_keywords_dict)
            st.download_button(data=json_string, label="JSON دانلود فایل به صورت", file_name="sentence_keywords.json",
                               use_container_width=True)
        except:
            st.markdown(loading_state_remove, unsafe_allow_html=True)
            st.markdown("<div class='hint_txt'><p>.نام ستون اشتباه است. لطفا دوباره تلاش کنید</p></div>",
                        unsafe_allow_html=True)
