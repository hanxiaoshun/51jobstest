jon_tmp = []
jon_tmp_uni = []
with open('files/uniq_company.txt', 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        line = line.replace('\n', '')
        lines = line.split('\t')
        if lines[0].__len__() > 0:
            if lines[0] not in jon_tmp:
                print(line)
                jon_tmp.append(lines[0])