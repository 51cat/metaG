import subprocess
from metaG.core.log import add_log
import os
import glob
import metaG
from dataclasses import dataclass
BWA_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/bwa/bwa"

@dataclass
class BWA:
    host: str = None
    fa: str = None
    genome_dir: str = None
    mode: str = None
    r1: str = None
    r2: str = None
    cpu: int = None
    memory: int = None

    def __post_init__(self):
        self.mem_out_bam = None

    def set_mem_out_bam(self, mem_out_bam):
        self.mem_out_bam =mem_out_bam

    @add_log
    def index(self):
        self.index.logger.info(f"Start Index: fa: {self.host}.fa")
        cmd1 = f"cp -a {self.fa} ./{self.host}.fa"
        cmd2 = f"{BWA_PATH} index ./{self.host}.fa"
        subprocess.check_call(cmd1, shell=True)
        subprocess.check_call(cmd2, shell=True)

    @add_log
    def mem(self):
        
        try:
            genome_fa = glob.glob(f"{self.genome_dir}/{self.host}.fasta")[0]
        except IndexError:
            genome_fa = glob.glob(f"{self.genome_dir}/{self.host}.fa")[0]
        print(f"{genome_fa}")
        cmd = (
            f"{BWA_PATH} mem -t {self.cpu} -M {genome_fa} {self.r1} {self.r2} | "
            f"samtools view -@{self.cpu} -b > {self.mem_out_bam}"
        )
        subprocess.check_call(cmd, shell=True)
    
    def run(self):
        if self.mode == "index":
            self.index()
        if self.mode == "map":
            self.mem()