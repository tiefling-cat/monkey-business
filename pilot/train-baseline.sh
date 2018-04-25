#!/bin/bash

COMMON=/net/work/people/mediankin/snmt
DATA=${COMMON}/data/czeng/pilot
MONKEY=${COMMON}/neuralmonkey

source ~/.bashrc
source activate tf15
#source ${COMMON}/nmenv/bin/activate
#source /a/merkur3/kocmanek/ANACONDA/envs/tf15/bin/activate
${MONKEY}/bin/neuralmonkey-train ${COMMON}/monkey-business/pilot/baseline.ini
