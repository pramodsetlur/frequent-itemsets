'''
Algorithm for PCY
_________________

1. Initial setup
    a. Generating the Frequent Item List of size 1 - FIL

k = 2
2. Hashing
    a. For all baskets:
        Read single basket
        generate all subsets of size k
        Hash them
    b. Create a bit map of the hash above

3. Generating the candiadate set
    a. For all baskets:
        Read basket
        Generate all subsets of size k
        For each item in the above subset:
            Generate a subset of k-1 size
            For each item in the subset:
                See if it is present in the FIL
            Check if item hashes to a frequent bucket
            Add it into the Candidate item set

4. Generating the frequent item set
    a. For all baskets:
        Generate subset of size k
        For each item in the subset:
            Check if it is present in the candidate item set
            Add it to the Candidate Dictionary with incrementing the count
    c. Clear FIL
    d. Iterate through the Candidate dictionary and check if the count is more than the support. Add it to FIL
    e. k++
'''



import sys

frequent_item_list = []
support = 0
bucket_size = 0

#Function to generate singleton frequent item set
def compute_singleton_set(singleton_dict, transaction):

    transaction_items = transaction.strip().split(',')

    for transaction in transaction_items:
        singleton_dict.setdefault(transaction, 1)
        count = singleton_dict.get(transaction)
        count = count + 1
        singleton_dict[transaction] = count
    return singleton_dict

def compute_frequent_singleton_set(input_file):
    #Converting command line params to integers from string

    #Computing the count of singleton items
    singleton_dict = {}
    with open(input_file) as file:
        for transaction in file:
            singleton_dict = compute_singleton_set(singleton_dict, transaction)

    #Computing frequent singleton item
    for item, count in singleton_dict.iteritems():
        if count >= support:
            frequent_item_list.append(item)

    #print the frequent singleton itemset
    frequent_item_list.sort()
    print frequent_item_list

    file.close()



if __name__ == '__main__':
    if 4 != len(sys.argv):
        print "Usage: python pramod_setlur_pcy.py [input.txt] [support] [hash_bucket_size]"
    else:
        input_file = sys.argv[1]
        support = sys.argv[2]
        bucket_size = sys.argv[3]

        support = int(support)
        bucket_size = int(bucket_size)

        compute_frequent_singleton_set(input_file)
