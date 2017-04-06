import sys
import math
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
from lda import get_cluster_matrix
from lda import get_genre_matrix
from lda import get_term_movie_matrix
from lda import fit_and_get_lda
from lda import get_account_topic_matrix
from lda import get_topic_term_matrix
from lda import get_user_movie_matrix
from tqdm import tqdm
import numpy
import argparse

guess_movies = False
use_genre = True

lda_max_iter = 20
n_topics = 40

def test_lda_on_clusters(train_file, test_file, guess_movie=False):
    train_matr, accounts, clus_by_index = get_cluster_matrix(train_file)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    run_cross(
        train_matr,
        acc_by_index,
        clus_by_index,
        test_file,
        'KMeans',
        guess_movie=guess_movies)

def test_lda_on_genres(train_file, test_file, guess_movie=False):
    train_matr, accounts, genre_by_index = get_genre_matrix(train_file)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    run_cross(
        train_matr,
        acc_by_index,
        genre_by_index,
        test_file,
        'VM_GENRE',
        guess_movie=guess_movies)

def test_lda_on_original(train_file, test_file):
    # matr.sum_duplicates()
    # matr.data = np.ones(len(matr.col))

    train_matr, accounts, movie_by_index = get_user_movie_matrix(train_file)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Remove duplicates
    train_matr.sum_duplicates()
    train_matr.data = numpy.ones(len(train_matr.col))

    run_cross(
        train_matr,
        acc_by_index,
        movie_by_index,
        test_file,
        'VM_TITLE')


def run_cross(train_matr, acc_by_index, term_by_index,
                test_file_path, term_key, guess_movie=False):
    # Fit LDA
    lda = fit_and_get_lda(train_matr, n_topics, lda_max_iter)
    # Transform account-cluster matrix accoring to fitted LDA
    train_transform = lda.transform(train_matr)
    # Get account-topic matrix from transformed matrix
    doc_topic_matr = get_account_topic_matrix(train_transform, acc_by_index)
    # Get topic-cluster matrix from LDA components
    top_term_matr = get_topic_term_matrix(lda.components_, term_by_index)

    term_movie_matr = get_term_movie_matrix(train_file, term_key) if guess_movie else None
    
    n_transactions = get_line_count(test_file_path)
    testset = get_data_file_pointer(test_file_path)
    guess_accuracy_sum = 0
    entries = 0
    zero_p_count = 0

    for trans in tqdm(testset, total=n_transactions):
        doc = trans['hashed_ID']
        term = trans[term_key]
        p = 0

        ## Guess cluster
        if doc in doc_topic_matr and\
            term in top_term_matr[0]:
            p = sum(t_p * top_term_matr[i][term]
                for i, t_p in enumerate(doc_topic_matr[doc]))
            
            # Additionally guess movie
            if term_movie_matr is not None:
                movie = trans['VM_TITLE']
                if movie in term_movie_matr[term]:
                    p *= term_movie_matr[term][movie]
                else:
                    p = 0

        if p == 0:
            zero_p_count += 1
        else:
            guess_accuracy_sum -= math.log(p, 2)
        entries += 1


    print 'Entropy: {}'.format(guess_accuracy_sum / entries)
    print 'Loss: {}'.format(zero_p_count / n_transactions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train')
    parser.add_argument('test')
    parser.add_argument('-n', '--topics', type=int, default=10, help='number of topics for lda')
    parser.add_argument('-i', '--maxiter', type=int, default=10, help='max iterations for lda')
    parser.add_argument('-t', '--term', choices=['genre', 'cluster', 'original'], default='original')
    parser.add_argument('-p', '--predict', choices=['group', 'movie'], default='movie')

    args = parser.parse_args()

    movie = args.predict == 'movie'

    if args.term == 'original':
        test_lda_on_original(args.train, args.test)
    elif args.term == 'genre':
        test_lda_on_genres(args.train, args.test, movie)
    else:
        test_lda_on_clusters(args.train, args.test, movie)

    
    lda_max_iter = args.maxiter
    n_topics = args.topics
