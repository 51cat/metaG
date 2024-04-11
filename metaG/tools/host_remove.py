import os
import pysam
import json
import pandas as pd
from collections import defaultdict
from functools import partial

from metaG.softs.bwa import BWA
from metaG.core.log import add_log
from metaG.core.minana import MinAna

class HostRemover(MinAna):
    def __init__(self, 
                 r1, 
                 r2, 
                 host,
                 genome_dir,
                 sample_name, 
                 outdir):
            super().__init__(outdir=outdir)
            self.r1 = r1
            self.r2 = r2
            self.host = host
            self.genome_dir = genome_dir
            self.sample_name = sample_name
            self._reads_dict = defaultdict(partial(defaultdict, str))
            self.host_remove_use = "bwa"
            
            self.out_bam = f"{self.outdir}/{self.sample_name}_host.bam"
            self.out_r1 = f"{self.outdir}/{self.sample_name}_clean_R1.fastq"
            self.out_r2 = f"{self.outdir}/{self.sample_name}_clean_R2.fastq"
            self.remove_host_json = f"{self.outdir}/{self.sample_name}_clean_data.json"
            self.host_count_table = f"{self.outdir}/{self.sample_name}_host_count.tsv"

            self.host_remove_soft = {
                "bwa":self.host_remove_BWA
            }

    def set_host_remove_use(self, use):
        self.host_remove_use = use

    @add_log
    def host_remove_BWA(self):
        
        runner = BWA(
                host=self.host,
                r1 = self.r1,
                r2 = self.r2,
                mode = "map",
                genome_dir = self.genome_dir,
                cpu=self.cpu,
                memory=self.memory
            )
        runner.set_mem_out_bam(self.out_bam)
        runner.run()
    

    @add_log
    def extract_reads_from_bam(self):
        nprocess = 0
        self.count_dict = {
             "drop_nreads":0,
             "target_nreads":0,
             "sample_name": self.sample_name
        }



        self._reads_dict[self.sample_name]["R1"] = os.path.abspath(f"{self.out_r1}")
        self._reads_dict[self.sample_name]["R2"] = os.path.abspath(f"{self.out_r2}")

        r1_writer = open(self.out_r1, "w")
        r2_writer = open(self.out_r2, "w")

        bam = pysam.AlignmentFile(self.out_bam)
        for r in bam:
            nprocess += 1
            if nprocess % 5000000 == 0:
                self.extract_reads_from_bam.logger.info(f"Process reads: {nprocess}")
            f1 = r.reference_name is None
            f2 = r.is_paired
            if f1 & f2:
                self.count_dict["target_nreads"] += 1
                
                if r.is_read1:
                     r1_writer.write(f'@{r.qname}\n{r.seq}\n+\n{r.qual}\n')
                
                if r.is_read2:
                     r2_writer.write(f'@{r.qname}\n{r.seq}\n+\n{r.qual}\n')
            else:
                 self.count_dict["drop_nreads"] += 1
        r1_writer.close()
        r2_writer.close()
    
    def out_count_detail(self):
        self.write_json(self._reads_dict, self.remove_host_json)
        pd.DataFrame([self.count_dict]).to_csv(
            self.host_count_table, index=None, sep="\t")
    

    def get_clean_r1_r2_path(self):
        stat_file = f"{self.outdir}/{self.sample_name}_clean_data.json"
        with open(stat_file, 'r') as f:
            data = json.load(f)
        return data[self.sample_name]['R1'], data[self.sample_name]['R2']

    @property
    def clean_r1_r2(self):
        return self.out_r1, self.out_r2

    @property
    def clean_r1_r2_json(self):
        return self.remove_host_json

    def run(self):
        self.host_remove_soft[self.host_remove_use]()
        self.extract_reads_from_bam()
        self.out_count_detail()
    
