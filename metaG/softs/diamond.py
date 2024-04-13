import subprocess
import os
import metaG
from metaG.utils import parse_config_file
from dataclasses import dataclass

DIAMOND_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/DIAMOND/diamond"
DATABASE_PATH = f"{os.path.dirname(metaG.__file__)}/lib/database/DIAMOND/"

@dataclass
class DIAMOND:
    query_fa :str = None,
    database_name :str = None,
    diamond_method :str = "blastp",
    min_evalue :float = 0.00001,
    min_identity :int = 80,
    format :int = 6,
    max_target_seqs :int = 10,
    tmp_out :str= None,
    out :str= None,
    block_size :int = 8, 
    config_file :str = None,
    cpu :int = None,
    memory :int = None
    
    def run(self):
        cmd = (
            f"{DIAMOND_PATH} "
            f"{self.diamond_method} "
            f"--query {self.query_fa} "
            f"--db {DATABASE_PATH}/{self.database_name}/{self.database_name} "
            f"--out {self.out} "
            f"--outfmt {self.format} "
            f"--evalue {self.min_evalue} "
            f"--max-target-seqs {self.max_target_seqs} "
            f"--id {self.min_identity} "
            f"--block-size {self.block_size} "
            f"--threads {self.cpu} "
        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "DIAMOND")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)