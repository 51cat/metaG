import subprocess
import os
import metaG
from metaG.utils import parse_config_file
from dataclasses import dataclass

PRODIGAL_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/prodigal/prodigal"
ARGS_JSON = f"{os.path.dirname(metaG.__file__)}/lib/softs/prodigal/args.json"

@dataclass
class PRODIGAL:
    contig_file :str = None,
    faa_out :str = None,
    ffn_out :str = None,
    out :str = None,
    config_file :str = None,
    cpu : int =  None,
    memory : int = None

    def run(self):
        cmd = (
            f"{PRODIGAL_PATH} -i {self.contig_file} -p meta -q -a {self.faa_out} -d {self.ffn_out} -o {self.out} "
        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "PRODIGAL", args_json=ARGS_JSON,args_prfx="-")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)