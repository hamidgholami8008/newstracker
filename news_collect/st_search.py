import streamlit as st
from news_keywords.database_crud import DBOperations


# st.set_page_config(layout='wide')

page_bg_img = '''
    <style>
    .stApp {
        background-image: linear-gradient( 95.2deg, rgba(173,252,234,1) 26.8%, rgba(192,229,246,1) 64% );
        background-size: cover;
    }
    </style>
    '''

st.markdown(page_bg_img, unsafe_allow_html=True)

#title
title_style = "<style>h2 {text-align: start; width:500px; direction: rtl; font-family: bnazanin;}</style>"
st.markdown(title_style, unsafe_allow_html=True)
st.columns(2)[1].header("جست و جوء کلیدواژه")


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: end;
            direction: rtl;
        }

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: start;
            direction: rtl;
        }
    </style>
    """,unsafe_allow_html=True
)
col1, col2= st.columns(2)
with col1:
    st.markdown("<style>input { direction: rtl; height: 50px;} span.st-emotion-cache-0 {display: none}</style>", unsafe_allow_html=True)
    input_st = st.text_input(placeholder="مانند:  صندوق سرمایه گذاری", label="ورودی متن", max_chars=20, label_visibility="collapsed", help="تگ")

with col2:
    st.markdown("<style> .helper {padding: 20px;}</style>"
                "<p class='helper'>متن را وارد کرده تا مطالب مرتبط با آن را ببینید:</p>", unsafe_allow_html=True)


db_obj = DBOperations()

array_of_input = input_st.split()

result = None
array_of_results = []

for input_word in array_of_input:
    array_of_results.append(db_obj.find_keyword(keyword=input_word, collection_name="news_full"))

content_style = """
    <style>
    .content
    {
        text-align: start:
        height: 150px;
        width: 700px;
        box-sizing: border-box;
        padding: 20px;
        margin: 10px;
        background-image: linear-gradient(to right, #F6F2FF, #FBF1F1);

        border-radius: 16px;
        direction: rtl;
    }
    .sentence
    {
        text-align: start;
        direction: rtl;
    }
    a
    {
        text-decoration: none;
    }
    </style>
"""
for result in array_of_results:
    for doc in result:
        st.markdown(content_style, unsafe_allow_html=True)
        st.write(f"<div class='content'>"
                 f"<a href='{doc['link']}'>{doc['title']}</a>"
                 f"<p class='sentence'>{(doc['summary'])[:170]}</p>"
                 f"</div>", unsafe_allow_html=True)
