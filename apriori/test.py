# Written by Ningyuan Jiang

import apriori
import apriori_improved
import sys

if __name__ =='__main__':
    if len(sys.argv) > 1 and 'improved' not in sys.argv:
        apriori.apriori(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    if len(sys.argv) > 1 and 'improved' in sys.argv:
        apriori_improved.apriori(sys.argv[1], int(sys.argv[2]), sys.argv[3])