import sys
import math
sys.path.insert(0, '../00-common')

from common import get_data_file_pointer
from common import get_line_count

from lda import *

from tqdm import tqdm
import numpy

LDA_MAX_ITER = 20
N_TOPICS = 40

DOC_TOPIC_THRESH = 0.1
TOPIC_TERM_THRESH = 0.001
c = 6

lda = None
doc_topic_matr = None
top_term_matr = None
train_matr = None
train_transform = None
accounts = None
movie_by_index = None


def build_lda_model(train_file):
    global accounts
    global train_matr
    global movie_by_index
    global lda
    train_matr, accounts, movie_by_index = get_user_movie_matrix(train_file)

    # remove duplicates
    train_matr.sum_duplicates()
    train_matr.data = numpy.ones(len(train_matr.col))

    lda = fit_and_get_lda(train_matr, N_TOPICS, LDA_MAX_ITER)

if __name__ == '__main__':
    data_file = sys.argv[1]
    # if len(sys.argv) == 4:
    #     DOC_TOPIC_THRESH = float(sys.argv[2])
    #     TOPIC_TERM_THRESH = float(sys.argv[3])

    build_lda_model(data_file)

    # Transform account-cluster matrix according to fitted LDA
    train_transform = lda.transform(train_matr)

    acc_by_index = [''] * len(accounts)
    for u_hash, i in accounts.iteritems():
        acc_by_index[i] = u_hash

    # Get account-topic matrix from transformed matrix
    doc_topic_matr = get_account_topic_matrix(train_transform, acc_by_index)

    doc_top2 = {}
    for acc, topics in doc_topic_matr.iteritems():
        doc_top2[acc] = []
        for i, t_p in enumerate(topics):
            t_p = round(c * math.log(1/t_p, 2), 0)
            t_p = math.pow(math.pow(2, t_p/c), -1)
            doc_top2[acc].append(t_p)
        
        # Ensure sum=1
        dc_sum = sum(doc_top2[acc])
        for i in xrange(0, len(doc_top2[acc])):
            p = doc_top2[acc][i]
            doc_top2[acc][i] = p + (1-dc_sum) * (p / float(dc_sum))
            
    doc_topic_matr = doc_top2
    
    # for account, topics in doc_topic_matr.iteritems():
    #     print '{};{}'.format(account, ';'.join(str(t) for t in topics))
    # print

    # Get topic-cluster matrix from LDA components
    top_term_matr = get_topic_term_matrix(lda.components_, movie_by_index)
    
    top_term2 = {}
    for top, movies_dict in top_term_matr.iteritems():
        top_term2[top] = {}
        for movie, m_p in movies_dict.iteritems():
            m_p = round(c * math.log(1/m_p, 2), 0)
            m_p = math.pow(math.pow(2, m_p/c), -1)
            top_term2[top][movie] = m_p
        
        # Ensure sum=1
        tt_sum = sum(top_term2[top].values())
        for movie in top_term2[top].keys():
            p = top_term2[top][movie]
            top_term2[top][movie] = p + (1-tt_sum) * (p / float(tt_sum))
            
    top_term_matr = top_term2
    
    # print 'TOPIC;{}'.format(';'.join(top_term_matr[0].iterkeys()))
    # for topic, movie_dict in top_term_matr.iteritems():
    #     p_vals = [str(p) for p in movie_dict.itervalues()]
    #     print '{};{}'.format(topic, ';'.join(p_vals))

    for i in xrange(11, 31):
        DOC_TOPIC_THRESH = 0.01 * i # 1% - 20%
        for j in xrange(1, 7):
            TOPIC_TERM_THRESH = 0.0005 * j # 0.05% - 1%

            sys.stdout.write(
                '[INFO] doc_top_t={}   top_term_t={}\n'.format(
                DOC_TOPIC_THRESH, TOPIC_TERM_THRESH))
            sys.stdout.flush()

            # Filter small values
            def_doc_top_vals = {} # Default p-vals per account for filtered values
            c_unf_doc_top = 0
            c_unf_top_term = 0
            for account, topics in doc_topic_matr.iteritems():
                unfiltered = unfiltered_sum = 0
                for i, p in enumerate(topics):
                    if p == 0:
                        print "{}: {}".format(account, ";".join(str(t) for t in topics))
                    if p >= DOC_TOPIC_THRESH:
                        unfiltered_sum += p
                        unfiltered += 1
                c_unf_doc_top += unfiltered
                def_doc_top_vals[account] =\
                    (1.0 - unfiltered_sum) / (N_TOPICS - unfiltered)
                
            def_top_term_vals = {}
            c_movies = len(top_term_matr.itervalues().next())
            for topic, movie_dict in top_term_matr.iteritems():
                unfiltered = unfiltered_sum = 0
                for movie in movie_dict:
                    if p == 0:
                        print "{}: {}".format(topic, ";".join(str(p) for p in movie_dict.itervalues()))
                    if movie_dict[movie] >= TOPIC_TERM_THRESH:
                        unfiltered_sum += movie_dict[movie]
                        unfiltered += 1
                c_unf_top_term += unfiltered
                def_top_term_vals[topic] =\
                    (1.0 - unfiltered_sum) / (c_movies - unfiltered)


            # calculate entropy
            dataset = get_data_file_pointer(data_file)
            guess_accuracy_sum = 0
            entries = 0
            for entry in tqdm(dataset, total=get_line_count(data_file)):
                user = entry['hashed_ID']
                movie = entry['VM_TITLE']
                entries += 1

                p = 0
                for topic, t_p in enumerate(doc_topic_matr[user]):
                    t_p = t_p if t_p >= DOC_TOPIC_THRESH else def_doc_top_vals[user]
                    m_p = top_term_matr[topic][movie]
                    m_p = m_p if m_p >= TOPIC_TERM_THRESH else def_top_term_vals[topic]
                    p += t_p * m_p

                try:
                    guess_accuracy_sum -= math.log(p, 2)
                except ValueError:
                    print p
                    print user
                    print movie
                    print "Doc-Topic:"
                    print " ; ".join(str(t_p) for t_p in doc_topic_matr[user])
                    print "Topic-Term:"
                    print " ; ".join(str(top_term_matr[topic][movie]) for topic, p in enumerate(doc_topic_matr[user]))
                    raise

            sys.stdout.write('{};{};{}\n'.format(
                guess_accuracy_sum / entries,
                c_unf_doc_top,
                c_unf_top_term))
            sys.stdout.flush()
    # print 'Entropy: {}'.format(guess_accuracy_sum / entries)
    # print 'Unfiltered in doc-topic: {}'.format(c_unf_doc_top)
    # print 'Unfiltered in topic-term: {}'.format(c_unf_top_term)
