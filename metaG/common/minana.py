
import subprocess
from abc import abstractmethod
import os

class MinAna:
    def __init__(self, outdir, *args, **kwargs) -> None:
        self.outdir = outdir


        for k, v in kwargs.items():
            setattr(self, k, v)
        
        if not os.path.exists(self.outdir):
           subprocess.check_call(f'mkdir -p {self.outdir}', shell = True)

    def make_step_outdir(self, dirname):
        subprocess.check_call(f"mkdir -p {self.outdir}/{dirname}", shell = True)
    
    def run_cmd(self, cmd):
        subprocess.check_call(cmd, shell= True)

    def run_cmds(self, cmd_lst):
        for cmd in cmd_lst:
            subprocess.check_call(cmd, shell=True)

    @abstractmethod
    def run(self):
        pass