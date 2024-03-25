from metaG.QC.remove_adpater import TrimmomaticCutter
from metaG.QC.fastqc_reads import Fastqcer
from metaG.common.minana import MinAna

class QCfq(MinAna):
    def __init__(
            self,
            r1 = None,
            r2= None,
            outdir= None ,
            sample_name = None
            ) -> None:
        super().__init__(outdir=outdir)
        self.r1 = r1
        self.r2 = r2
        self.outdir = outdir
        self.sample_name = sample_name

    def run(self):
        
       trim_runner =  TrimmomaticCutter(
            r1 = self.r1, 
            r2 = self.r2,
            sample_name= self.sample_name,
            outdir=self.outdir
        )
       trim_runner.run()
       
       r1_paired, r2_paired = trim_runner.get_clean_r1_r2_path()
       fasqc_runner =  Fastqcer(
            r1 = r1_paired, 
            r2 = r2_paired,
            outdir=self.outdir
        )
       fasqc_runner.run()