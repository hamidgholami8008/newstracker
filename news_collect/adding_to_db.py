from news_keywords.keywords_extract import KeywordsExtract
from news_keywords.database_crud import  DBOperations
from hazm import *

keyword_extract = KeywordsExtract(the_normalizer=Normalizer(), pos_tagger_obj=POSTagger('pos_tagger.model'))
db_obj = DBOperations()

cur = db_obj.get_cursor_find("news_title_link_sentence")

new_dict_list = []

for doc in cur:
    new_dict_list.append({
        'title': doc['title'],
        'link': doc['link'],
        'summary': doc['sentence'],
        'keywords': keyword_extract.find_noun_keywords_of_sentence(doc['sentence'])
    })

db_obj.save_list_to_db(new_dict_list, 'news_full')
