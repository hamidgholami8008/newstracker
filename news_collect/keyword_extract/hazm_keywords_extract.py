import json
import re
from hazm import *
import itertools
from .keywords_extract import KeywordExtract
from collections import Counter


class HazmKeywordsExtract(KeywordExtract):

    def __init__(self, pos_tagger_obj: POSTagger):

        self.__pos_tagger_obj = pos_tagger_obj
        self.__the_normalizer = Normalizer()

    def __pos_tag_sentence(self, sentence: str):
        # tokenizing the sentence (finding key-words)
        tokenized_text = self.__get_tokenized_text(sentence)

        # tagging the position of tokens
        tokenized_text_pos_tagged: list = self.__pos_tagger_obj.tag(tokens=tokenized_text)

        return tokenized_text_pos_tagged

    def __pos_tag_list_of_sentences(self, the_list: list):

        # creating a temporary dictionary for storing the keywords
        temp_dict = {}
        # iterating the list to find keywords
        for item in the_list:
            # storing keywords in a dict with key 'sentence'
            temp_dict['sentence'] = self.__pos_tag_sentence(item)

        return temp_dict

    def __get_tokenized_text(self, text: str):
        # normalizing every sentence
        normalize_text = self.__the_normalizer.normalize(text)

        # tokenizing the sentence (finding key-words)
        tokenized_text = [word_tokenize(txt) for txt in sent_tokenize(normalize_text)]

        # converting list[list[str]] to list[str]
        tokenized_text_flatten: list = list(itertools.chain.from_iterable(tokenized_text))

        return tokenized_text_flatten

    @staticmethod
    def __get_noun_pos_from_list(tokenized_text_pos_tagged: list):

        # creating a temporary list to store noun pos
        noun_keywords = []

        # iterating the list to separate the nouns from other positions
        for tag_tuple in tokenized_text_pos_tagged:

            if tag_tuple[1] == 'NOUN':
                noun_keywords.append(tag_tuple[0])

        noun_keywords = set(noun_keywords)
        noun_keywords = list(noun_keywords)

        return noun_keywords

    def find_noun_pos_of_sentence(self, sentence: str):
        tokenized_text_pos_tagged = self.__pos_tag_sentence(sentence)
        return self.__get_noun_pos_from_list(tokenized_text_pos_tagged)

    @staticmethod
    def __perform_re(sentences: list):
        """
        performs regular expressions patterns to modify the text
        :param sentences: the input list to perform regular expressions
        :return: returns a modified list
        """
        # The regular expression pattern for removing short words
        short_word_pattern = r'\b\w{1,2}\b'

        # The regular expression pattern for removing simple plural words
        characters_to_remove = r"هایی"
        plural_word_pattern_1 = rf"{characters_to_remove}(?=\b|\s)"

        # The regular expression pattern for removing simple plural words
        characters_to_remove = r"ها"
        plural_word_pattern_2 = rf"{characters_to_remove}(?=\b|\s)"

        # The regular expression pattern for removing english words
        english_re = r'^[a-zA-Z\s]+$'

        # the regular expression pattern for removing special characters
        special_characters_pattern = r'[.,!-]'

        temp_list = []

        for sentence in sentences:
            word = re.sub(short_word_pattern, '', sentence)
            word = re.sub(plural_word_pattern_1, '', word)
            word = re.sub(plural_word_pattern_2, '', word)
            word = re.sub(special_characters_pattern, '', word)
            word = re.sub(english_re, '', word)
            if word != "" and word != "٫":
                temp_list.append(word)

        return temp_list

    def remove_not_repeated_words(self, list_of_docs):

        # Step 1: Flatten the list of keywords
        all_keywords = [keyword for document in list_of_docs for keyword in document["keywords"]]

        # Step 2: Count the occurrences of each word
        word_counts = Counter(all_keywords)

        # Step 3: Filter out words that occur only once
        non_singleton_words = {word for word, count in word_counts.items() if count > 1}

        # Step 4: Update the keywords list in each document
        for document in list_of_docs:
            document["keywords"] = [keyword for keyword in document["keywords"] if keyword in non_singleton_words]

        return list_of_docs

    @staticmethod
    def append_noun_keywords_to_file(tokenized_text_pos_tagged: list, file: str):
        with open(file, "a") as f:
            for tag_tuple in tokenized_text_pos_tagged:
                if tag_tuple[1] == 'NOUN':
                    f.write(tag_tuple[0] + "\n")

    # extracts the keywords from the json list then saves them into a list of dictionaries and returns it
    def __extract_keywords_of_json_to_dict(self, json_list: list, sentences_label: str):
        # creating a temporary list to store keywords as a json list
        list_of_keywords_dict = []

        # iterating documents in the json list
        for doc in json_list:
            # finding keywords in every sentence of json list
            keywords = self.__pos_tag_sentence(doc[sentences_label])
            # separating noun keywords from the other positions in a sentence
            noun_keywords = self.__get_noun_pos_from_list(keywords)
            # removing short words from the list
            noun_keywords = self.__perform_re(noun_keywords)
            # storing noun keywords as a dict
            keywords_dict = {'sentence': doc[sentences_label], 'keywords': noun_keywords}
            # storing the dict in the list
            list_of_keywords_dict.append(keywords_dict)

        list_of_keywords_dict = self.remove_not_repeated_words(list_of_keywords_dict)
        return list_of_keywords_dict

    # extracts the keywords from the input list then saves them into a list of dictionaries and returns it
    def __extract_keywords_of_list_to_dict(self, the_list):
        # creating a temporary list to store keywords as a json list
        list_of_keywords_dict = []
        # iterating sentences in the list
        for sentence in the_list:
            # finding keywords in every sentence in the list
            keywords = self.__pos_tag_sentence(sentence)
            # separating noun keywords from the other positions in a sentence
            noun_keywords = self.__get_noun_pos_from_list(keywords)
            # storing noun keywords as a dict
            keywords_dict = {'sentence': sentence, 'keywords': noun_keywords}
            # storing the dict in the list
            list_of_keywords_dict.append(keywords_dict)

        list_of_keywords_dict = self.remove_not_repeated_words(list_of_keywords_dict)
        return list_of_keywords_dict

    def extract_keywords(self, the_input, name_of_sentence_key=""):

        if name_of_sentence_key == "":
            return self.__extract_keywords_of_list_to_dict(the_input)

        return self.__extract_keywords_of_json_to_dict(the_input, name_of_sentence_key)
