# frequent-itemsets
### INF-553 USC

##Assignment
####This is an assignment to find the frequent item sets of all sizes in various transactions using 3 algorithms

USAGE: $ python pramod_setlur_<ALGO_NAME>.py [INPUT_FILE] [SUPPORT_THRESHOLD] [HASH_BUCKET_SIZE]
Eg: $ python pramod_setlur_pcy.py data/input.txt 4 20
Link to standford's PPT of all the algorithms: http://infolab.stanford.edu/~ullman/mining/pdf/assoc-rules2.pdf

##PCY (Park-Chen-Yu) Algorithm
The PCY algorithm is an extension of the apriori algorithm. This provides a better utilization of memory by hashing. The candidate pairs is reduced to a drastic amount using this method.

##Minhash Algorithm
Item sets can be concluded as candidate itemsets if they can hash into a frequent bucket when they are hashed into a frequent bucket when all the hash functions are applied. This algorithm uses 2 hash functions

##Toivonen's Algortihm
[WIP]