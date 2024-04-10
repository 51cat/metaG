
import os
from functools import partial
from collections import defaultdict

from metaG.softs.prodigal import PRODIGAL
from metaG.core.minana import MinAna

class Predicter(MinAna):
    def __init__(self, 
                  contig_file,
                 sample_name,
                 outdir,
                 config_file = None):
            super().__init__(outdir=outdir)
            self.contig_file = contig_file
            self.outdir = outdir
            self.sample_name = sample_name
            self.config_file = config_file
            self.out_json = defaultdict(partial(defaultdict, str))
            self.predict_use = "prodigal"

            self._faa_out = f"{self.outdir}/{self.sample_name}_orf.faa"
            self._ffn_out = f"{self.outdir}/{self.sample_name}_orf.fna"
            self._anno = f"{self.outdir}/{self.sample_name}_anno.txt"
            self._predict_json = f"{self.outdir}/{self.sample_name}_predict.json"
            
            self.predict_soft = {
                 "prodigal":self.predict_prodigal
            }

    def set_predict_use(self, use):
         self.predict_use = use

    def predict_prodigal(self):
        
        runner = PRODIGAL(
                 contig_file = self.contig_file,
                 faa_out = self._faa_out,
                 ffn_out = self._ffn_out,
                 out = self._anno,
                 config_file = self.config_file,
                 cpu = self.cpu,
                 memory = self.memory
        )
        runner.run()
        # write json
        self.out_json[self.sample_name]["ffn"] = os.path.abspath(self._ffn_out)
        self.out_json[self.sample_name]["faa"] = os.path.abspath(self._faa_out)
        self.write_json(self.out_json, f"{self.outdir}/{self.sample_name}_predict.json")

    @property
    def faa(self):
         return self._faa_out
    
    @property
    def ffn(self):
         return self._ffn_out
    
    @property
    def predict_json(self):
         return self._predict_json

    def run(self):
          self.predict_soft[self.predict_use]()