from metaG.core.minana import MinAna
from metaG.tools.seqtools import SeqProcesser
import json
import psutil
from metaG.tools.assembly import Assemblyer

AVA_PCT = 0.95
MEGHIT_TOTAL_AVA = psutil.virtual_memory().available*AVA_PCT
MEGHIT_RAM = 12884901888

class GenomeAssembly(MinAna):
    def __init__(
            self,
            fq_json= None,
            outdir= None ,
            min_contig_len=500,
            config_file = None,
            assembly_use = "MEGAHIT",
            parallel = True
            ) -> None:
        super().__init__(outdir=outdir, step_name="assembly")
        self.fq_json = fq_json
        self.outdir = outdir
        self.config_file = config_file
        self.min_contig_len = min_contig_len
        self.assembly_use = assembly_use
        self.parallel =parallel

        self._assembly_dir = f"02.assembly/{self.assembly_use}_out/"
        self.assembly_dir = f"{self.outdir}/{self._assembly_dir}/"

        self.make_step_outdir(self._assembly_dir)
        self.prep_start()

        self.clean_contig_dict = {}
        self.assembly_tasks_lst = []

        self.clean_contig_json = f"{self.parent_dir}/clean_contig.json"
        self.contig_stat_file = f"{self.parent_dir}/assembly_fa_stat.txt"
        self.count_dir = f"{self.assembly_dir}/contig_count/"


    def make_assembly_tasks(self):
        with open(self.fq_json, 'r', encoding='utf-8') as fd:
            fq_path_dict = json.load(fd)
            for sample_name in fq_path_dict.keys():
                r1 = fq_path_dict[sample_name]["R1"]
                r2 = fq_path_dict[sample_name]["R2"]
                runner = Assemblyer(
                    r1=r1,
                    r2=r2, 
                    sample_name=sample_name,
                    outdir=self.assembly_dir,
                    min_contig_len=self.min_contig_len
                )
                runner.set_assembly_use(self.assembly_use)
                self.clean_contig_dict.update({sample_name:runner.clean_contig})
                self.assembly_tasks_lst.append(runner)
    
    def make_assembly_stat(self):
        self.write_json(self.clean_contig_dict, self.clean_contig_json)
        SeqProcesser.stat(self.contig_stat_file, list(self.clean_contig_dict.values()))
        self.run_cmd(f"mv {self.count_dir} {self.parent_dir}")

    def start(self):
        self.make_assembly_tasks()
        self.run_tasks(self.assembly_tasks_lst, self.parallel, n = max(int(MEGHIT_TOTAL_AVA/MEGHIT_RAM), 1))
        self.make_assembly_stat()

def main():
    runner = GenomeAssembly(
        "/home/issas/dev/meta_genome/test/test_final/out/01.prep/clean_data.json",
        outdir="./test/"
    )
    runner.start()

if __name__ == '__main__':
    main()

