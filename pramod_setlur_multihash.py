'''
Algorithm for Multihash
_______________________

1. Create a frequent item set of size 1
2. While there are more items in frequent itemsets
    #Generating hash
    Compute hash_bucket1 and hash_bucket2
    Compute bit_map1 and bit_map2

    #Generating candidate item sets
    If each subset maps to a bitmap with 1 in both bitmaps 1 and 2
        consider it as a candidate itemset

    Generate Frequent itemsets using the above candidate itemsets

'''
import sys
import itertools

frequent_item_list = []
support = 0
bucket_size = 0



#Function to generate singleton (all) item set
def compute_singleton_set(singleton_dict, transaction):

    transaction_items = transaction.strip().split(',')

    for transaction in transaction_items:
        singleton_dict.setdefault(transaction, 0)
        count = singleton_dict.get(transaction)
        count = count + 1
        singleton_dict[transaction] = count
    return singleton_dict

def compute_frequent_singleton_item_set(input_file):
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

def generate_hash_value1(each_subset):
    length = len(each_subset)
    total = 0
    for i in range(length):
        total += hash(each_subset[i])

    return total % bucket_size

def generate_hash_value2(each_subset):
    length = len(each_subset)
    total = 0
    for i in range(length):
        total += ord(each_subset[i])

    return total % bucket_size

def compute_hash(hash_bucket1, bit_map1, hash_bucket2, bit_map2, input_file, k):
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            list_transaction.sort()

            #print "line being processed: ", list_transaction
            subsets_k = itertools.combinations(list_transaction,  k)
            subset_k_list = list(subsets_k)

            #print "subset_k_list: ", subset_k_list

            for each_subset in subset_k_list:
                bucket_number1 = generate_hash_value1(each_subset)
                #print each_subset, "is hashing to bucket number ", bucket_number1
                hash_bucket1.setdefault(bucket_number1, 0)
                count = hash_bucket1[bucket_number1]
                count = count + 1
                hash_bucket1[bucket_number1] = count

                bucket_number2 = generate_hash_value2(each_subset)
                #print each_subset, "is hashing to bucket number2 ", bucket_number2
                hash_bucket2.setdefault(bucket_number2, 0)
                count = hash_bucket2[bucket_number2]
                count = count + 1
                hash_bucket2[bucket_number2] = count



    #print "Final Hash Bucket: ", hash_bucket
    #create the bit map
    for bucket_num, count in hash_bucket1.iteritems():
        if count >= support:
            bit_map1.insert(bucket_num, 1)
        else:
            bit_map1.insert(bucket_num, 0)

    for bucket_num, count in hash_bucket2.iteritems():
        if count >= support:
            bit_map2.insert(bucket_num, 1)
        else:
            bit_map2.insert(bucket_num, 0)

    file.close()

    #print "Final Bit map: ", bit_map
    return (hash_bucket1, bit_map1, hash_bucket2, bit_map2)


def compute_candidate_item_sets(input_file, bit_map1, bit_map2, k):
    #print "\n****Candidate pairs****\n"
    candidate_item_set = []
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            list_transaction.sort()

            #print "line being processed: ", list_transaction
            subset_k = itertools.combinations(list_transaction, k)
            subset_k_list = list(subset_k)

            for each_subset in subset_k_list:
                #print "subset being processed: ", each_subset
                bucket_number1 = generate_hash_value1(each_subset)
                if 1 == bit_map1[bucket_number1]:
                    bucket_number2 = generate_hash_value2(each_subset)
                    if 1 == bit_map2[bucket_number2]:
                        if each_subset not in candidate_item_set:
                            candidate_item_set.append(each_subset)

    file.close()
    #print "Final Candidate pairs: ", candidate_item_set
    return candidate_item_set

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
                if each_subset in candidate_item_sets:
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


if __name__ == '__main__':
    if 4 != len(sys.argv):
        print "Usage: $ python pramod_setlur_multihash.py [input.txt] [support] [hash_bucket_size]"
    else:
        input_file = sys.argv[1]
        support = sys.argv[2]
        bucket_size = sys.argv[3]

        support = int(support)
        bucket_size = int(bucket_size)

        compute_frequent_singleton_item_set(input_file)

        k = 1

        while 0 != len(frequent_item_list):
            hash_bucket1 = {}
            bit_map1 = [0]
            for i in range(bucket_size):
                hash_bucket1[i] = 0

            hash_bucket2 = {}
            bit_map2 = [0]
            for i in range(bucket_size):
                hash_bucket2[i] = 0


            k += 1

            #print "Hash bucket after initializing to 0: ", hash_bucket

            hash_bucket1, bit_map1, hash_bucket2, bit_map2 = compute_hash(hash_bucket1, bit_map1, hash_bucket2, bit_map2, input_file, k)
            candidate_item_set = compute_candidate_item_sets(input_file, bit_map1, bit_map2, k)
            frequent_item_list = compute_frequent_item_sets(input_file, candidate_item_set, k)


            if 0 != len(frequent_item_list):
                print "\n", hash_bucket1
                print hash_bucket2
                print frequent_item_list