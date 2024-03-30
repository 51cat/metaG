import pysam
import json
from metaG.common.log import add_log
from metaG.common.minana import MinAna
from metaG.utils import get_software_path
from metaG.software.interface import SoftInterface as SIF

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

class TrimmomaticCutter(MinAna):
    def __init__(self, 
                 r1, 
                 r2, 
                 sample_name, 
                 outdir,
                 config_file = None):
            super().__init__(outdir=outdir, step_name="prep")
            self.r1 = r1
            self.r2 = r2
            self.sample_name = sample_name
            self.outdir = outdir
            self.config_file = config_file
            self.phred = guss_phred(self.r1)

            self._steps_dir = "01.prep/QC/TrimmomaticCut/"
            self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
            self.make_step_outdir(self._steps_dir)
            self.prep_start()
    
    def remove_adpater(self):
        
        trimmomatic_infc = SIF(
            interpreter="python",
            work_dir=self.step_outdir,
            path=get_software_path("trimmomatic"),
            r1 = self.r1,
            r2 = self.r2,
            out = self.step_outdir,
            sample = self.sample_name,
            config_file = self.config_file
        )

        trimmomatic_infc.mk_cmd()
        trimmomatic_infc.run_by_py()
    
    def get_clean_r1_r2_path(self):
        stat_file = f"{self.step_outdir}/{self.sample_name}_trimmomatic_stat.json"
        with open(stat_file, 'r') as f:
            data = json.load(f)
        return data[self.sample_name]['R1'], data[self.sample_name]['R2']


    def run(self):
        self.remove_adpater()
    
