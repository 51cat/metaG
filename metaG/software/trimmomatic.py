import argparse
import subprocess
from metaG.common.log import add_log
import os
import metaG
import re
import json
from collections import defaultdict

ADAPTER = f"ILLUMINACLIP:{os.path.dirname(metaG.__file__)}/lib/adapters/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:15 MINLEN:75"

class Trimmomatic:
    def __init__(self,
                 r1 = None, 
                 r2 = None,
                 sample_name = None,
                 out = None,
                 threads = 16,
                 phred = "phred33"
                 ) -> None:
        
        self.r1 = r1
        self.r2 = r2
        self.sample_name = sample_name
        self.out = out
        self.threads = threads
        self.phred = phred
        self._adapter = ADAPTER
        self._reads_dict = defaultdict(lambda: defaultdict(str))

    def mk_outdir(self):
        #r1_file_name = self.r1.split("/")[-1]  
        #r2_file_name = self.r2.split("/")[-1]  
        #self.r1_name = r1_file_name.split("fastq.gz")[0].rstrip(".")
        #self.r2_name = r2_file_name.split("fastq.gz")[0].rstrip(".")

        subprocess.check_call(f"mkdir -p {self.out}/paired/", shell= True)
        subprocess.check_call(f"mkdir -p {self.out}/unpaired/", shell= True)

        self.out_r1_pair = f"{self.out}/paired/{self.sample_name}_R1_pair.fastq.gz"
        self.out_r2_pair = f"{self.out}/paired/{self.sample_name}_R2_pair.fastq.gz"
        self.out_r1_unpair = f"{self.out}/unpaired/{self.sample_name}_R1_unpair.fastq.gz"
        self.out_r2_unpair = f"{self.out}/unpaired/{self.sample_name}_R2_unpair.fastq.gz"

        self._reads_dict[self.sample_name]["R1"] = os.path.abspath(self.out_r1_pair)
        self._reads_dict[self.sample_name]["R2"] = os.path.abspath(self.out_r2_pair)
    
    def run(self):
        self.mk_outdir()
        cmd = (
            f"trimmomatic PE "
            f"-threads {self.threads} "
            f"-{self.phred} "
            f"{self.r1} {self.r2} "
            f"{self.out_r1_pair} {self.out_r1_unpair} {self.out_r2_pair} {self.out_r2_unpair} \\"
            f"{self._adapter}"
            )
        subprocess.check_call(cmd, shell= True)
        
        with open(f"{self.out}/{self.sample_name}_trimmomatic_stat.json", "w") as fd:
            json.dump(self._reads_dict, fd, indent=4)

        

def main():
    parser = argparse.ArgumentParser(description='Warpper for trimmomatic')
    parser.add_argument('--r1', help='', required=True)
    parser.add_argument('--r2', help='', required=True)
    parser.add_argument('--out', help='', required=True)
    parser.add_argument('--sample_name', help='', required=True)
    parser.add_argument('--phred', help='', default="phred33")
    args = parser.parse_args()

    runner = Trimmomatic(
        r1 = args.r1,
        r2 = args.r2,
        out = args.out,
        phred = args.phred,
        sample_name = args.sample_name
    )

    runner.run()
    
if __name__ == '__main__':
    main()