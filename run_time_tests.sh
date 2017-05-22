#!/bin/bash

PHYS_DIR=`pwd -P`
fulldataset=$PHYS_DIR/$1

dataset=$(basename "$fulldataset")
fulldatasetnofilename="${dataset%.*}"

splitedbytime=$fulldatasetnofilename'_divided_by_time.csv'
cd 00-common

#python split_customer.py $dataset -d -n2 # by day 2 periods (weekday and weekend)

for j in `seq 2 3`;
do
    n=$((24/$j-1))
    for i in `seq 0 $n`;
    do
        echo '== '$j' intervals, starting at '$i' =='
        python split_customer.py $dataset -n$j -s$i
        export out_file="to_be_defined.csv" ;
        head -n1 $splitedbytime > $out_file ; tail -n+2 $splitedbytime | sort >> $out_file
        rm $splitedbytime
        python split_data.py $out_file
        python ../06-latent-dirichlet-allocation/lda_recall.py $train $test
        rm $train
        rm $test
    done
done
