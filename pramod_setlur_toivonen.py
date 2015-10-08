'''
Algorithm for Toivonen
______________________

'''

import sys
import itertools
import random

support = 0
bucket_size = 0

sample_percentage = 0.5
scaled_support = support * sample_percentage * 0.8


def update_scaled_support(support):
    scaled_support = support * sample_percentage * 0.8


def generate_random_sample(input_file, k):
    random_sample = []
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            intermediate_random_set = list_transaction
            if k <= len(list_transaction):
                intermediate_random_set = random.sample(list_transaction, k)
            random_sample.append(intermediate_random_set)
    return random_sample
    file.close()

def count_item_sets(random_sample_data, k):
    item_set_count = {}
    for each_random_item in random_sample_data:
        print tuple(each_random_item)
        item_set_count.setdefault(each_random_item, 0)
        count = item_set_count.get(each_random_item)
        count += 1
        item_set_count[each_random_item] = count

def generate_candidate_item_sets(random_sample_data, k):
    item_set_count = count_item_sets(random_sample_data, k)
    print item_set_count

def generate_frequent_item_set_apriori(random_sample_data, k):
    candidate_item_set = generate_candidate_item_sets(random_sample_data, k)


if __name__ == '__main__':
    if 3 != len(sys.argv):
        print "Usage: $ python pramod_setlur_toivonen.py [input.txt] [support]"
    else:
        input_file = sys.argv[1]
        support = int(sys.argv[2])

        update_scaled_support(support)

        k = 1
        random_sample_data = generate_random_sample(input_file, k)
        print random_sample_data
        frequent_item_list = generate_frequent_item_set_apriori(random_sample_data, k)