#!/bin/bash

PHYS_DIR=`pwd -P`
fulldataset=$PHYS_DIR/$1

dataset=$(basename "$fulldataset")
fulldatasetnofilename="${dataset%.*}"

train=$fulldatasetnofilename'_train.csv'
test=$fulldatasetnofilename'_test.csv'

cd 00-common

for i in `seq 1 1`;
do
    echo '== ITERATION: '$i ' =='
    echo '[INFO] dividing the data into train and test datasets'
    python split_data.py $fulldataset

    trainc=$train

    echo '[INFO] frequency model'
    python ../02-frequency-model/freq_recall.py $trainc $test
    echo '[INFO] genre baseline model'
    python ../03-genre-model/base_model_recall.py $trainc $test
    echo '[INFO] personalised genre model'
    python ../03-genre-model/cross_validate_recall.py $trainc $test
    echo '[INFO] lda model'
    python ../06-latent-dirichlet-allocation/lda_recall.py $trainc $test
    echo '[INFO] removing train and test datasets'
    rm $trainc
    rm $test
done
