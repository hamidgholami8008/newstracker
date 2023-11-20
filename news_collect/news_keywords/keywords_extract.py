from hazm import *
import itertools


class KeywordsExtract:

    def __init__(self, the_normalizer: Normalizer, pos_tagger_obj: POSTagger):

        self.pos_tagger_obj = pos_tagger_obj
        self.the_normalizer = the_normalizer

    def find_keywords_of_sentence(self, sentence: str):
        # tokenizing the sentence (finding key-words)
        tokenized_text = self.get_tokenized_text(sentence)

        # tagging the position of tokens
        tokenized_text_pos_tagged: list = self.pos_tagger_obj.tag(tokens=tokenized_text)

        return tokenized_text_pos_tagged

    def find_keywords_of_list_of_sentences(self, the_list: list):

        temp_dict = {}
        for item in the_list:

            temp_dict['sentence'] = self.find_keywords_of_sentence(item)

        return temp_dict

    def get_tokenized_text(self, text: str):
        # normalizing every sentence
        normalize_text = self.the_normalizer.normalize(text)

        # tokenizing the sentence (finding key-words)
        tokenized_text = [word_tokenize(txt) for txt in sent_tokenize(normalize_text)]

        # converting list[list[str]] to list[str]
        tokenized_text_flatten: list = list(itertools.chain.from_iterable(tokenized_text))

        return tokenized_text_flatten

    @staticmethod
    def get_noun_keywords_from_list(tokenized_text_pos_tagged: list):

        noun_keywords = []

        for tag_tuple in tokenized_text_pos_tagged:

            if tag_tuple[1] == 'NOUN':
                noun_keywords.append(tag_tuple[0])

        return noun_keywords

    @staticmethod
    def append_noun_keywords_to_file(tokenized_text_pos_tagged: list, file: str):
        with open(file, "a") as f:
            for tag_tuple in tokenized_text_pos_tagged:
                if tag_tuple[1] == 'NOUN':
                    f.write(tag_tuple[0] + "\n")
