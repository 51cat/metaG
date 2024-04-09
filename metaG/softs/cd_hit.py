import argparse
import subprocess
import os
import metaG
from metaG.utils import parse_config_file
import multiprocessing

CD_HIT_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/cd-hit/cd-hit-est"
ARGS_JSON = f"{os.path.dirname(metaG.__file__)}/lib/softs/cd-hit/args.json"

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