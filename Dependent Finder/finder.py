input_file = 'dependent_list.txt'

lines = []
with open(input_file) as f:
    for line in f:
        if not len(line.strip()):
            continue

        lines.append(line.strip())

lhs_symbol = set()
rhs_symbol = set()
for line in lines:
    lhs, rhs = [e.strip() for e in line.split(':')]

    lhs_symbol.add(lhs)
    for s in rhs.split(' '):
        rhs_symbol.add(s.strip())

used_symbol = set()
for line in lines:
    lhs, rhs = [e.strip() for e in line.split(':')]

    for s in rhs.split(' '):
        if not (s in lhs_symbol):
            if not (s in used_symbol):
                print(s)
                used_symbol.add(s)
