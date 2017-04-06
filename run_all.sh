#!/bin/bash

##### Guessing movie #####

# Frequency model
echo 'Frequency model - guess movie'
cd 02-frequency-model
python cross-validation.py $1 $2

# Genre model
echo 'Genre model - guess movie'
cd ../03-genre-model
python cross-validate.py $1 $2
echo 'Genre model w/LDA (10 topics) - guess movie'
cd ../06-latent-dirichlet-allocation
python lda-cross.py --genre --movie --topics=10 $1 $2

# Genre-time model
echo 'Genre-time model - guess movie'
cd ../04-time-model
python cross-validate.py $1 $2

# Cluster model
echo 'Cluster model (40 clusters) - guess movie'
cd ../05-content-clustering
python clustering-cross-validation.py $1 $2
echo 'Cluster model (40 clusters) w/LDA (10 topics) - guess movie'
cd ../06-latent-dirichlet-allocation
python lda-cross.py --cluster --movie --topics=10 $1 $2


##### Guessing group #####

# Genre model
echo 'Genre model w/LDA (10 topics) - guess group'
cd ../06-latent-dirichlet-allocation
python lda-cross.py --genre --group --topics=10 $1 $2
echo 'Genre model - guess group'
cd ../03-genre-model
python genre_cross.py $1 $2

# Cluster model
echo 'Cluster model (40 clusters) w/LDA (10 topics) - guess group'
cd ../06-latent-dirichlet-allocation
python lda-cross.py --cluster --group --topics=10 $1 $2
# Need a script to test
# echo 'Cluster model (40 clusters) - guess group'
# cd ../05-content-clustering
# python clustering-cross-validation.py $1 $2
