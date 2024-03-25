from metaG.common.minana import MinAna
from metaG.utils import get_software_path
from metaG.software.interface import SoftInterface as SIF


class Fastqcer(MinAna):
    def __init__(self, 
                 r1, 
                 r2, 
                 outdir):
            super().__init__(outdir=outdir)
            self.r1 = r1
            self.r2 = r2
            self.outdir = outdir

            self._steps_dir = "01.prep/QC/Fastqc/"
    
    def run(self):
        self.make_step_outdir(self._steps_dir)

        fastqc_infc = SIF(
            interpreter="python",
            work_dir=f"{self.outdir}/{self._steps_dir}/",
            path=get_software_path("fastqc"),
            r1 = self.r1,
            r2 = self.r2,
            out = f"{self.outdir}/{self._steps_dir}/"
        )

        fastqc_infc.mk_cmd()
        fastqc_infc.run_by_py()

    
