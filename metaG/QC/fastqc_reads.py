from metaG.common.minana import MinAna
from metaG.utils import get_software_path
from metaG.software.interface import SoftInterface as SIF


class Fastqcer(MinAna):
    def __init__(self, 
                 r1, 
                 r2, 
                 outdir):
            super().__init__(outdir=outdir, step_name="prep")
            self.r1 = r1
            self.r2 = r2
            self.outdir = outdir

            self._steps_dir = "01.prep/QC/Fastqc/"
            self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
            self.make_step_outdir(self._steps_dir)
            self.prep_start()
    
    def run(self):
        
        fastqc_infc = SIF(
            interpreter="python",
            work_dir=self.step_outdir,
            path=get_software_path("fastqc"),
            r1 = self.r1,
            r2 = self.r2,
            out = self.step_outdir
        )

        fastqc_infc.mk_cmd()
        fastqc_infc.run_by_py()

    
