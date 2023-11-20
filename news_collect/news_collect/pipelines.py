# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from news_keywords.database_crud import DBOperations
import sys
sys.path.append("..")
# useful for handling different item types with a single interface


class NewsCollectPipeline:

    # db_obj = None
    # COL_NAME = "news_list2"
    #
    # def open_spider(self, spider):
    #     logging.warning("SPIDER STARTED")
    #     self.db_obj = DBOperations()
    #
    # def close_spider(self, spider):
    #     logging.warning("SPIDER STOPPED")
    #     self.db_obj.close_client()

    def process_item(self, item, spider):
        # self.db_obj.save_dict_as_one_to_db(item, self.COL_NAME)
        return item
