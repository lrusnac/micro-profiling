#!/bin/bash

PHYS_DIR=`pwd -P`
fulldataset=$PHYS_DIR/$1

dataset=$(basename "$fulldataset")
fulldatasetnofilename="${dataset%.*}"

splitedbytime=$fulldatasetnofilename'_divided_by_time.csv'
cd 00-common

python split_customer.py $dataset -n3 -s5
out_file="to_be_defined.csv"

head -n1 $splitedbytime > $out_file
tail -n+2 $splitedbytime | sort -t';' -k2 >> $out_file

rm $splitedbytime
python split_data.py $out_file

train="to_be_defined_train.csv"
test="to_be_defined_test.csv"

echo '[INFO] frequency model'
python ../02-frequency-model/freq_recall.py $train $test
echo '[INFO] genre baseline model'
python ../03-genre-model/base_model_recall.py $train $test
echo '[INFO] personalised genre model'
python ../03-genre-model/cross_validate_recall.py $train $test
echo '[INFO] lda model'
python ../06-latent-dirichlet-allocation/lda_recall.py $train $test
echo '[INFO] removing train and test datasets'
rm $train
rm $test
