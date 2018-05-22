COMMON=/net/work/people/mediankin/snmt
DATA=$(COMMON)/data/czeng/pilot
TRAIN=$(DATA)/train
MONKEY=$(COMMON)/neuralmonkey

bpe:
	gunzip -k $(TRAIN)/cz_lin.txt.gz
	gunzip -k $(TRAIN)/en.txt.gz
	paste $(TRAIN)/cz_lin.txt $(TRAIN)/en.txt | python3 $(MONKEY)/lib/subword_nmt/learn_bpe.py -s 10000 > $(TRAIN)/merge_file.bpe
	$(MONKEY)/lib/subword_nmt/apply_bpe.py -i $(TRAIN)/cz_lin.txt -c $(TRAIN)/merge_file.bpe -o $(TRAIN)/cz_lin_bpe.txt
	$(MONKEY)/lib/subword_nmt/apply_bpe.py -i $(TRAIN)/en.txt -c $(TRAIN)/merge_file.bpe -o $(TRAIN)/en_bpe.txt

	echo 'token     count' >$(TRAIN)/header.txt

	cat $(TRAIN)/en_bpe.txt | tr ' ' '\n' | sort | uniq -c | sort -hr >$(TRAIN)/en_cnt.txt
	cat $(TRAIN)/en_cnt.txt | sed "s/^ \+//g" | sed "s/^\([^ ]\+\) \+\([^ ]\+\)$/\2\t\1/g" >$(TRAIN)/en_voc_.csv
	cat $(TRAIN)/header.txt $(TRAIN)/en_voc_.csv >$(TRAIN)/en_voc.csv
	rm $(TRAIN)/en_cnt.txt $(TRAIN)/en_voc_.csv

	cat $(TRAIN)/cz_lin_bpe.txt | tr ' ' '\n' | sort | uniq -c | sort -hr >$(TRAIN)/cz_cnt.txt
	cat $(TRAIN)/cz_cnt.txt | sed 's/^ \+//g' | sed 's/^\([^ ]\+\) \+\([^ ]\+\)$/\2\t\1/g' >$(TRAIN)/cz_voc_.csv
	cat $(TRAIN)/header.txt $(TRAIN)/cz_voc_.csv >$(TRAIN)/cz_voc.csv
	rm $(TRAIN)/cz_cnt.txt $(TRAIN)/cz_voc_.csv

train-baseline:
	qsub -cwd -j y -q gpu.q@dll[256] -l gpu=1,gpu_cc_min3.5=1,gpu_ram=2G -M mediankin@ufal.mff.cuni.cz -m beas ./train-baseline.sh
