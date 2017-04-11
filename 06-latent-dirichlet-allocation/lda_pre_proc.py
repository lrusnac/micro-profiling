import sys
import math

sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count

from lda import fit_and_get_lda
from lda import get_account_topic_matrix
from lda import get_topic_term_matrix
from lda import get_user_movie_matrix
from tqdm import tqdm
import numpy
import csv

t_topic_p = 0.1

lda_max_iter = 20
n_topics = 40

def preprocess_on_original(filepath):
    # matr.sum_duplicates()
    # matr.data = np.ones(len(matr.col))

    train_matr, accounts, movie_by_index = get_user_movie_matrix(filepath)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Remove duplicates
    train_matr.sum_duplicates()
    train_matr.data = numpy.ones(len(train_matr.col))

    # Fit LDA
    lda = fit_and_get_lda(train_matr, n_topics, lda_max_iter)
    # Transform account-cluster matrix accoring to fitted LDA
    train_transform = lda.transform(train_matr)
    # Get account-topic matrix from transformed matrix
    doc_topic_matr = get_account_topic_matrix(train_transform, acc_by_index)
    # Get topic-cluster matrix from LDA components
    top_term_matr = get_topic_term_matrix(lda.components_, movie_by_index)

    # Filter topic propabilities with low p
    multi_accounts = {}
    for account, topics in doc_topic_matr.iteritems():
        good_topics = dict((i, t) for i, t in enumerate(topics) if t > t_topic_p)
        multi_accounts[account] = good_topics
    
    # for acc, tops in multi_accounts.iteritems():
    #     print '{}: {}'.format(acc,
    #         ['{:>2d}: {:>5.3f}'.format(i, t) for i, t in tops.iteritems()])

    out_filepath = '.'.join(filepath.split('.')[:-1]) + '_w_topics.csv'
    csvfile = get_data_file_pointer(filepath)
    fields = csvfile.fieldnames
    
    with open(out_filepath, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(fields)

        for trans in tqdm(csvfile, total=get_line_count(filepath)):
            account = trans['hashed_ID']
            movie = trans['VM_TITLE']

            # Get topic giving max: acc_topic_p * topic_term_p
            max_t = -1
            max_p = -1
            for top_i in multi_accounts[account]:
                p = multi_accounts[account][top_i] * top_term_matr[top_i][movie]
                if p > max_p:
                    max_p = p
                    max_t = top_i
            
            trans['hashed_ID'] = account + '_' + str(max_t)
            writer.writerow(map(lambda field: trans[field], fields))


if __name__ == '__main__':
    preprocess_on_original(sys.argv[1])
    

