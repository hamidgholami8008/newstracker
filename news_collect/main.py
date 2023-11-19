from news_keywords.database_crud import DBOperations
from news_keywords.keywords_extract import KeywordsExtract
from hazm import *
import pandas as pd
import streamlit as st

db = DBOperations()

cur = db.get_cursor_find('news_list')
keyword_extract = KeywordsExtract(Normalizer(), POSTagger('pos_tagger.model'))
for doc in cur:
    keywords = keyword_extract.get_tokenized_text(doc['title'])
    for keyword in keywords:
        keywords_pos_tagged = keyword_extract.find_keywords_of_sentence(keyword)
        noun_keywords = keyword_extract.get_noun_keywords_from_list(keywords_pos_tagged)
        print(noun_keywords)



