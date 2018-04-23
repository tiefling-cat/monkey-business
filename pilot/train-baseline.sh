#!/bin/bash

COMMON=/net/work/people/mediankin/snmt
DATA=$(COMMON)/data/czeng/pilot
MONKEY=$(COMMON)/neuralmonkey

source $(COMMON)/nm/bin/activate
$(MONKEY)/bin/neuralmonkey-train $(COMMON)/monkey-business/pilot/baseline.ini
