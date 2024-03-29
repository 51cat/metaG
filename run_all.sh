metaG pre-process \
   --rawdata_table ./data/raw_file.list\
   --host rice \
   --outdir ./test/out/

metaG assembly \
   --outdir ./test/out/ \
   --min_contig_len 500
