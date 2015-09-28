import sys

singleton_sets = {}


def compute_singleton_set(transaction):
    transaction_items = transaction.rstrip('\n')
    transaction_items = transaction_items.split(',')

    for transaction in transaction_items:
        singleton_sets.setdefault(transaction, 1)
        count = singleton_sets.get(transaction)
        count = count + 1
        singleton_sets[transaction] = count

def compute_frequent_sets_pcy(input_file, support, bucket_size):
    for transaction in open(input_file):
        compute_singleton_set(transaction)
    print singleton_sets

if __name__ == '__main__':
    if (4 != len(sys.argv)):
        print "Usage: python pramod_setlur_pcy.py [input.txt] [support] [hash_bucket_size]"
    else:
        input_file = sys.argv[1]
        support = sys.argv[2]
        bucket_size = sys.argv[3]

        compute_frequent_sets_pcy(input_file, support, bucket_size)
