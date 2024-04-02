from metaG.QC.remove_adpater import TrimmomaticCutter
from metaG.QC.fastqc_reads import Fastqcer
from metaG.QC.remove_host import HostRemover
from metaG.common.minana import MinAna

from metaG.utils import get_target_dir

class QCfq(MinAna):
    def __init__(
            self,
            r1 = None,
            r2= None,
            outdir= None ,
            sample_name = None,
            host = None,
            config_file = None
            ) -> None:
        super().__init__(outdir=outdir)
        self.r1 = r1
        self.r2 = r2
        self.outdir = outdir
        self.sample_name = sample_name
        self.host = host
        self.config_file = config_file

    def run(self):
        
       trim_runner =  TrimmomaticCutter(
            r1 = self.r1, 
            r2 = self.r2,
            sample_name= self.sample_name,
            outdir=self.outdir,
            config_file=self.config_file
        )
       trim_runner.run()
       
       r1_paired, r2_paired = trim_runner.get_clean_r1_r2_path()

       hr_runner = HostRemover(
           r1 = r1_paired,
           r2 = r2_paired,
           host=self.host,
           genome_dir= get_target_dir(self.outdir, "prep", "ref_index"),
           sample_name= self.sample_name,
           outdir=self.outdir
       )
       hr_runner.run()
       r1_clean, r2_clean = hr_runner.get_clean_r1_r2_path()
       fasqc_runner =  Fastqcer(
            r1 = r1_clean, 
            r2 = r2_clean,
            outdir=self.outdir
        )
       fasqc_runner.run()