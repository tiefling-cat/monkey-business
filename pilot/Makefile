DATA=/net/work/people/mediankin/snmt/data/czeng/pilot
MONKEY=/net/work/people/mediankin/snmt/neuralmonkey

bpe:
	paste $(DATA)/train/cz_lin.txt.gz $(DATA)/train/en.txt.gz | python3 $(MONKEY)/lib/subword_nmt/learn_bpe.py -s 50000 > $(DATA)/merge_file.bpe
