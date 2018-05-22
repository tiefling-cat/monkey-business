#!/bin/bash

COMMON=/net/work/people/mediankin/snmt
DATA=${COMMON}/data/czeng/pilot
MONKEY=${COMMON}/neuralmonkey

source ~/.bashrc
source activate tf14
rm -rf /net/work/people/mediankin/snmt/experiments/pilot/baseline
${MONKEY}/bin/neuralmonkey-train ${COMMON}/monkey-business/pilot/baseline.ini
