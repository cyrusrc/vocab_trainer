import numpy.random as rand
from word_db import WordDB


class VocabTrainer:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, words_path, dictionary_path, num_mult_choice, initial_vocab_level):
        self.word_db = WordDB(words_path, dictionary_path)
        self.num_mult_choice = num_mult_choice
        self.trainer_active = True
        self.user_vocab_level = float(initial_vocab_level)

    @staticmethod
    def welcome_msg():
        return "\n---***---\nWelcome to VocabTrainer.\nEnter ` at any time " \
               "to exit.\nSelect the correct definition from the given options " \
               "by entering its letter.\nAs you play, your vocab level will " \
               "rise and fall with your performance.\n---***---\n"

    def show_vocab_level(self):
        print "Vocab level now {}\n".format(self.user_vocab_level)

    """
    Adjusts user vocab level based on whether they correctly answered the question.
    Score is calculated by comparing the index (which is a proxy for frequency
    rank) of the question's word with the mean index expected based on the user's
    vocab level.

    Score varies between 1.0 and 25.0. The lower limit is necessary because of
    the gamma distribution's properties; the upper limit is set such that
    MAX_VOCAB_LEVEL * (WORD_LIST_LENGTH * 0.05)* = a value slightly higher than the
    number of words in the word list (44,506 words). That ensures that words presented
    to a user at MAX_VOCAB_LEVEL will be much more likely to come from the end of the
    word list (before smoothing to account for indices generated that are > its length --
    see explanation in get_word_index()).

    *This is the expected value of numbers drawn from the gamma distribution with
    parameters SHAPE = MAX_VOCAB_LEVEL and SCALE = (WORD_LIST_LENGTH * 0.05).

    Note: both positive and negative scores are dampened to prevent extreme
    vocab level fluctuations from a single question.
    """
    def adjust_vocab_level(self, word, was_correct):
        word_index = self.word_db.get_word_list_index(word)
        # The mean of a gamma distribution == shape * scale, or, in this case (vocab level) * (an
        # experimentally determined fraction of the word list length)
        expected_vocab_index = self.user_vocab_level * (len(self.word_db.word_list) * 0.05)
        score = float(word_index) / expected_vocab_index

        if was_correct:
            # we don't want the score to rise dramatically because the user got one hard word correct
            self.user_vocab_level += min(score, 2.0)
            if self.user_vocab_level > 25.0:
                self.user_vocab_level = 25.0
        else:
            # if the score is > 1, it is harder than the expected difficulty for the user's current vocab level.
            # accordingly, the user's vocab level shouldn't be changed if they get such a word wrong.
            # if, on the other hand, the score is low (indicating the word should be easy), points should be deducted.
            # note: 2 chosen experimentally but somewhat arbitrarily
            self.user_vocab_level -= max(2 - score, 0)
            if self.user_vocab_level < 1.0:
                self.user_vocab_level = 1.0

    @staticmethod
    def display_question(q):
        print "WORD: {}\n".format(q[0])
        for i in xrange(0, len(q[1])):
            print "{}.) {}\n".format(VocabTrainer.alphabet[i], q[1][i])

    """
    Returns an index drawn from a gamma distribution with shape determined
    by user vocab level and scale determined by length of the word list.
    This distribution is substantially right-skewed with shape values near 1
    and approaches a normal distribution centered on shape_param * scale_param
    as shape increases.

    Note also: to smooth returned indices when the user vocab level approaches
    the maximum vocab level, the index is reduced by a second number drawn
    from an exponential distribution with a scale determined again by the
    length of the word list IF AND ONLY IF the initial value returned by the
    gamma distribution >= the length of the word list.
    """
    def get_word_index(self):
        ceil = len(self.word_db.word_list)
        level = self.user_vocab_level
        g_scale = ceil * 0.05
        e_scale = ceil * 0.1

        val = int(rand.gamma(level, g_scale))
        # Smooth values that are > ceil
        if val >= ceil:
            val = int(ceil - rand.exponential(e_scale))

        return val

    """
    Returns a word, an array of N definitions (one of which is correct),
    and the index of the correct definition. N is determined by
    self.num_mult_choice.
    """
    def get_question(self):
        word_index = self.get_word_index()
        word = self.word_db.word_list[word_index]
        word_def = self.word_db.look_up(word)

        # will contain both genuine definition and bogus definitions
        definitions = [word_def]

        # generate bogus definitions
        for i in xrange(0, self.num_mult_choice - 1):
            # TODO: consider if this is the best way to generate indices of bogus definitions
            false_word_index = int(word_index + rand.uniform(-1000, 1000))

            # make sure index is not the same as that of the chosen word and is within the defined range
            while false_word_index == word_index or not 0 <= false_word_index < len(self.word_db.word_list):
                false_word_index = int(word_index + rand.uniform(-1000, 1000))

            false_word = self.word_db.word_list[false_word_index]

            definitions.append(self.word_db.look_up(false_word))

        rand.shuffle(definitions)

        return word, definitions, definitions.index(word_def)


def main():
    words_path = "assets/words.txt"
    dictionary_path = "assets/dictionary.txt"
    # Sets number of definitions per question at 5, initializes uer vocab to 1.0.
    trainer = VocabTrainer(words_path, dictionary_path, 5, 1.0)

    print trainer.welcome_msg()

    # trainer control structure
    while trainer.trainer_active:
        trainer.show_vocab_level()

        q = trainer.get_question()
        trainer.display_question(q)

        cmd = raw_input(">> ").lower()

        # input control structure
        if cmd == "`":
            trainer.trainer_active = False
            print "Exiting trainer..."
            continue
        elif cmd == "":
            cmd = raw_input("Please enter a valid letter command: ")
        while len(cmd) > cmd not in VocabTrainer.alphabet[0:trainer.num_mult_choice]:
            cmd = raw_input("Please enter a valid letter command: ")

        was_correct = False
        if list(VocabTrainer.alphabet).index(cmd) == q[2]:
            was_correct = True

        if was_correct:
            print "Correct!"
        else:
            print "Incorrect. The correct definition is:\n{}".format(q[1][q[2]])

        trainer.adjust_vocab_level(q[0], was_correct)


if __name__ == '__main__':
    main()
