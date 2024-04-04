
import subprocess
from abc import abstractmethod
import os
import json
from metaG.utils import get_target_dir

class MinAna:
    def __init__(self, outdir, step_name = None, *args, **kwargs) -> None:
        self.outdir = outdir
        self.step_name = step_name
        self._rubbish = []

        for k, v in kwargs.items():
            setattr(self, k, v)
        
        if not os.path.exists(self.outdir):
           subprocess.check_call(f'mkdir -p {self.outdir}', shell = True)

    def prep_start(self):
        if self.step_name is not None:
            self.parent_dir = get_target_dir(self.outdir, self.step_name)
            
        else:
            self.parent_dir = None

    def add_rubbish(self, *args):
        for f in args:
            self._rubbish.append(f) 

    def make_step_outdir(self, dirname):
        subprocess.check_call(f"mkdir -p {self.outdir}/{dirname}", shell = True)
    
    def run_cmd(self, cmd):
        subprocess.check_call(cmd, shell= True)

    def run_cmds(self, cmd_lst):
        for cmd in cmd_lst:
            subprocess.check_call(cmd, shell=True)
    
    def write_json(self, dict, out):
        json_str = json.dumps(dict, indent=4)
        with open(out,"w") as fd:
            fd.write(json_str)
    
    def clean(self):
        if len(self._rubbish) == 0:
            return
        else:
            cmds = [f"rm -rf {f}" for f in self._rubbish]
            self.run_cmds(cmds)


    @abstractmethod
    def run(self):
        pass