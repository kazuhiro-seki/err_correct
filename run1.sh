#!/bin/bash

#$ -l rt_G.small=1
#$ -l h_rt=36:00:00
#$ -j y
#$ -cwd
#$ -m e

source /etc/profile.d/modules.sh
module load python/3.6/3.6.12 cuda/10.0/10.0.130.1 cudnn/7.6/7.6.5
source venv/bin/activate

#model=transformer_iwslt_de_en
model=transformer

optimizer=nag
#optimizer=adam

fairseq-train data-bin/transcript.tokenized.1m --optimizer $optimizer --lr 0.25 --clip-norm 0.1 --dropout 0.2 --max-tokens 4000 --arch $model --save-dir checkpoints/${model}_${optimizer} --max-epoch 100 --no-epoch-checkpoints \
--lr-scheduler inverse_sqrt --warmup-updates 8000 --warmup-init-lr 1e-7 
#--adam-betas '(0.9, 0.98)'


# https://github.com/pytorch/fairseq/issues/1239

# I've been dealing with the same problem, but for other language pair (et-en). I solved my problem adding the following flags to fairseq-train:

# --lr-scheduler inverse_sqrt --warmup-updates 8000 --warmup-init-lr 1e-7
# After these flags were added, the training started to work perfectly. Check out https://arxiv.org/pdf/1706.03762.pdf#optimizer and https://www.borealisai.com/en/blog/tutorial-17-transformers-iii-training/ --> "Learning rate warm-up"
