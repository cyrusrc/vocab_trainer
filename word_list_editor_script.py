from word_db import WordDB

words_path = 'assets/count_1w.txt'
words_pruned_path = 'assets/words.txt'

dict_path = "assets/dictionary.txt"

db = WordDB(words_path, dict_path)

words_f = open(words_path)
lines = words_f.readlines()
words_f.close()

words_pruned_f = open(words_pruned_path, 'w')

# ditch counts -- index in list gives relative frequency, so counts unneeded
for l in lines:
    word = l.split()[0]
    if db.look_up(word):
        words_pruned_f.write(word + "\n")

words_pruned_f.close()
