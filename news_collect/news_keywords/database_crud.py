from pymongo import MongoClient


class DBOperations:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database('news_sentences')

    def __set_or_create_collection(self, collection_name: str):

        try:
            col = self.db.get_collection(collection_name)
        except NameError:
            print(str(NameError) + "\n New collection is created")
            col = self.db.create_collection(collection_name)

        return col

    def extract_field_of_db_to_list(self, collection_name: str, field_name: str):

        col = self.__set_or_create_collection(collection_name)

        return col.find({field_name: 1})

    def save_list_to_db(self, the_list: list, collection_name: str):

        col = self.__set_or_create_collection(collection_name)

        for item in the_list:
            col.insert_one(item)

        print('list in inserted successfully')

    def save_dict_as_one_to_db(self, the_dict: dict, collection_name: str):

        col = self.__set_or_create_collection(collection_name)

        col.insert(the_dict)

    def close_client(self):
        self.client.close()