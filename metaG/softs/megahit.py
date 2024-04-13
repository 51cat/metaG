import subprocess
import os
import metaG
from metaG.utils import parse_config_file
from dataclasses import dataclass
MEGAHIT_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/MEGAHIT/bin/megahit"

@dataclass
class MEGAHIT:
    r1 :str= None,
    r2 :str= None,
    out :str= None,
    config_file :str= None,
    min_contig_len :int = 500,
    cpu :int = None,
    memory :int = None

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