from metaG.common.minana import MinAna
from metaG.software.interface import SoftInterface as SIF
from metaG.utils import get_software_path
import glob
import os

class DupRemover(MinAna):
    def __init__(
            self, 
            in_fa, 
            outdir,
            word_size = 9,
            identity_threshold = 0.95,
            shorter_coverage = 0.9,
            config_file = None) -> None:
        super().__init__(outdir=outdir, step_name="predict")

        self.in_fa = in_fa
        self.outdir = outdir
        self.word_size = word_size
        self.identity_threshold = identity_threshold
        self.shorter_coverage = shorter_coverage
        self.config_file = None
        self.out_fa = f"{self.outdir}/GeneSet_clean_unique.fa"
    
    def drop_dupseq(self):
        cd_hit_infc = SIF(
            interpreter="python",
            work_dir=f"{self.outdir}",
            path=get_software_path("cd_hit"),
            
            in_fa = self.in_fa,
            out_fa = self.out_fa,
            identity_threshold = self.identity_threshold,
            word_size = self.word_size,
            shorter_coverage = self.shorter_coverage,
            config_file = self.config_file,
        )

        cd_hit_infc.mk_cmd()
        cd_hit_infc.run_by_py()
    
    def index_unqiue_geneset(self):
        bwa_infc = SIF(
            interpreter="python",
            work_dir=self.outdir,
            path=get_software_path("bwa"),
            host = "GeneSet_clean_unique", 
            fa = self.out_fa,
            mode = "index"
        )
        bwa_infc.mk_cmd()
        bwa_infc.run_by_py()

        index_files = glob.glob(f"GeneSet_clean_unique*[fa,amd,ann,bwt,pac,sa]")
        mv_to_outdir = [f"mv {os.path.abspath(file)} {self.outdir}"
                        for file in index_files]
        self.run_cmds(mv_to_outdir)
    
    @property
    def clean_geneset(self):
        return f"{self.outdir}/GeneSet_clean_unique.fa"
    
    def run(self):
        self.drop_dupseq()
        self.index_unqiue_geneset()