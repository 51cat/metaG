import argparse
import subprocess
from metaG.common.log import add_log
import os
import glob
import metaG

BWA_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/bwa/bwa"

class bwa:
    def __init__(self,
                 host = None, 
                 fa = None, 
                 genome_dir = None, 
                 r1 = None, 
                 r2 = None,
                 out = None,
                 threads = 40
                 ) -> None:
        
        self.host = host
        self.fa = fa
        self.genome_dir = genome_dir
        self.r1 = r1
        self.r2 = r2
        self.out = out
        self.threads = threads
    
    def pre_check(self):
        pass
    
    @add_log
    def index(self):
        self.index.logger.info(f"Start Index: fa: {self.host}.fa")
        cmd1 = f"cp -a {self.fa} ./{self.host}.fa"
        cmd2 = f"{BWA_PATH} index ./{self.host}.fa"
        subprocess.check_call(cmd1, shell=True)
        subprocess.check_call(cmd2, shell=True)

    def mem(self, out_file_name):
        genome_fa = glob.glob(f"{self.genome_dir}/{self.host}.fasta")[0]
        cmd = (
            f"{BWA_PATH} mem -t 40 -M {genome_fa} {self.r1} {self.r2} | "
            f"samtools view -@{self.threads} -b > {out_file_name}"
        )
        subprocess.check_call(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser(description='Warpper for bwa')
    parser.add_argument('--host', help='', required=True)
    parser.add_argument('--fa', help='', required=True)
    parser.add_argument('--mode', help='', default=None, required=True)
    parser.add_argument('--genome_dir', help='', required=False)
    parser.add_argument('--r1', help='')
    parser.add_argument('--r2', help='')
    parser.add_argument('--out', help='')
    parser.add_argument('--mem_out_file_name', help='')
    parser.add_argument('--threads', help='', type=int, default=16)
    
    args = parser.parse_args()

    runner = bwa(
        args.host,
        args.fa,
        args.genome_dir,
        args.r1,
        args.r2,
        args.out,
        args.threads
    )

    runner.pre_check()
    
    if args.mode == "index":
        runner.index()
    
    if args.mode == "mem":
        runner.mem(out_file_name=args.mem_out_file_name)

if __name__ == '__main__':
    main()