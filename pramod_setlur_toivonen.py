'''
Algorithm for Toivonen
______________________

'''

import sys
import itertools
import random
import math

support = 0
bucket_size = 0

sample_percentage = 0.5
scaled_support = support * sample_percentage * 0.8


def update_scaled_support(support):
    scaled_support = support * sample_percentage * 0.8


def generate_random_sample(input_file, sample_percentage):
    random_sample = []
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')

            k = len(list_transaction) * sample_percentage
            k = int(math.floor(k))

            intermediate_random_set = random.sample(list_transaction, k)
            random_sample.append(intermediate_random_set)

    file.close()
    return random_sample


def count_item_sets(random_sample_data, k):
    item_set_count = {}
    for each_random_transaction in random_sample_data:
        subset_k_list = list(itertools.combinations(each_random_transaction, k))
        for each_transaction in subset_k_list:
            if 1 == len(each_transaction):
                each_transaction = each_transaction[0]

            item_set_count.setdefault(each_transaction, 0)
            count = item_set_count.get(each_transaction)
            count += 1
            item_set_count[each_transaction] = count
    return item_set_count


def generate_candidate_item_sets(random_sample_data, k):
    item_set_count = count_item_sets(random_sample_data, k)
    candidate_item_set = []
    for each_item, count in item_set_count.iteritems():
        if count >= scaled_support:
            if each_item not in candidate_item_set:
                candidate_item_set.append(each_item)

    return  candidate_item_set

def generate_frequent_item_set_apriori(random_sample_data, k):
    candidate_item_set = generate_candidate_item_sets(random_sample_data, k)
    print candidate_item_set

if __name__ == '__main__':
    if 3 != len(sys.argv):
        print "Usage: $ python pramod_setlur_toivonen.py [input.txt] [support]"
    else:
        input_file = sys.argv[1]
        support = int(sys.argv[2])

        update_scaled_support(support)

        k = 1
        random_sample_data = generate_random_sample(input_file, sample_percentage)
        frequent_item_list = generate_frequent_item_set_apriori(random_sample_data, k)