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
        singleton_dict.setdefault(transaction, 0)
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

def compute_hash(hash_bucket, bit_map, input_file, k):
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            list_transaction.sort()

            #print "line being processed: ", list_transaction
            subsets_k = itertools.combinations(list_transaction,  k)
            subset_k_list = list(subsets_k)

            #print "subset_k_list: ", subset_k_list

            for each_subset in subset_k_list:
                bucket_number = generate_hash_value(each_subset)
                #print each_subset, "is hashing to bucket number ", bucket_number
                hash_bucket.setdefault(bucket_number, 0)
                count = hash_bucket[bucket_number]
                count = count + 1
                hash_bucket[bucket_number] = count

    #print "Final Hash Bucket: ", hash_bucket
    #create the bit map
    for bucket_num, count in hash_bucket.iteritems():
        if count >= support:
            bit_map.insert(bucket_num, 1)
        else:
            bit_map.insert(bucket_num, 0)

    #print "Final Bit map: ", bit_map
    return (hash_bucket, bit_map)
    file.close()

def compute_frequent_item_sets(input_file, candidate_item_sets, k):
    #print "\n****Frequent item sets calculation***\n"
    candidate_dictionary = {}
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            list_transaction.sort()
            #print "line being processed: ",

            subset_k = itertools.combinations(list_transaction, k)
            subset_k_list = list(subset_k)
            #print "all subsets of the above line: ", subset_k_list

            for each_subset in subset_k_list:
                if each_subset in candidate_item_set:
                    candidate_dictionary.setdefault(each_subset, 0)
                    count = candidate_dictionary.get(each_subset)
                    count += 1
                    #print each_subset, " is now appearing for the ", count, " time"
                    candidate_dictionary[each_subset] = count

        frequent_item_list = []

        for candidate_set, count in candidate_dictionary.iteritems():
            if count >= support:
                if candidate_item_set not in frequent_item_list:
                    frequent_item_list.append(list(candidate_set))

    file.close()
    #print "Frequent item list: ", frequent_item_list
    frequent_item_list.sort()
    return frequent_item_list



def compute_candidate_item_sets(input_file, bit_map, k):
    #print "\n****Candidate pairs****\n"
    candidate_item_set = []
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            list_transaction.sort()

            #print "line being processed: ", list_transaction
            subset_k = itertools.combinations(list_transaction, k)
            subset_k_list = list(subset_k)

            #print "subsets of the above line: ", subset_k_list

            for each_subset in subset_k_list:
                subset_k_1_list = list(itertools.combinations(each_subset, k-1))
                #print "subsets of k-1 length: ", subset_k_1_list
                flag = 1
                for item in subset_k_1_list:
                    #Check if the item is present in FIL (whose item sizes should also be k-1)
                    length = len(item)
                    for i in range(length):
                        #print "single items in the above subset of k-1: ", item[i]
                        if item[i] not in frequent_item_list:
                            #print item[i], " is not in the frequent item set"
                            flag = 0

                if flag == 1:
                    #print "all of the elements in ", each_subset, " is in the frequent list"
                    bucket_number = generate_hash_value(each_subset)
                    #print each_subset, "hashes to bucker number: ", bucket_number
                    if(1 == bit_map[bucket_number]):
                        if each_subset not in candidate_item_set:
                            candidate_item_set.append(each_subset)

    file.close()
    #print "Final Candidate pairs: ", candidate_item_set
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

        #initial setup
        compute_frequent_singleton_set(input_file)

        k = 2

        #initializing the bucket
        hash_bucket = {}
        bit_map = [0]
        for i in range(bucket_size):
            hash_bucket[i] = 0

        #print "Hash bucket after initializing to 0: ", hash_bucket

        hash_bucket, bit_map = compute_hash(hash_bucket, bit_map, input_file, k)

        print "\n"
        print hash_bucket

        candidate_item_set = compute_candidate_item_sets(input_file, bit_map, k)
        frequent_item_list = compute_frequent_item_sets(input_file, candidate_item_set, k)
        print frequent_item_list