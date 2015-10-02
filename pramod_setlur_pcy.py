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
import itertools

frequent_item_list = {}

#Function to generate singleton frequent item set
def compute_singleton_set(transaction):
    transaction_items = transaction.strip().split(',')

    for transaction in transaction_items:
        frequent_item_list.setdefault(transaction, 1)
        count = frequent_item_list.get(transaction)
        count = count + 1
        frequent_item_list[transaction] = count

def compute_frequent_sets_pcy(input_file, support, bucket_size):
    #Converting command line params to integers from string
    support = int(support)
    bucket_size = int(bucket_size)

    for transaction in open(input_file):
        compute_singleton_set(transaction)
    print frequent_item_list

if __name__ == '__main__':
    if 4 != len(sys.argv):
        print "Usage: python pramod_setlur_pcy.py [input.txt] [support] [hash_bucket_size]"
    else:
        input_file = sys.argv[1]
        support = sys.argv[2]
        bucket_size = sys.argv[3]

        compute_frequent_sets_pcy(input_file, support, bucket_size)
