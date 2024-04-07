import argparse
import subprocess
from metaG.common.log import add_log
import os
import metaG
import re
import json
from metaG.utils import parse_config_file
from collections import defaultdict
from metaG import get_default_cpus

ADAPTER = f"ILLUMINACLIP:{os.path.dirname(metaG.__file__)}/lib/adapters/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:15 MINLEN:75"

def mk_trim_rules(
        adapter_fa, 
        mismatch,
        match_pct,
        match_pct_force,
        slide_window,
        min_len,
        plate = 'ILLUMINACLIP'):
    return f"{plate}:{adapter_fa}:{mismatch}:{match_pct}:{match_pct_force} SLIDINGWINDOW:{slide_window} MINLEN:{min_len}"
    

class Trimmomatic:
    def __init__(self,
                 r1 = None, 
                 r2 = None,
                 sample_name = None,
                 out = None,
                 phred = "phred33",
                 config_file = None,
                 cpu = None,
                 memory = None
                 ) -> None:
        
        self.r1 = r1
        self.r2 = r2
        self.sample_name = sample_name
        self.out = out
        self.cpu = cpu
        self.memory = memory
        self.phred = phred
        self._adapter = ADAPTER
        self.config_file = config_file
        self._reads_dict = defaultdict(lambda: defaultdict(str))
    

    def mk_outdir(self):

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

        if self.config_file not in [None, "None"]:
            config_dict = parse_config_file(self.config_file, key="Trimmomatic", return_dict=True)
            self._adapter = mk_trim_rules(
                config_dict["adapter_fa"],
                config_dict["mismatch"],
                config_dict["match_pct"],
                config_dict["match_pct_force"],
                config_dict["slide_window"],
                config_dict["min_len"],
                config_dict["plate"]
            )

        cmd = (
            f"trimmomatic PE "
            f"-threads {self.cpu} "
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
    parser.add_argument('--config_file', help='', default=None)
    parser.add_argument('--cpu', help='', default=get_default_cpus())
    args = parser.parse_args()

    runner = Trimmomatic(
        r1 = args.r1,
        r2 = args.r2,
        out = args.out,
        phred = args.phred,
        sample_name = args.sample_name,
        config_file=args.config_file,
        cpu = args.cpu
    )

    runner.run()
    
if __name__ == '__main__':
    main()