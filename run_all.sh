#!/bin/bash

set -e
train_file=$(readlink -f $1)
test_file=$(readlink -f $2)
RED='\033[1;31m' # Start red color
NC='\033[0m' # No more color

##### Guessing movie #####

# Frequency model
echo -e "${RED}Frequency model - guess movie${NC}"
cd 02-frequency-model
python cross-validation.py $train_file $test_file
echo ''

# Genre model
echo -e "${RED}Genre model - guess movie${NC}"
cd ../03-genre-model
python cross-validate.py $train_file $test_file
echo ''
echo -e "${RED}Genre model w/LDA (10 topics) - guess movie${NC}"
cd ../06-latent-dirichlet-allocation
python lda_cross.py -t=genre -p=movie --topics=10 $train_file $test_file
echo ''

# Genre-time model
echo -e "${RED}Genre-time model - guess movie${NC}"
cd ../04-time-model
python cross-validate.py $train_file $test_file
echo ''

# Cluster model
echo -e "${RED}Cluster model (40 clusters) - guess movie${NC}"
cd ../05-content-clustering
python clustering_cross_validation.py $train_file $test_file
echo ''
echo -e "${RED}Cluster model (40 clusters) w/LDA (10 topics) - guess movie${NC}"
cd ../06-latent-dirichlet-allocation
python lda_cross.py -t=cluster -p=movie --topics=10 $train_file $test_file
echo ''


##### Guessing group #####

# Genre model
echo -e "${RED}Genre model w/LDA (10 topics) - guess group${NC}"
cd ../06-latent-dirichlet-allocation
python lda_cross.py -t=genre -p=group --topics=10 $train_file $test_file
echo ''
echo -e "${RED}Genre model - guess group${NC}"
cd ../03-genre-model
python genre_cross.py $train_file $test_file
echo ''

# Cluster model
echo -e "${RED}Cluster model (40 clusters) w/LDA (10 topics) - guess group${NC}"
cd ../06-latent-dirichlet-allocation
python lda_cross.py -t=cluster -p=group --topics=10 $train_file $test_file
echo ''
# Need a script to test
# echo -e "${RED}Cluster model (40 clusters) - guess group${NC}"
# cd ../05-content-clustering
# python clustering_cross_validation.py $train_file $test_file
# echo ''
