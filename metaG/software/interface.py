import subprocess
import os
from metaG.common.log import add_log


class SoftInterface:
    
    def __init__(
            self, 
            interpreter:    str,
            work_dir:       str,
            path:           str = None,
            use:            str = "--" ,
            **kwargs
            ) -> None:
        
        self.interpreter = interpreter
        
        if path is None:
            self.path = ""
        else:
            self.path = path

        self.work_dir = work_dir

        self.args_dict = {}
        self.use = use

        self.cmd_basic = " ".join([self.interpreter, self.path])

        for k, v in kwargs.items():
            self.args_dict.update({k:v})

    def mk_cmd(self):
        for arg, val in self.args_dict.items():
            if self.use != "":
                self.cmd_basic += f" {self.use}{arg} {val}"
            else:
                self.cmd_basic += f" {val}"
        self.cmd = self.cmd_basic
    
    def get_cmd(self):
        return self.cmd

    @add_log
    def run_by_py(self):
        self.run_by_py.logger.info(f"cmd: {self.get_cmd()}")
        subprocess.check_call(self.cmd, shell= True)
    
    @add_log
    def out_shell_file(self):
        if not os.path.exists(self.work_dir):
            subprocess.check_call(f'mkdir -p {self.work_dir}', shell=True)
          
        shell_file = f"{self.work_dir}/{self.path.split('/')[-1].replace('.', '_')}.run.sh"
        self.out_shell_file.logger.info(f"File Name: {shell_file}")
        with open(shell_file, "w") as fd:
            fd.write(self.cmd)