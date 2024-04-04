import pysam
import json
import os
import gzip
import pandas as pd
from metaG.common.log import add_log
from metaG.common.minana import MinAna
from metaG.utils import get_software_path
from metaG.software.interface import SoftInterface as SIF
from collections import defaultdict

class HostRemover(MinAna):
    def __init__(self, 
                 r1, 
                 r2, 
                 host,
                 genome_dir,
                 sample_name, 
                 outdir):
            super().__init__(outdir=outdir, step_name="prep")
            self.r1 = r1
            self.r2 = r2
            self.host = host
            self.genome_dir = genome_dir
            self.sample_name = sample_name
            self.outdir = outdir
            self._reads_dict = defaultdict(lambda:defaultdict(str))

            self._steps_dir = "01.prep/remove_host/"
            self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
            self.make_step_outdir(self._steps_dir)
            self.prep_start()

    
    @add_log
    def map_reads_to_host(self):
        
        self.out_bam = f"{self.step_outdir}/{self.sample_name}_host.bam"

        bwa_mem_infc = SIF(
            interpreter="python",
            work_dir= self.step_outdir,
            path=get_software_path("bwa"),
            host = self.host,
            fa = None,
            mode = "mem",
            genome_dir = self.genome_dir,
            r1 = self.r1,
            r2 = self.r2,
            out = self.step_outdir,
            mem_out_file_name = self.out_bam
        )

        bwa_mem_infc.mk_cmd()
        bwa_mem_infc.run_by_py()
    
    @add_log
    def extract_reads_from_bam(self):
        nprocess = 0
        self.count_dict = {
             "drop_nreads":0,
             "target_nreads":0,
             "sample_name": self.sample_name
        }

        self.out_r1 = f"{self.step_outdir}/{self.sample_name}_clean_R1.fastq"
        self.out_r2 = f"{self.step_outdir}/{self.sample_name}_clean_R2.fastq"

        self._reads_dict[self.sample_name]["R1"] = os.path.abspath(f"{self.out_r1}.gz")
        self._reads_dict[self.sample_name]["R2"] = os.path.abspath(f"{self.out_r2}.gz")

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
        self.compress_file(self.out_r1, self.out_r2)
    
    def out_count_detail(self):
         
        with open(f"{self.step_outdir}/{self.sample_name}_clean_data.json", "w") as fd:
            json.dump(self._reads_dict, fd, indent=4)
        
        df = pd.DataFrame([self.count_dict])
        df.to_csv(f"{self.step_outdir}/{self.sample_name}_host_count.tsv", index=None, sep="\t")
        
    def get_clean_r1_r2_path(self):
        stat_file = f"{self.step_outdir}/{self.sample_name}_clean_data.json"
        with open(stat_file, 'r') as f:
            data = json.load(f)
        return data[self.sample_name]['R1'], data[self.sample_name]['R2']

    def run(self):
        self.map_reads_to_host()
        self.extract_reads_from_bam()
        self.out_count_detail()
    
