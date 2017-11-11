# vocab_trainer

Overview: A trainer that quizzes the user on the definitions of
words and keeps track of their rising and falling vocabulary level.
Words given as questions are drawn from a slice of words with
difficulty levels near the user's current vocabulary level. 

The program relies on two classes: vocab_trainer and word_db.
Its assets are a list of words ordered by frequency
and a dictionary of the format "word|-|definition\n".

**word_db** manages a list of words read in from the words
file and a dictionary read from the dictionary file.
It also contains a dictionary mapping words to their index in
an instance's word_list -- this is used as a proxy for calculating
word frequency, which in turn serves as a proxy for word difficulty.

This looks like:
- word_list = ["the", "of", "and", ...]
- dictionary: {"the": "[1.] (v. i.) See Thee., [2.] (definite article.) A word placed before nouns...", ...}
- word_list_indices_dict: {"the": 0, "of": 1, "and": 2, ...}

**vocab_trainer** implements a user interface and methods for generating,
displaying, and scoring questions. A question consists of a word the user
is asked to define by selecting its definition from a multiple choice list
and N false definitions (modifiable). The **meat of the logic here** is in
get_word_index and adjust_vocab_level.

- **get_word_index** generates word indices based a gamma distribution
parameterized with the user's vocab level and (a fraction of)
the vocab_trainer instance's word_list length. See method comment
for further explanation.
- **adjust_vocab_level** scores the user's response to a question and
modifies the user vocab level (stored as trainer.user_vocab_level)
accordingly. See method comment for further explanation.
