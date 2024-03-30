from metaG.common.minana import MinAna
from metaG.utils import get_software_path, \
                        get_target_dir, \
                        rename_fa_to_target_name
from metaG.software.interface import SoftInterface as SIF
import os
import subprocess


class MEGAHITer(MinAna):
     def __init__(self, 
                 r1, 
                 r2, 
                 sample_name,
                 outdir,
                 min_contig_len = 500,
                 config_file = None):
            super().__init__(outdir=outdir, step_name="assembly")
            self.r1 = r1
            self.r2 = r2
            self.outdir = outdir
            self.sample_name = sample_name
            self.config_file = config_file
            self.min_contig_len = min_contig_len

            self._steps_dir = f"02.assembly/megahit_out/"
            self.step_outdir = f"{self.outdir}/{self._steps_dir}/"
            self.make_step_outdir(self._steps_dir)
            self.prep_start()
    
     def assembly_megahit(self):
        
        fastqc_infc = SIF(
            interpreter="python",
            work_dir=f"{self.step_outdir}/{self.sample_name}",
            path=get_software_path("megahit"),
            r1 = self.r1,
            r2 = self.r2,
            out = f"{self.step_outdir}/{self.sample_name}",
            config_file = None,
            min_contig_len = self.min_contig_len
        )

        fastqc_infc.mk_cmd()
        fastqc_infc.run_by_py()

        
        
        raw_contig = f"{self.step_outdir}/{self.sample_name}/final.contigs.fa"
        clean_contig = f"{self.parent_dir}/{self.sample_name}_clean.contigs.fa"
        rename_fa_to_target_name(
             raw_contig,
             self.sample_name,
             clean_contig
        )
        
        self.write_json({self.sample_name:os.path.abspath(clean_contig)}, 
                        f"{self.step_outdir}/{self.sample_name}_contigs_clean.json")
     
     def get_clean_json(self):
          return f"{self.step_outdir}/{self.sample_name}_contigs_clean.json"

     def run(self):
         self.assembly_megahit()