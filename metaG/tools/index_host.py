import os
import glob
import metaG
import subprocess

from metaG.core.minana import MinAna
from metaG.core.log import add_log
from metaG.softs.bwa import BWA

class IndexHost(MinAna):
    
    def __init__(self, 
                 host, 
                 outdir, 
                 fa = None):
        super().__init__(outdir=outdir)

        self._hostbase_path = f"{os.path.dirname(metaG.__file__)}/lib/host_database"
        self._supports = os.listdir(self._hostbase_path)
        
        self.host = host
        self.fa = fa
        self.index_use = "bwa"
        
        self.index_soft = {
            "bwa":self.index_host_BWA
        }

    def set_index_use(self, use):
        self.index_use = use

    @add_log
    def index_host_BWA(self):
        if self.host in self._supports:
            self.index_host_BWA.logger.info(f"Successfully found {self.host} in {self._supports} ")

            index_files = glob.glob(f"{self._hostbase_path}/{self.host}/*")
            link_cmds = [f"ln -s {os.path.abspath(file)} {self.outdir}" 
                        for file in index_files]
            
            self.run_cmds(link_cmds)
        
        else:
            
            if self.fa is None:
                raise FileNotFoundError(f"Error path: GENOME fasta {self.fa}!")
            
            runner = BWA(
                host=self.host,
                fa=self.fa,
                mode = "index"
            )
            runner.run()
            # 写入数据库
            self.index_host.logger.info(f"Write {self.host} to {self._hostbase_path} ")
            
            new_host_path = f"{self._hostbase_path}/{self.host}/"
            subprocess.check_call(f"mkdir -p {new_host_path}", shell=True)
            index_files = glob.glob(f"{self.host}*[fa,amd,ann,bwt,pac,sa]")
            
            cp_to_database_cmds = [f"cp -a {os.path.abspath(file)} {new_host_path}"
                        for file in index_files]

            mv_to_outdir = [f"mv {os.path.abspath(file)} {self.outdir}"
                        for file in index_files]

            self.run_cmds(cp_to_database_cmds)
            self.run_cmds(mv_to_outdir)

    @property
    def index_dir(self):
        return self.outdir

    def run(self):
        self.index_soft[self.index_use]()