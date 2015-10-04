# frequent-itemsets

##Assignment
####This is an assignment to find the frequent item sets of all sizes in various transactions using 3 algorithms

USAGE: $ python pramod_setlur_<ALGO_NAME>.py [INPUT_FILE] [SUPPORT_THRESHOLD] [HASH_BUCKET_SIZE]
Eg: $ python pramod_setlur_pcy.py data/input.txt 4 20

##PCY (Park-Chen-Yu) Algorithm
The PCY algorith is an extension of the apriori algorithm. This provides a better utilization of memory by hashing. The candidate pairs is reduced to a drastic amount using this method.

Link to standford's PPT of PCY algorithm: http://infolab.stanford.edu/~ullman/mining/pdf/assoc-rules2.pdf

##Minhash Algorithm
