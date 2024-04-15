import subprocess
from metaG.core.log import add_log
import os
import metaG
from dataclasses import dataclass

FASTQC_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/FastQC/fastqc"

@dataclass
class Fastqc:
    reads_list :list = None
    out: str = None

    def __post_init__(self):
        self.reads_input = " ".join(self.reads_list)
        self.threads = min(metaG.get_default_cpus(),len(self.reads_list))

    @add_log
    def run(self):
        self.run.logger.info(f"threads: {self.threads}")
        cmd = (
            f"{FASTQC_PATH} -q -t {self.threads} -o {self.out}  {self.reads_input}"
        )
        subprocess.check_call(cmd, shell=True)