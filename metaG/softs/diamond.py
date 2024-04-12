import subprocess
import os
import metaG
from metaG.utils import parse_config_file

DIAMOND_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/DIAMOND/diamond"
DATABASE_PATH = f"{os.path.dirname(metaG.__file__)}/lib/database/DIAMOND/"

class DIAMOND:
    def __init__(self,
                 query_fa = None,
                 database_name = None,
                 method = "blastp",
                 min_evalue =0.00001,
                 min_identity = 80,
                 format = 6,
                 max_target_seqs = 10,
                 tmp_out = None,
                 out = None,
                 block_size = 8, 
                 config_file = None,
                 cpu = None,
                 memory = None
                 ) -> None:
        
        self.query_fa = query_fa
        self.database_name = database_name
        self.method = method
        self.out = out
        self.min_evalue = min_evalue
        self.max_target_seqs = max_target_seqs
        self.tmp_out = tmp_out
        self.format = format
        self.min_identity = min_identity
        self.block_size = block_size
        self.config_file = config_file
        self.cpu = cpu
        self.memory = memory
    
    def run(self):
        cmd = (
            f"{DIAMOND_PATH} "
            f"{self.method} "
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

def main():
    query_fa = "/mnt/sdb/issas/Example_Projects2/02.workspace/06.profile/uniqGeneSet.faa"
    database_name = "Scyc"
    tmp_out = "./test/"
    out = "./aaa.tsv"
    cpu = 128
    runner = DIAMOND(
        query_fa=query_fa,
        database_name=database_name,
        tmp_out=tmp_out,
        out=out,
        cpu=cpu
    )

    runner.run()

if __name__ == '__main__':
    main()
