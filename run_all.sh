rm -rf ./test_preprocess
metaG pre-process \
   --rawdata_table ./data/raw_file.list\
   --host rice \
   --outdir ./test_preprocess/ \
   --config_file configs.yaml

metaG assembly \
   --outdir ./test_preprocess/ \
   --min_contig_len 200 \
   --config_file configs.yaml

metaG predict-gene \
   --outdir ./test_preprocess/ \
   --use prodigal