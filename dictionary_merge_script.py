mw_path = "assets/unused/mw_new.txt"
oed_path = "assets/unused/oed.txt"
combined_path = "assets/combined_dict.txt"

mw_f = open(mw_path)
oed_f = open(oed_path)
combined_f = open(combined_path, 'w')

mw_lines = mw_f.readlines()
oed_lines = oed_f.readlines()

mw_f.close()
oed_f.close()

combined_dict = {}
combined_lines = []

for entry in mw_lines:
    arr = entry.partition("|-|")
    combined_dict[arr[0]] = arr[2]

for entry in oed_lines:
    arr = entry.partition("|-|")
    if arr[0] not in combined_dict:
        combined_dict[arr[0]] = arr[2]

for key in combined_dict.keys():
    combined_lines.append(key + "|-|" + combined_dict[key])

combined_lines = sorted(combined_lines)

for line in combined_lines:
    combined_f.write(line)

combined_f.close()
