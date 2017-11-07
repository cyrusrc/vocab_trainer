old_path = 'assets\unused\dictionary_orig.txt'
new_path = 'assets\unused\dictionary.txt'

old_f = open(old_path)
lines = old_f.readlines()
old_f.close()

new_f = open(new_path, 'w')
new_lines = []

for line in lines:
    arr = line.partition(" (")
    new_lines.append(arr[0].lower() + "|-|(" + arr[2])

merged_lines = []

"""
below used to merge multiple definitions under same headword
"""
i = 0
while i < len(new_lines):
    line = new_lines[i].strip()
    arr = line.partition("|-|")
    word = arr[0]

    cursor = 1

    while i + cursor < len(new_lines) and word == new_lines[i + cursor].partition("|-|")[0]:
        nth_def_arr = new_lines[i + cursor].strip().partition("|-|")
        if cursor == 1:
            line = word + arr[1] + "[{}.] {}, [{}.] {}".format(cursor, arr[2], cursor + 1, nth_def_arr[2])
        else:
            line += ", [{}.] {}".format(cursor + 1, nth_def_arr[2])
        cursor += 1

    merged_lines.append(line + "\n")
    i += cursor

for line in merged_lines:
    new_f.write(line)

new_f.close()

"""
import json
import unicodedata

old_path = 'assets\unused\dictionary.json'
new_path = 'assets\unused\mw_new.txt'

new_mw = open(new_path, 'w')

with open(old_path) as data_file:
    data = json.load(data_file)

new_lines = []

for key in data:
    word = key.lower()
    definition = unicodedata.normalize('NFKD', data[key]).encode('ascii', 'ignore')
    new_lines.append("{}|-|{}\n".format(word, definition))

new_lines = sorted(new_lines)

for line in new_lines:
    new_mw.write(line)

new_mw.close()
"""
