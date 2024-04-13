

import os
import pandas as pd
from functools import partial
from collections import defaultdict
from metaG.tools.seqtools import  SeqProcesser
from metaG.softs.diamond import DIAMOND
from metaG.core.minana import MinAna

DIAMOND_COLS = ["qseqid", "sseqid", "pident", "length", "mismatch", 
                "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"]

class Annoater(MinAna):
    def __init__(self, 
                 query_fa = None,
                 uniq_gene_fa = None,
                 database_name = None,
                 outdir = None,
                 config_file = None,
                 **kwargs
                 ):
            super().__init__(outdir=outdir, **kwargs)
            self.query_fa = query_fa
            self.uniq_gene_fa = uniq_gene_fa
            self.database_name = database_name
            self.config_file = config_file
            self.filter_df = None

            self.annoate_use = "diamond"
            self.annoate_soft = {
                 "diamond":self.annoate_diamond
            }

            self._anno_out_raw = f"{self.outdir}/annotation_raw.tsv"
            self._anno_out_filter = f"{self.outdir}/annotation_filter.tsv"
            self._gene_length_json = f"{self.outdir}/gene_length.json"
            self._gene_annoate_json = f"{self.outdir}/gene_annoate.json"
            self.tmp_out = f"{self.outdir}/tmp/"
            
    def set_annoate_use(self, use):
         self.annoate_use = use

    def annoate_diamond(self):
        
        runner = DIAMOND(
                 query_fa=self.query_fa,
                 database_name=self.database_name,
                 diamond_method=self.diamond_method,
                 min_evalue=self.min_evalue,
                 min_identity=self.min_identity,
                 format=self.format,
                 max_target_seqs=self.max_target_seqs,
                 tmp_out=self.tmp_out,
                 block_size=self.block_size,
                 out = self._anno_out_raw,
                 config_file = self.config_file,
                 cpu = self.cpu,
                 memory = self.memory
        )
        runner.run()
     
    def filter_res(self):
         raw_df = pd.read_table(self._anno_out_raw, header=None)
         raw_df.columns = DIAMOND_COLS
         self.filter_df = raw_df.loc[raw_df.groupby('qseqid')['bitscore'].idxmax()]
         self.filter_df.to_csv(self._anno_out_filter, sep = "\t", index= None)

    def create_gene_info_length(self):
         info_dict= {}
         length_dict = {}
         for _, row in self.filter_df.iterrows():
              info_dict.update({row["qseqid"]:row["sseqid"]})
         self.write_json(info_dict, self._gene_annoate_json)

         sp = SeqProcesser()
         length_file = f"{self.outdir}/__len.tsv"
         sp.set_in_fa(self.uniq_gene_fa)
         sp.getlen(length_file)

         length_df = pd.read_table(length_file)
         for _, row in length_df.iterrows():
              try:
                  new_seq_name = info_dict[row['seq_name']]
                  length_dict.update({new_seq_name:row['seq_len']})
              except KeyError:
                   pass
         self.write_json(length_dict, self._gene_length_json)
         self.add_rubbish(length_file)
     
    @property
    def anno_raw(self):
         return self._anno_out_raw
    
    @property
    def anno_filter(self):
         return os.path.abspath(self._anno_out_filter)
    
    @property
    def gene_length(self):
         return os.path.abspath(self._gene_length_json)

    @property
    def gene_annoate(self):
         return os.path.abspath(self._gene_annoate_json)

    def run(self):
         self.annoate_soft[self.annoate_use]()
         self.filter_res()
         self.create_gene_info_length()
         self.clean()