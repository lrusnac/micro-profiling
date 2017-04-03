import sys
import math
sys.path.insert(0, '../00-common')
from common import get_data_file_pointer
from common import get_line_count
from lda import get_cluster_matrix
from lda import get_genre_matrix
from lda import get_cluster_movies_map
from lda import fit_and_get_lda
from lda import get_account_topic_matrix
from lda import get_topic_cluster_matrix
from tqdm import tqdm

guess_movies = False
use_genre = False

def test_lda_on_clusters(train_file, test_file):
    train_matr, accounts = get_cluster_matrix(train_file)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Fit LDA
    lda = fit_and_get_lda(train_matr)
    # Transform account-cluster matrix according to fitted LDA
    train_transform = lda.transform(train_matr)
    # Get account-topic matrix from transformed matrix
    acc_top_matrix = get_account_topic_matrix(train_transform, acc_by_index)
    # Get topic-cluster matrix from LDA components
    top_clus_matrix = get_topic_cluster_matrix(lda.components_)
    # Get map of movie probabilities with clusters
    clus_mov_map = get_cluster_movies_map(train_file)

    n_transactions = get_line_count(test_file) - 1
    testset = get_data_file_pointer(test_file)
    guess_accuracy_sum = 0
    entries = 0
    zero_p_count = 0
    for trans in tqdm(testset, total=n_transactions):
        u_hash = trans['hashed_ID']
        cluster = trans['KMeans']
        p = 0

        ## Guess cluster
        if u_hash in acc_top_matrix:
            p = sum(t_p * top_clus_matrix[i][int(cluster)]
                for i, t_p in enumerate(acc_top_matrix[u_hash]))

            # Additionally guess movie
            if guess_movies:
                movie = trans['VM_TITLE']
                if movie in clus_mov_map[cluster]:
                    p *= clus_mov_map[cluster][movie]
                else:
                    p = 0

        if p == 0:
            zero_p_count += 1
        else:
            guess_accuracy_sum -= math.log(p, 2)
        entries += 1
            
    
    print 'Entropy: {}'.format(guess_accuracy_sum / entries)
    print 'Loss: {}'.format(zero_p_count / n_transactions)

def test_lda_on_genres(train_file, test_file):
    train_matr, accounts, genre_indices = get_genre_matrix(train_file)

    ##### Populate acc_by_index
    acc_by_index = [""] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Fit LDA
    lda = fit_and_get_lda(train_matr)
    # Transform account-cluster matrix accoring to fitted LDA
    train_transform = lda.transform(train_matr)
    # Get account-topic matrix from transformed matrix
    acc_top_matrix = get_account_topic_matrix(train_transform, acc_by_index)
    # Get topic-cluster matrix from LDA components
    top_clus_matrix = get_topic_cluster_matrix(lda.components_)
    # Get map of movie probabilities with clusters
    clus_mov_map = get_cluster_movies_map(train_file, use_genre=True)

    n_transactions = get_line_count(test_file)
    testset = get_data_file_pointer(test_file)
    guess_accuracy_sum = 0
    entries = 0
    zero_p_count = 0
    for trans in tqdm(testset, total=n_transactions):
        u_hash = trans['hashed_ID']
        genre = trans['VM_GENRE']
        p = 0

        ## Guess cluster
        if u_hash in acc_top_matrix:
            p = sum(t_p * top_clus_matrix[i][genre_indices[genre]]
                for i, t_p in enumerate(acc_top_matrix[u_hash]))
            
            # Additionally guess movie
            if guess_movies:
                movie = trans['VM_TITLE']
                if movie in clus_mov_map[genre]:
                    p *= clus_mov_map[genre][movie]
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
    if use_genre:
        test_lda_on_genres(sys.argv[1], sys.argv[2])
    else:
        test_lda_on_clusters(sys.argv[1], sys.argv[2])
    

