class WordDB:
    def __init__(self, word_list_path, dict_path):
        self.word_list = []
        self.word_list_indices_dict = {}
        self.dictionary = {}

        self.__read_words(word_list_path)
        self.__read_dict(dict_path)

    """
    Populates word list with words in order of their frequency (as
    determined by their order in the words file).
    """
    def __read_words(self, freq_path):
        with open(freq_path) as f:
            lines = f.readlines()
            for i in xrange(0, len(lines)):
                word = lines[i].strip()  # delete trailing newline
                if not word == "":  # don't add final empty line from words file
                    self.word_list.append(word)
                    self.word_list_indices_dict[word] = i

    """
    Populates dictionary with {word:definition} key:arg pairs.
    """
    def __read_dict(self, dict_path):
        with open(dict_path) as f:
            for line in f.readlines():
                arr = line.partition("|-|")
                word = arr[0]
                definition = arr[2].strip()  # delete trailing newline
                self.dictionary[word] = definition

    """
    Looks for word definition in instance's dictionary.
    """
    def look_up(self, word):
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            return None

    """
    Looks for index of word in instance's word_list
    """
    def get_word_list_index(self, word):
        if word in self.word_list_indices_dict:
            return self.word_list_indices_dict[word]
        else:
            return -1
