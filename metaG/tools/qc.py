import pysam
import json
from metaG.core.log import add_log
from metaG.core.minana import MinAna
from metaG.softs.trimmomatic import Trimmomatic

@add_log
def guss_phred(fq, guss_max = 10000):
    ascii_sets = set()
    n = 0
    lower_58 = 0 
    upper_75 = 0

    for r in pysam.FastxFile(fq):
        n += 1
        ascii_sets.update(set(r.get_quality_array()))
        if n == guss_max:
            break

    for ascii in ascii_sets:
        if ascii <= 58:
            lower_58 += 1
        elif ascii >= 75:
            upper_75 += 1

    guss_phred.logger.info(f"use reads: {guss_max}")
    guss_phred.logger.info(f"lower_58: {lower_58}")
    guss_phred.logger.info(f"upper_75: {upper_75}")
    
    if (lower_58 >= 1) and upper_75 == 0:
        return "phred33"
    
    if (lower_58 == 0) and upper_75 >= 1:
        return "phred64"

class QCer(MinAna):
    def __init__(self, 
                 r1, 
                 r2, 
                 sample_name, 
                 outdir,
                 config_file = None):
            super().__init__(outdir=outdir)
            self.r1 = r1
            self.r2 = r2
            self.sample_name = sample_name
            self.outdir = outdir
            self.config_file = config_file
            self.phred = guss_phred(self.r1)

            self.qc_use = "trimmomatic"
            self.qc_soft = {
                "trimmomatic":self.qc_trimmomatic
            }

    def set_qc_use(self, use):
        self.host_qc_use = use

    def qc_trimmomatic(self):
        
        runner = Trimmomatic(
            r1 = self.r1,
            r2 = self.r2,
            sample_name=self.sample_name,
            phred=self.phred,
            config_file=self.config_file,
            cpu = self.cpu,
            memory=self.memory,
            out=self.outdir
        )
        runner.run()


    @property
    def clean_r1_r2_path(self):
        stat_file = f"{self.outdir}/{self.sample_name}_trimmomatic_stat.json"
        with open(stat_file, 'r') as f:
            data = json.load(f)
        return data[self.sample_name]['R1'], data[self.sample_name]['R2']

    def run(self):
        self.qc_soft[self.qc_use]()