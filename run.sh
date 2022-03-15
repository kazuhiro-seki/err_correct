#!/bin/bash

#$ -l rt_G.small=1
#$ -l h_rt=6:00:00
#$ -j y
#$ -cwd
#$ -m e

source /etc/profile.d/modules.sh
module load python/3.6/3.6.12 cuda/10.0/10.0.130.1 cudnn/7.6/7.6.5
source venv/bin/activate

fairseq-train data-bin/iwslt14.tokenized.de-en --optimizer nag --lr 0.25 --clip-norm 0.1 --dropout 0.2 --max-tokens 4000 --arch fconv_iwslt_de_en --save-dir checkpoints/fconv
