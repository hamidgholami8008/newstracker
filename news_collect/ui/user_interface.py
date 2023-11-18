import streamlit as st
import pandas as pd

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
    the_word = st.text_input(placeholder="مانند: بانک", label="ورودی تگ", max_chars=20, label_visibility="collapsed", help="تگ")

with col2:
    """
    .نگ را وارد کرده تا اخبار مرتبط با آن را ببینید
    """
