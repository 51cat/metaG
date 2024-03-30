import os
import metaG
import subprocess
from metaG.common.minana import MinAna
import glob
from metaG.software.interface import SoftInterface as SIF
from metaG.utils import get_software_path
from metaG.common.log import add_log

class IndexHost(MinAna):
    
    def __init__(self, host, outdir, fa = None):
        super().__init__(outdir=outdir, step_name="prep")

        self._hostbase_path = f"{os.path.dirname(metaG.__file__)}/lib/host_database"
        self._supports = os.listdir(self._hostbase_path)
        
        self.host = host
        self.fa = fa

        self._steps_dir = "01.prep/ref_index/"
        self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
        self.make_step_outdir(self._steps_dir)
        self.prep_start()

    @add_log
    def index_host(self):
        if self.host in self._supports:
            self.index_host.logger.info(f"Successfully found {self.host} in {self._supports} ")

            index_files = glob.glob(f"{self._hostbase_path}/{self.host}/*")
            link_cmds = [f"ln -s {os.path.abspath(file)} {self.step_outdir}" 
                        for file in index_files]
            
            self.run_cmds(link_cmds)
        
        else:
            
            if self.fa is None:
                raise FileNotFoundError(f"Error path: GENOME fasta {self.fa}!")
            
            bwa_infc = SIF(
                interpreter="python",
                work_dir=self._steps_dir,
                path=get_software_path("bwa"),
                host = self.host, 
                fa = self.fa,
                mode = "index"
            )
            bwa_infc.mk_cmd()
            bwa_infc.run_by_py()
            
            # 写入数据库
            self.index_host.logger.info(f"Write {self.host} to {self._hostbase_path} ")
            new_host_path = f"{self._hostbase_path}/{self.host}/"
            subprocess.check_call(f"mkdir -p {new_host_path}", shell=True)
            index_files = glob.glob(f"{self.host}*[fa,amd,ann,bwt,pac,sa]")
            
            cp_to_database_cmds = [f"cp -a {os.path.abspath(file)} {new_host_path}"
                        for file in index_files]

            mv_to_outdir = [f"mv {os.path.abspath(file)} {self.step_outdir}"
                        for file in index_files]

            self.run_cmds(cp_to_database_cmds)
            self.run_cmds(mv_to_outdir)

    
    def get_index_dir(self):
        return self.step_outdir

    def run(self):
        self.index_host()
    

def main():
    runner = IndexHost("rice2", "./test/", fa = "/home/issas/dev/meta_genome/test/rice2.fasta")
    runner.run()
    runner.get_index_dir()

if __name__ == '__main__':
    main()