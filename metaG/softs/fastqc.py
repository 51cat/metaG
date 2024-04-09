import argparse
import subprocess
from metaG.core.log import add_log
import os
import metaG

FASTQC_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/FastQC/fastqc"

class Fastqc:
    def __init__(self,
                 r1 = None,
                 r2 = None,
                 out = None,
                 ) -> None:
        
        self.r1 = r1
        self.r2 = r2
        self.out = out

    def run(self):
        cmd = (
            f"{FASTQC_PATH} -o {self.out}  {self.r1} {self.r2}"
        )
        subprocess.check_call(cmd, shell=True)