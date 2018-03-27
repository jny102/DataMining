# Written by Ningyuan Jiang
import itertools
import time

def read_data(input):
    with open(input) as f:
        dataset = [[int(x) for x in line.split()] for line in f]
    #dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]] # FIXME
    return dataset


def gen_C1(dataset):
    C1 = []
    for t in dataset:
        for i in t:
            if not [i] in C1:
                C1.append([i])
    C1.sort()
    return map(frozenset, C1)


def gen_Ck(L, k):
    Ck = []
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            list1, list2 = list(L[i]), list(L[j])
            list1, list2 = list1[:k-2], list2[:k-2]
            if list1 == list2:
                c = L[i] | L[j]
                #print c
                if not need_prune(c, L, k):
                    Ck.append(c)
    return Ck


def need_prune(c, L, k):
    s = set(itertools.combinations(c, k-1))
    for i in s:
        if frozenset(i) not in L:
            return True
    return False


def scan(dataset, Ck, msc):
    item_count = dict()
    for t in dataset:
        for i in Ck:
            if i.issubset(t):
                if item_count.has_key(i):
                    item_count[i] += 1
                else:
                    item_count[i] = 1
    Lk, Lk_count = [], {}
    for i in Ck:
        if item_count.has_key(i) and item_count[i] >= msc:
            Lk.append(i)
            Lk_count[i] = item_count[i]
        #else:
            #discard(dataset, i)
    return Lk, Lk_count


def apriori(input, msc, output):
    dataset = read_data(input)
    C1 =  gen_C1(dataset)
    L1, L_count = scan(dataset, C1, msc)
    L_final, k = [L1], 2
    while len(L_final[k - 2]) != 0:  # Stop when there is no more possible candidates
        Ck = gen_Ck(L_final[k-2], k)
        #truncate(dataset, Ck)  # Discard transactions that do not contain any of the candidates
        Lk, Lk_count = scan(dataset, Ck, msc)
        L_final.append(Lk)
        L_count.update(Lk_count)
        k += 1
    file = open(output, 'w+')
    for list in L_final:
        for i in list:
            s = ' '.join(str(s) for s in i)
            file.write(s)
            file.write(' (')
            file.write(str(L_count[i]))
            file.write(')\n')
    file.close()
