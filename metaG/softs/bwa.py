import subprocess
from metaG.core.log import add_log
import os
import glob
import metaG

BWA_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/bwa/bwa"

class BWA:
    def __init__(self,
                 host = None, 
                 fa = None, 
                 genome_dir = None,
                 mode = None, 
                 r1 = None, 
                 r2 = None,
                 cpu = None,
                 memory = None
                 ) -> None:
        
        self.host = host
        self.fa = fa
        self.genome_dir = genome_dir
        self.r1 = r1
        self.r2 = r2
        self.mode = mode
        self.cpu = cpu
        self.memory = memory
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