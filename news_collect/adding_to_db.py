from keyword_extract.hazm_keywords_extract import HazmKeywordsExtract
from keyword_extract.database_crud import DBOperations
from hazm import *

keyword_extract = HazmKeywordsExtract(pos_tagger_obj=POSTagger('pos_tagger.model'))
db_obj = DBOperations()

cur = db_obj.get_cursor_find("news_title_link_sentence")

new_dict_list = []

for doc in cur:
    new_dict_list.append({
        'title': doc['title'],
        'link': doc['link'],
        'summary': doc['sentence'],
        'keywords': keyword_extract.find_noun_pos_of_sentence(doc['sentence'])
    })

db_obj.save_list_to_db(new_dict_list, 'news_full')
