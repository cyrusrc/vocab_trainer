old_path = 'assets\oed.txt'
new_path = 'assets\oed_clean.txt'

old_oed = open(old_path)
lines = old_oed.readlines()
old_oed.close()

new_oed_f = open(new_path, 'w')
new_lines = []

for line in lines:
    arr = line.partition("|")
    word = arr[0].upper().lower()
    defn = arr[2].strip()
    l = "{}|{}\n".format(word, defn)
    new_lines.append(l)

for line in new_lines:
    new_oed_f.write(line)

new_oed_f.close()
