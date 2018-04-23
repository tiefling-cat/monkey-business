DATA=/net/work/people/mediankin/snmt/data/czeng/pilot
MONKEY=/net/work/people/mediankin/snmt/neuralmonkey

bpe:
	gunzip -k $(DATA)/train/cz_lin.txt.gz
	gunzip -k $(DATA)/train/en.txt.gz
	paste $(DATA)/train/cz_lin.txt $(DATA)/train/en.txt | python3 $(MONKEY)/lib/subword_nmt/learn_bpe.py -s 50000 > $(DATA)/merge_file.bpe
