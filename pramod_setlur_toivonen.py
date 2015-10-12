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
            list_transaction = sorted(transaction.strip().split(','))
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

def generate_k_combinations(data, k):
    combination_list = []
    for each_transaction in data:
        each_transaction_combinations = list(itertools.combinations(each_transaction, k))
        if 1 == k:
            for each_combination in each_transaction_combinations:
                for element in each_combination:
                    if element not in combination_list:
                        combination_list.append(element)
        else:
            for each_combination in each_transaction_combinations:
                combination_list.append(each_combination)

    combination_list.sort()
    return combination_list


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
        ck_2 = list(itertools.combinations(lk_1_list, 2))
        combinations_random_list = generate_k_combinations(random_sample_data, k)
        for each_transaction in combinations_random_list:
            if each_transaction in ck_2:
                ck_dictionary.setdefault(each_transaction, 0)
                count = ck_dictionary.get(each_transaction)
                count += 1
                ck_dictionary[each_transaction] = count

    if k >= 3:
        combinations_random_list = generate_k_combinations(random_sample_data, k)
        for each_combination in combinations_random_list:
            subset_k_1 = list(itertools.combinations(each_combination, k-1))
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

def generate_frequent_list(ck_dictionary, support):
    lk_list = []
    for item, count in ck_dictionary.iteritems():
        if count >= support:
            if item not in lk_list:
                lk_list.append(item)
    lk_list.sort()
    return lk_list


def generate_nbl_list(ck_list, lk_list, lk_list_1, k):
    nbl_temp_list = []
    nbl_list = []
    for each_item in ck_list:
        if each_item not in lk_list:
            nbl_temp_list.append(each_item)
    if 1 == k:
        nbl_list = nbl_temp_list
    else:
        for each_item in nbl_temp_list:
            subset_nbl_list = list(itertools.combinations(each_item, k-1))
            flag = 1
            for each_subset in subset_nbl_list:
                if 1 == len(each_subset):
                    if each_subset[0] not in lk_list_1:
                        flag = 0
                else:
                    if each_subset not in lk_list_1:
                        flag = 0
            if 1 == flag:
                nbl_list.append(each_item)
    return nbl_list

def generate_ck_list_from_dictionary(ck_dictionary):
    ck_list = []
    for key, value in ck_dictionary.iteritems():
        ck_list.append(key)
    ck_list.sort()
    return ck_list


def convert_file_to_list(input_file):
    full_file_list = []
    with open(input_file) as file:
        for each_line in file:
            list_line = each_line.strip().split(',')
            full_file_list.append(list(list_line))
    file.close()
    return full_file_list

def generate_candidate_dictionary_full_file(input_file, nbl_list, lk_list, k):
    candidate_dictionary = {}
    with open(input_file) as file:
        for each_transaction in file:
            list_each_transaction = sorted(each_transaction.strip().split(','))
            each_transaction_combinations = list(itertools.combinations(list_each_transaction, k))
            if 1 == k:
                temp_each_transaction_combination = []
                for element in each_transaction_combinations:
                    temp_each_transaction_combination.append(element[0])
                each_transaction_combinations = temp_each_transaction_combination

            for each_combination in each_transaction_combinations:
                if each_combination in nbl_list or each_combination in lk_list:
                    candidate_dictionary.setdefault(each_combination, 0)
                    count = candidate_dictionary.get(each_combination)
                    count += 1
                    candidate_dictionary[each_combination] = count
    return candidate_dictionary
    file.close()

def check_frequent_list_nbl(frequent_list_full_file, nbl_list):
    for each_frequent_item_set in frequent_list_full_file:
        if each_frequent_item_set in nbl_list:
            return False
    return True


def generate_toivonen(input_file):
    ultimate_frequent_list = []
    lk_1_list = []
    resample = True
    k = 1
    while 0 != len(lk_1_list) or 1 == k:
        if resample:
            k = 1
            random_sample_data = generate_random_sample(input_file)
            print "Random Sample Data: ", random_sample_data, "\n"
        if 1 == k:
            lk_1_list = random_sample_data

        #Pass 1: with Random Sampled data

        ck_dictionary = generate_ck_dictionary(random_sample_data, lk_1_list, k)
        print "ck-dictionary: ", ck_dictionary, "\n"

        ck_list = generate_ck_list_from_dictionary(ck_dictionary)
        print "ck_list: ", ck_list, "\n"

        lk_list = generate_frequent_list(ck_dictionary, scaled_support)
        print "lk_list: ", lk_list, "\n"

        nbl_list = generate_nbl_list(ck_list, lk_list, lk_1_list, k)
        print "nbl_list:", nbl_list, "\n"

        #Pass 2: Checking with the actual file


        full_file_list = convert_file_to_list(input_file)
        print "File as a list: ", full_file_list, "\n"

        candidate_dictionary_item_sets_full_file = generate_candidate_dictionary_full_file(input_file, nbl_list, lk_list, k)
        print "Candidate Dictionary Full File: ", candidate_dictionary_item_sets_full_file, "\n"

        frequent_list_full_file = generate_frequent_list(candidate_dictionary_item_sets_full_file, support)
        print "Frequent item set full file: ", frequent_list_full_file, "\n"

        result = check_frequent_list_nbl(frequent_list_full_file, nbl_list)
        print "Result: ", result
        resample = not result

        ultimate_frequent_list.append(frequent_list_full_file)
        lk_1_list = frequent_list_full_file
        k += 1

        if resample:
            lk_1_list = []
            ultimate_frequent_list = []

    return ultimate_frequent_list


if __name__ == '__main__':
    if 3 != len(sys.argv):
        print "Usage: $ python pramod_setlur_toivonen.py [input.txt] [support]"
    else:
        input_file = sys.argv[1]
        support = int(sys.argv[2])

        update_scaled_support(support)

        print "support: ", support, "\n"
        print "scaled support", scaled_support, "\n"

        ultimate_frequent_list  = generate_toivonen(input_file)
        print "Ultimate Frequent List: \n", ultimate_frequent_list

