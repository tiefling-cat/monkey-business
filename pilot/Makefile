bpe:
	./make-bpe.sh 10000

train-baseline:
	qsub -cwd -j y -q gpu.q@dll[256] -l gpu=1,gpu_cc_min3.5=1,gpu_ram=2G -M mediankin@ufal.mff.cuni.cz -m beas ./train-baseline.sh
