import argparse
import subprocess
import os
import metaG
from metaG.utils import parse_config_file
import multiprocessing

CD_HIT_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/cd-hit/cd-hit-est"

# 暂不开放config_file
ARGS_JSON = f"{os.path.dirname(metaG.__file__)}/lib/softs/cd-hit/args.json"
#/mnt/sdb/issas/bin/software/cd-hit/cd-hit-est -i all.sam.geneSet.fa -o uniqGeneSet.fa -n 9 -c 0.95 -G 0 -M 0 -d 0 -aS 0.9 -r 0 -T 88

class CD_HIT:
    def __init__(self,
                 in_fa,
                 out_fa,
                 word_size = 9,
                 identity_threshold = 0.95,
                 shorter_coverage = 0.9,
                 config_file = None
                 ) -> None:
        self.in_fa = in_fa
        self.out_fa = out_fa
        self.word_size = word_size
        self.identity_threshold = identity_threshold
        self.shorter_coverage = shorter_coverage
        self.threads = min(64, multiprocessing.cpu_count())

        self.config_file = None
    
    def run(self):
        cmd = (
            f"{CD_HIT_PATH} -i {self.in_fa} "
            f"-o {self.out_fa} "
            f"-n {self.word_size} "
            f"-c {self.identity_threshold} "
            f"-G 0 "
            f"-M 0 "
            f"-d 0 "
            f"-aS {self.shorter_coverage} "
            f"-r 0 "
            f"-T {self.threads} "

        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "PRODIGAL", args_json=ARGS_JSON,args_prfx="-")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)
        

def main():
    parser = argparse.ArgumentParser(description='Warpper for cd-hit-est')
    parser.add_argument('--in_fa', help='', required=True)
    parser.add_argument('--out_fa', help='', required=True)
    parser.add_argument('--word_size', help='', required=False, default=9)
    parser.add_argument('--identity_threshold', help='', required=False, default= 0.95)
    parser.add_argument('--shorter_coverage', help='', required=False, default= 0.9)
    parser.add_argument('--config_file', help='', required=False, default=None)
    
    args = parser.parse_args()

    runner = CD_HIT(
                 in_fa = args.in_fa,
                 out_fa = args.out_fa,
                 word_size = args.word_size,
                 identity_threshold = args.identity_threshold,
                 shorter_coverage = args.shorter_coverage
    )

    runner.run()
    
if __name__ == '__main__':
    main()