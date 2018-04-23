COMMON=/net/work/people/mediankin/snmt
DATA=$(COMMON)/data/czeng/pilot
MONKEY=$(COMMON)/neuralmonkey

bpe:
	gunzip -k $(DATA)/train/cz_lin.txt.gz
	gunzip -k $(DATA)/train/en.txt.gz
	paste $(DATA)/train/cz_lin.txt $(DATA)/train/en.txt | python3 $(MONKEY)/lib/subword_nmt/learn_bpe.py -s 50000 > $(DATA)/merge_file.bpe

train-baseline:
	qsub -cwd -j y -q gpu.q -l gpu=1,gpu_cc_min3.5=1,gpu_ram=2G ./train-baseline.sh
	#/home/bojar/tools/shell/qsubmit --gpus=1 --gpumem=2G --queue="gpu.q" --logdir="$(DATA)" $(MONKEY)/bin/neuralmonkey-train $(COMMON)/monkey-business/pilot/baseline.ini
