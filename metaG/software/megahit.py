import argparse
import subprocess
from metaG.common.log import add_log
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
                 min_contig_len = 500
                 ) -> None:
        
        self.r1 = r1
        self.r2 = r2
        self.out = out
        self.min_contig_len = min_contig_len
        self.config_file = config_file
    
    def run(self):
        cmd = (
            f"{MEGAHIT_PATH} -1 {self.r1} -2 {self.r2} -o {self.out} --min-contig-len {self.min_contig_len} "
        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "MEGAHIT")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)
        

def main():
    parser = argparse.ArgumentParser(description='Warpper for fastqc')
    parser.add_argument('--r1', help='', required=True)
    parser.add_argument('--r2', help='', required=True)
    parser.add_argument('--out', help='', required=True)
    parser.add_argument('--config_file', help='', required=False, default= None)
    parser.add_argument('--min_contig_len', help='', required=False, default= 500)
    
    args = parser.parse_args()

    runner = MEGAHIT(
            r1 = args.r1,
            r2 = args.r2,
            out = args.out,
            config_file = args.config_file,
            min_contig_len=args.min_contig_len
    )

    runner.run()
    
if __name__ == '__main__':
    main()