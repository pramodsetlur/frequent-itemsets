import sys
import itertools

singleton_sets = {}
pairs_sets = {}

def compute_singleton_set(list_transaction):
    transaction_items = list_transaction.split(',')

    for transaction in transaction_items:
        singleton_sets.setdefault(transaction, 1)
        count = singleton_sets.get(transaction)
        count = count + 1
        singleton_sets[transaction] = count

def compute_pairs_sets(transaction):
    transaction_items = transaction.rstrip('\n')
    transaction_items = transaction.strip(',')

    transaction_combination_two = itertools.combinations(transaction_items, 2)
    transaction_pairs = list(transaction_combination_two)

    #print transaction_pairs


def compute_frequent_sets_pcy(input_file, support, bucket_size):
    for transaction in open(input_file):
        transaction.rstrip('\n')
        list_transaction = list(transaction)
        compute_singleton_set(list_transaction)
        compute_pairs_sets(transaction)
    print singleton_sets

if __name__ == '__main__':
    if (4 != len(sys.argv)):
        print "Usage: python pramod_setlur_pcy.py [input.txt] [support] [hash_bucket_size]"
    else:
        input_file = sys.argv[1]
        support = sys.argv[2]
        bucket_size = sys.argv[3]

        compute_frequent_sets_pcy(input_file, support, bucket_size)
