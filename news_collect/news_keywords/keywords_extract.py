from hazm import *
import itertools


class KeywordsExtract:

    def __init__(self, the_normalizer: Normalizer, pos_tagger_obj: POSTagger):

        self.pos_tagger_obj = pos_tagger_obj
        self.the_normalizer = the_normalizer

    def __find_keywords_of_sentence(self, sentence: str):
        # tokenizing the sentence (finding key-words)
        tokenized_text = self.__get_tokenized_text(sentence)

        # tagging the position of tokens
        tokenized_text_pos_tagged: list = self.pos_tagger_obj.tag(tokens=tokenized_text)

        return tokenized_text_pos_tagged

    def __find_keywords_of_list_of_sentences(self, the_list: list):

        # creating a temporary dictionary for storing the keywords
        temp_dict = {}
        # iterating the list to find keywords
        for item in the_list:
            # storing keywords in a dict with key 'sentence'
            temp_dict['sentence'] = self.__find_keywords_of_sentence(item)

        return temp_dict

    def __get_tokenized_text(self, text: str):
        # normalizing every sentence
        normalize_text = self.the_normalizer.normalize(text)

        # tokenizing the sentence (finding key-words)
        tokenized_text = [word_tokenize(txt) for txt in sent_tokenize(normalize_text)]

        # converting list[list[str]] to list[str]
        tokenized_text_flatten: list = list(itertools.chain.from_iterable(tokenized_text))

        return tokenized_text_flatten

    @staticmethod
    def __get_noun_keywords_from_list(tokenized_text_pos_tagged: list):

        # creating a temporary list to store noun keywords
        noun_keywords = []

        # iterating the list to separate the nouns from other positions
        for tag_tuple in tokenized_text_pos_tagged:

            if tag_tuple[1] == 'NOUN':
                noun_keywords.append(tag_tuple[0])

        return noun_keywords

    def find_noun_keywords_of_sentence(self, sentence: str):
        tokenized_text_pos_tagged = self.__find_keywords_of_sentence(sentence)
        return self.__get_noun_keywords_from_list(tokenized_text_pos_tagged)

    @staticmethod
    def append_noun_keywords_to_file(tokenized_text_pos_tagged: list, file: str):
        with open(file, "a") as f:
            for tag_tuple in tokenized_text_pos_tagged:
                if tag_tuple[1] == 'NOUN':
                    f.write(tag_tuple[0] + "\n")

    def extract_keywords_of_json_to_dict(self, json_list: list, sentences_label: str):
        # creating a temporary list to store keywords as a json list
        list_of_keywords_dict = []

        # iterating documents in the json list
        for doc in json_list:
            # finding keywords in every sentence of json list
            keywords = self.__find_keywords_of_sentence(doc[sentences_label])
            # separating noun keywords from the other positions in a sentence
            noun_keywords = self.__get_noun_keywords_from_list(keywords)
            # storing noun keywords as a dict
            keywords_dict = {'sentence': doc[sentences_label], 'keywords': noun_keywords}
            # storing the dict in the list
            list_of_keywords_dict.append(keywords_dict)

        return list_of_keywords_dict

    def extract_keywords_of_list_to_dict(self, the_list):
        # creating a temporary list to store keywords as a json list
        list_of_keywords_dict = []
        # iterating sentences in the list
        for sentence in the_list:
            # finding keywords in every sentence in the list
            keywords = self.__find_keywords_of_sentence(sentence)
            # separating noun keywords from the other positions in a sentence
            noun_keywords = self.__get_noun_keywords_from_list(keywords)
            # storing noun keywords as a dict
            keywords_dict = {'sentence': sentence, 'keywords': noun_keywords}
            # storing the dict in the list
            list_of_keywords_dict.append(keywords_dict)

        return list_of_keywords_dict

