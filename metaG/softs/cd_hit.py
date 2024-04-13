import subprocess
import os
import metaG
from metaG.utils import parse_config_file
from dataclasses import dataclass

CD_HIT_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/cd-hit/cd-hit-est"
ARGS_JSON = f"{os.path.dirname(metaG.__file__)}/lib/softs/cd-hit/args.json"

@dataclass
class CD_HIT:
    in_fa: str
    out_fa: str
    word_size: int = 9,
    identity_threshold: float = 0.95,
    shorter_coverage: float = 0.9,
    config_file: str = None,
    cpu: int = None
    memeory: int = None
    
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
            f"-T {self.cpu} "

        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "CD_HIT", args_json=ARGS_JSON,args_prfx="-")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)