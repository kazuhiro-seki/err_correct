#!/bin/bash

#$ -l rt_G.small=1
#$ -l h_rt=1:00:00
#$ -j y
#$ -cwd
#$ -m e

source /etc/profile.d/modules.sh
module load python/3.6/3.6.12 cuda/10.0/10.0.130.1 cudnn/7.6/7.6.5
source venv/bin/activate

#model=transformer_iwslt_de_en_nag
model=transformer_nag

fairseq-generate data-bin/transcript.tokenized.1m --path checkpoints/$model/checkpoint_best.pt --batch-size 128 --beam 5 --remove-bpe
