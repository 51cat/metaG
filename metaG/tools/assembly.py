import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from metaG.core.minana import MinAna
from metaG.tools.seqtools import SeqProcesser
from metaG.softs.megahit import MEGAHIT

def draw_histogram(file_path, column_name, output_file):
    df = pd.read_table(file_path)
    column_data = np.log10(df[column_name] + 1)
    plt.hist(column_data, bins=100, color='skyblue', alpha=0.8)
    plt.title(f'Histogram of {column_name}')
    plt.xlabel(f"log10({column_name})")
    plt.ylabel('Frequency')
    plt.savefig(output_file)
    plt.close()

class Assemblyer(MinAna):
        def __init__(
                self, 
                r1, 
                r2, 
                sample_name,
                outdir,
                min_contig_len = 500,
                config_file = None):
            super().__init__(outdir=outdir)
            self.r1 = r1
            self.r2 = r2
            self.outdir = outdir
            self.sample_name = sample_name
            self.config_file = config_file
            self.min_contig_len = min_contig_len

            self.assembly_use = "MEGAHIT"
            self.raw_contig = f"{self.outdir}/{self.sample_name}/final.contigs.fa"
            self.clean_contig = f"{self.outdir}/{self.sample_name}_clean.contigs.fa"

            self.assembly_soft = {
                 "MEGAHIT":self.assembly_MEGAHIT
            }

        def set_assembly_use(self, use):
             self.assembly_use = use

        def assembly_MEGAHIT(self):
             runner = MEGAHIT(
                  r1 = self.r1,
                  r2 = self.r2,
                  min_contig_len = self.min_contig_len,
                  out = f"{self.outdir}/{self.sample_name}/",
                  config_file= self.config_file,
                  cpu = self.cpu,
                  memory=self.memory
             )
             runner.run()

        def analysis_contig_len(self):
            sp = SeqProcesser()
            count_dir = f"{self.outdir}/contig_count/"
            os.system(f"mkdir -p {count_dir}")

            sp = SeqProcesser()
            sp.set_in_fa(self.raw_contig)
            sp.set_out_fa(self.clean_contig)
            sp.rename(target_name=self.sample_name)
               
            self.write_json({self.sample_name:os.path.abspath(self.clean_contig)}, 
                              f"{self.outdir}/{self.sample_name}_contigs_clean.json")

            sp = SeqProcesser()
            sp.set_in_fa(self.clean_contig)
            sp.getlen(f"{self.outdir}/contig_count/{self.sample_name}_length.tsv")
            
            draw_histogram(
                file_path= f"{count_dir}/{self.sample_name}_length.tsv",
                column_name="seq_len",
                output_file = f"{count_dir}/{self.sample_name}_length.png"
            )
        
        def run(self):
             self.assembly_soft[self.assembly_use]()
             self.analysis_contig_len()

        @property
        def clean_tag(self):
             return self.clean_contig