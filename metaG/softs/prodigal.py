import argparse
import subprocess
import os
import metaG
from metaG.utils import parse_config_file

PRODIGAL_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/prodigal/prodigal"
ARGS_JSON = f"{os.path.dirname(metaG.__file__)}/lib/softs/prodigal/args.json"

class PRODIGAL:
    def __init__(self,
                 contig_file,
                 faa_out,
                 ffn_out,
                 out,
                 config_file = None,
                 cpu = None,
                 memory = None
                 ) -> None:
        
        self.contig_file = contig_file
        self.faa_out = faa_out
        self.ffn_out = ffn_out
        self.out = out
        self.config_file = config_file
        self.cpu = cpu
        self.memory = memory
    
    def run(self):
        cmd = (
            f"{PRODIGAL_PATH} -i {self.contig_file} -p meta -q -a {self.faa_out} -d {self.ffn_out} -o {self.out} "
        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "PRODIGAL", args_json=ARGS_JSON,args_prfx="-")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)