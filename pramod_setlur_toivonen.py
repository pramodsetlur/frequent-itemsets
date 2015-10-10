'''
Algorithm for Toivonen
______________________
Pass1
1. Generate Random Sample data
2. Generate Candidate Frequent Itemsets, Ck
3. Generate Frequent Itemsets, Lk (using scaled support)
4. Generate N.B.L

Pass2:
1. Generate count for whole file for the ones present in Lk and NBL
2. Generate frequent itemsets (using actual support)
2. If any NBL is present in the above list, resample and start algorithm again wth k = 1
    else increment k
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
    global scaled_support
    scaled_support = support * sample_percentage * 0.8


def get_total_number_of_lines(input_file):
    with open(input_file) as file:
        number_of_lines = sum(1 for line in file)
    file.close()
    return number_of_lines


def get_random_line_numbers(number_of_lines):
    sample_lines_required = number_of_lines * sample_percentage
    sample_lines_required = int(math.floor(sample_lines_required))
    random_line_numbers = random.sample(range(1, number_of_lines), sample_lines_required)
    return random_line_numbers

def generate_random_sample(input_file):
    random_sample = []
    number_of_lines = get_total_number_of_lines(input_file)
    random_line_numbers = get_random_line_numbers(number_of_lines)

    line_number = 1
    with open(input_file) as file:
        for transaction in file:
            list_transaction = transaction.strip().split(',')
            if line_number in random_line_numbers:
                random_sample.append(list_transaction)
            line_number += 1
    file.close()
    return random_sample

def generate_singleton(list):
    singleton = []
    for each_transaction in list:
        for each_item in each_transaction:
            if each_item not in singleton:
                singleton.append(each_item)
    singleton.sort()
    return singleton

def generate_combinations_k_random_data(random_sample_data, k):
    combination_random_list = []
    for each_transaction in random_sample_data:
        each_transaction_combinations = itertools.combinations(each_transaction, k)
        for each_combination in each_transaction_combinations:
            if each_combination not in combination_random_list:
                combination_random_list.append(each_combination)

    combination_random_list.sort()
    return combination_random_list


def generate_ck_dictionary(random_sample_data, lk_1_list, k):
    ck_dictionary = {}
    if 1 == k:
        for each_transaction in random_sample_data:
            for each_item in each_transaction:
                ck_dictionary.setdefault(each_item, 0)
                count = ck_dictionary.get(each_item)
                count += 1
                ck_dictionary[each_item] = count

    if 2 == k:
        combinations_random_list = generate_combinations_k_random_data(random_sample_data, k)
        for each_transaction in combinations_random_list:
            ck_dictionary.setdefault(each_transaction, 0)
            count = ck_dictionary.get(each_transaction)
            count += 1
            ck_dictionary[each_transaction] = count

    if k >= 3:
        combinations_random_list = generate_ck_dictionary(random_sample_data, k)
        for each_combination in combinations_random_list:
            subset_k_1 = itertools.combinations(each_combination, k-1)
            flag = 1
            for each_subset in subset_k_1:
                if each_subset not in lk_1_list:
                    flag = 0
            if 1 == flag:
                ck_dictionary.setdefault(each_combination, 0)
                count = ck_dictionary.get(each_combination)
                count += 1
                ck_dictionary[each_combination] = count

    return ck_dictionary

def generate_lk_list(ck_dictionary):
    lk_list = []
    for item, count in ck_dictionary.iteritems():
        if count > scaled_support:
            if item not in lk_list:
                lk_list.append(item)
    lk_list.sort()
    return lk_list


def generate_nbl_list(ck_dictionary, lk_list, k):
    if 1 == k:


    for each_item in lk_list:


def generate_ck_list_from_dictionary(ck_dictionary):


if __name__ == '__main__':
    if 3 != len(sys.argv):
        print "Usage: $ python pramod_setlur_toivonen.py [input.txt] [support]"
    else:
        input_file = sys.argv[1]
        support = int(sys.argv[2])

        update_scaled_support(support)

        k = 1
        random_sample_data = generate_random_sample(input_file)
        if 1 == k:
            lk_1_list = random_sample_data
        ck_dictionary = generate_ck_dictionary(random_sample_data, lk_1_list, k)
        lk_list = generate_lk_list(ck_dictionary)
        ck_list = generate_ck_list_from_dictionary(ck_dictionary)
        #print lk_list
        nbl_list = generate_nbl_list(ck_dictionary, lk_list, k)
