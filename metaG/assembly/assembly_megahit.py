from metaG.common.minana import MinAna
from metaG.utils import get_software_path
from metaG.common.seqtools import SeqProcesser
from metaG.software.interface import SoftInterface as SIF
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

def draw_histogram(file_path, column_name, output_file):
    df = pd.read_table(file_path)
    column_data = np.log10(df[column_name] + 1)
    plt.hist(column_data, bins=100, color='skyblue', alpha=0.8)
    plt.title(f'Histogram of {column_name}')
    plt.xlabel(f"log10({column_name})")
    plt.ylabel('Frequency')
    plt.savefig(output_file)
    plt.close()


class MEGAHITer(MinAna):
     def __init__(self, 
                 r1, 
                 r2, 
                 sample_name,
                 outdir,
                 min_contig_len = 500,
                 config_file = None):
            super().__init__(outdir=outdir, step_name="assembly")
            self.r1 = r1
            self.r2 = r2
            self.outdir = outdir
            self.sample_name = sample_name
            self.config_file = config_file
            self.min_contig_len = min_contig_len

            self.raw_contig = None
            self.clean_contig = None

            self._steps_dir = f"02.assembly/megahit_out/"
            self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
            self.make_step_outdir(self._steps_dir)
            self.prep_start()
    
     def assembly_megahit(self):
        
        MEGAHIT_infc = SIF(
            interpreter="python",
            work_dir=f"{self.step_outdir}/{self.sample_name}",
            path=get_software_path("megahit"),
            r1 = self.r1,
            r2 = self.r2,
            out = f"{self.step_outdir}/{self.sample_name}",
            config_file = self.config_file,
            min_contig_len = self.min_contig_len
        )

        MEGAHIT_infc.mk_cmd()
        MEGAHIT_infc.run_by_py()

        self.raw_contig = f"{self.step_outdir}/{self.sample_name}/final.contigs.fa"
        self.clean_contig = f"{self.parent_dir}/{self.sample_name}_clean.contigs.fa"
        
        sp = SeqProcesser()
        sp.set_in_fa(self.raw_contig)
        sp.set_out_fa(self.clean_contig)
        sp.rename(target_name=self.sample_name)
        
        self.write_json({self.sample_name:os.path.abspath(self.clean_contig)}, 
                        f"{self.step_outdir}/{self.sample_name}_contigs_clean.json")


     def count_contig_len(self):
          os.system(f"mkdir -p {self.parent_dir}/contig_count/")

          sp = SeqProcesser()
          sp.set_in_fa(self.clean_contig)
          sp.getlen(f"{self.parent_dir}/contig_count/{self.sample_name}_length.tsv")
          

          draw_histogram(
              file_path= f"{self.parent_dir}/contig_count/{self.sample_name}_length.tsv",
               column_name="seq_len",
               output_file = f"{self.parent_dir}/contig_count/{self.sample_name}_length.png"
          )

     def fa2gz(self):
          os.system(f"gzip {self.clean_contig}")

     def get_clean_json(self):
          return f"{self.step_outdir}/{self.sample_name}_contigs_clean.json"

     def run(self):
         self.assembly_megahit()
         self.count_contig_len()
         #self.fa2gz()
         