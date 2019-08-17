
## RUN HMMs
## generate config.yaml for samples
perl ../scripts/generate_sample_yaml.pl /data/pathogens/ > config_pathogens.yaml
perl ../scripts/generate_sample_yaml.pl /data/healthy_contigs/ > config_healthy.yaml

# Snakemake is not working yet
# do it manually 

ls /data/pathogens/*.fasta | while read f; do \
	hmmsearch -E 1e-5 --cpu 8 --domtblout $f.tab \
	/home/ousmane.cisse/DATA/NCBI_hack/data/processed/VFDB/VFDB_setA_nt.hmm \
	$f;done

ls /data/healthy_contigs/*.fasta | while read f; do \
	hmmsearch -E 1e-5 --cpu 8 --domtblout $f.tab \
	/home/ousmane.cisse/DATA/NCBI_hack/data/processed/VFDB/VFDB_setA_nt.hmm \
	$f;done

