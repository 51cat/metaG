import subprocess
from metaG.core.log import add_log
import os
import metaG
from dataclasses import dataclass

FASTQC_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/FastQC/fastqc"

@dataclass
class Fastqc:
    r1 :str = None
    r2 :str = None
    out: str = None
    cpu: int = metaG.get_default_cpus()
        
    def set_cpu(self, ncpu):
        self.cpu  = ncpu

    @add_log
    def run(self):
        cmd = (
            f"{FASTQC_PATH} -q -t {self.cpu} -o {self.out}  {self.r1} {self.r2}"
        )
        subprocess.check_call(cmd, shell=True)