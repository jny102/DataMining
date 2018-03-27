# Written by Ningyuan Jiang
import itertools
import time
import collections

def read_data(input):
    with open(input) as f:
        dataset = [[int(x) for x in line.split()] for line in f]
    #dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]] # FIXME
    return dataset


def gen_L1(dataset, msc):
    L1 = []
    L1_info = dict()
    for t in dataset:
        for i in t:
            s = frozenset([i])
            if not L1_info.has_key(s):
                L1.append([i])
                L1_info[s] = [1, [dataset.index(t)]]
            else:
                L1_info[s][0] += 1
                L1_info[s][1].append(dataset.index(t))
    remove = []
    for i in L1:
        s = frozenset(i)
        if L1_info[s][0] < msc:
            remove.append(i)
            del L1_info[s]
    L1 = filter(lambda x: x not in remove, L1)
    L1.sort()
    return map(frozenset, L1), L1_info


def gen_Lk(L, L_info, k, msc):
    Lk = []
    Lk_info = dict()
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            list1, list2 = list(L[i])[:k-2], list(L[j])[:k-2]
            if list1 == list2:  # FIXME: Any k-2 elements same
            #if len(L[i].intersection(L[j])) == k-2:
                x, y = L[i], L[j]
                ex, ey = L_info[x][1], L_info[y][1]
                c = x | y   # Frozenset of a candidate
                intersection = list(set(ex).intersection(ey))
                Lk_info[c] = [len(intersection), intersection]
                if Lk_info[c][0] < msc:
                    del Lk_info[c]
                else:
                    Lk.append(c)
    Lk = map(frozenset, sorted(list(Lk)))
    return Lk, Lk_info


def apriori(input, msc, output):
    dataset = read_data(input)
    L1, L_info = gen_L1(dataset, msc)
    L_final, k = [L1], 2
    while len(L_final[k-2]) != 0:
        Lk, Lk_info = gen_Lk(L_final[k-2], L_info, k, msc)
        L_final.append(Lk)
        L_info.update(Lk_info)
        k += 1
    file = open(output, 'w+')
    # TODO: Sort 2D into 1D ???
    for list in L_final:
        for i in list:
            s = ' '.join(str(s) for s in i)
            file.write(s)
            file.write(' (')
            file.write(str(L_info[i][0]))
            file.write(')\n')
    file.close()
