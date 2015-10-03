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

def generate_hash_value(each_subset):
    length = len(each_subset)
    total = 0
    for i in range(length):
        total += hash(each_subset[i])

    return total % bucket_size

def compute_hash(hash_bucket, input_file, k):
    bit_map = [0]
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            subsets_k = itertools.combinations(list_transaction,  k)
            subset_k_list = list(subsets_k)

            for each_subset in subset_k_list:
                bucket_number = generate_hash_value(each_subset)
                hash_bucket.setdefault(bucket_number, 1)
                count = hash_bucket[bucket_number]
                count = count + 1
                hash_bucket[bucket_number] = count

    for bucket_num, count in hash_bucket.iteritems():
        if count >= support:
            bit_map.insert(bucket_num, 1)
        else:
            bit_map.insert(bucket_num, 0)

    return (hash_bucket, bit_map)
    file.close()

def compute_candidate_item_sets(input_file, bit_map, k):
    candidate_item_set = []
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            subset_k = itertools.combinations(list_transaction, k)
            subset_k_list = list(subset_k)

            for each_subset in subset_k_list:
                subset_k_1_list = list(itertools.combinations(each_subset, k-1))
                flag = 1
                for item in subset_k_1_list:
                    #Check if the item is present in FIL (whose item sizes should also be k-1)
                    length = len(item)
                    for i in range(length):
                        if item[i] not in frequent_item_list:
                            flag = 0

                if flag == 1:
                    bucket_number = generate_hash_value(each_subset)
                    if(1 == bit_map[bucket_number]):
                        if each_subset not in candidate_item_set:
                            candidate_item_set.append(each_subset)

    file.close()
    return candidate_item_set

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

        k = 2

        #initializing the bucket
        hash_bucket = {}
        for i in range(bucket_size):
            hash_bucket[i] = 0

        hash_bucket, bit_map = compute_hash(hash_bucket, input_file, k)
        print hash_bucket
        candidate_item_set = compute_candidate_item_sets(input_file, bit_map, k)
        compute_frequent_item_sets(input_file, candidate_item_set)