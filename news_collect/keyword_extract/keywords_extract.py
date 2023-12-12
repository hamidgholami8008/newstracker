class KeywordExtract:
    """
        This class is able to extract keywords from sentences
        with specifying the method of extraction.
    """

    def extract_keywords(self, the_input, name_of_sentence_key=""):
        """
        Extracts keywords from a collection of sentences
        :param the_input: it can be a json list or a list of sentences.
        :param name_of_sentence_key: Optional if the_input is a json, specify the name of the key for sentences.
        :return: the keywords list of dicts with sentence & keywords as keys
        """
