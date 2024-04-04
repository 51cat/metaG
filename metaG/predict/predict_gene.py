from metaG.common.minana import MinAna
import os
from metaG.utils import get_software_path, seqtools_run
from metaG.software.interface import SoftInterface as SIF
from collections import defaultdict

class PREDICTer(MinAna):
    def __init__(self, 
                  contig_file,
                 sample_name,
                 outdir,
                 use = "prodigal",
                 config_file = None):
            super().__init__(outdir=outdir, step_name="predict")
            self.contig_file = contig_file
            self.outdir = outdir
            self.use = use
            self.sample_name = sample_name
            self.config_file = config_file
            self.out_json = defaultdict(lambda:defaultdict(str))

            self._steps_dir = f"03.predict/{self.use}_out/"
            self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
            self.make_step_outdir(self._steps_dir)
            self.prep_start()

            self.faa_out = f"{self.step_outdir}/{self.sample_name}_orf.faa"
            self.ffn_out = f"{self.step_outdir}/{self.sample_name}_orf.fna"
            self.anno = f"{self.step_outdir}/{self.sample_name}_anno.txt"
    
    def predict_gene(self):
        
        predict_infc = SIF(
            interpreter="python",
            work_dir=f"{self.step_outdir}/{self.sample_name}",
            path=get_software_path(self.use),
            contig_file = self.contig_file,
            faa_out = self.faa_out,
            ffn_out = self.ffn_out,
            out = f"{self.anno}",
            config_file = self.config_file,
        )

        predict_infc.mk_cmd()
        predict_infc.run_by_py()
        
        # write json
        self.out_json[self.sample_name]["ffn"] = os.path.abspath(self.ffn_out)
        self.out_json[self.sample_name]["faa"] = os.path.abspath(self.faa_out)
        self.write_json(self.out_json, f"{self.step_outdir}/{self.sample_name}_predict.json")
    
    @property
    def faa(self):
         return self.faa_out
    
    @property
    def ffn(self):
         return self.ffn_out
    
    @property
    def predict_json(self):
         return f"{self.step_outdir}/{self.sample_name}_predict.json"

    def run(self):
          self.predict_gene()