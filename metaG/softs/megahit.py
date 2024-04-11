import subprocess
import os
import metaG
from metaG.utils import parse_config_file

MEGAHIT_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/MEGAHIT/bin/megahit"

class MEGAHIT:
    def __init__(self,
                 r1 = None,
                 r2 = None,
                 out = None,
                 config_file = None,
                 min_contig_len = 500,
                 cpu = None,
                 memory = None
                 ) -> None:
        
        self.r1 = r1
        self.r2 = r2
        self.out = out
        self.min_contig_len = min_contig_len
        self.config_file = config_file
        self.cpu = cpu
        self.memory = memory
    
    def run(self):
        cmd = (
            f"{MEGAHIT_PATH} "
            f"-1 {self.r1} "
            f"-2 {self.r2} "
            f"-o {self.out} "
            f"--min-contig-len {self.min_contig_len} "
            f"--num-cpu-threads {self.cpu} "
            f"--memory 0.9 "
        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "MEGAHIT")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)