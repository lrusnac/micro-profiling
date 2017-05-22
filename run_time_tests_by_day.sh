#!/bin/bash

PHYS_DIR=`pwd -P`
fulldataset=$PHYS_DIR/$1

dataset=$(basename "$fulldataset")
fulldatasetnofilename="${dataset%.*}"

splitedbytime=$fulldatasetnofilename'_divided_by_time.csv'
cd 00-common

python split_customer.py $dataset -d="day"
out_file="to_be_defined.csv"

head -n1 $splitedbytime > $out_file
tail -n+2 $splitedbytime | sort >> $out_file

rm $splitedbytime
python split_data.py $out_file

train="to_be_defined_train.csv"
test="to_be_defined_test.csv"

python ../06-latent-dirichlet-allocation/lda_recall.py $train $test
rm $train
rm $test
