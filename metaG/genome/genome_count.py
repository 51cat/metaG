from metaG.tools.count import GeneCounter
from metaG.tools.gene_count_transfer import GeneAnn, GeneTransfer
from metaG.core.minana import MinAna
from metaG.core.log import add_log
from metaG.utils import merge_json_files
import json
import os

class GenomoCount(MinAna):
    def __init__(self,
                 fq_json,
                 genome_fa,
                 ann_dir,
                 outdir,
                 parallel = True) -> None:
        super().__init__(outdir,step_name="count")
        self.fq_json = fq_json
        self.genome_fa = genome_fa
        self.ann_dir = ann_dir
        self.parallel = parallel

        self._count_dir = f"05.count/count_out/"
        self.count_dir = f"{self.outdir}/{self._count_dir}/"

        self.make_step_outdir(self._count_dir)
        self.prep_start()
        
        self.gene_info_all = f"{self.ann_dir}/gene_info.json"
        self.gene_length_all = f"{self.ann_dir}/gene_length.json"

        self.map_tasks = []
        self.sample_count_jsons = []
        self.raw_count_json = f"{self.parent_dir}/raw_count.json"

    def make_map_tasks(self):
        with open(self.fq_json, 'r', encoding='utf-8') as fd:
            fq_path_dict = json.load(fd)
        
        for sample_name in fq_path_dict.keys():
            runner = GeneCounter(
                r1 = fq_path_dict[sample_name]["R1"],
                r2 = fq_path_dict[sample_name]["R2"],
                sample_name=sample_name,
                outdir=self.count_dir,
                genome_fa=self.genome_fa
            )
            self.sample_count_jsons.append(runner.raw_reads_json)
            self.map_tasks.append(runner)
    
    
    def load_json(self, file):
        with open(file) as fd:
            return json.load(fd)


    def make_count_json(self):
        self.raw_count_dict = merge_json_files(self.sample_count_jsons)
        self.write_json(self.raw_count_dict, self.raw_count_json)

    @add_log
    def make_final_count(self):
        with open(self.gene_info_all) as fd:
            gene_info_all_dict = json.load(fd)
        with open(self.gene_length_all) as fd:
            gene_length_all_dict = json.load(fd)
        
        for database_name in gene_info_all_dict.keys():
            res_out = f"{self.parent_dir}/{database_name}"
            os.system(f"mkdir -p {res_out}")
            length_dict = self.load_json(gene_length_all_dict[database_name])
            info_dict = self.load_json(gene_info_all_dict[database_name])
            
            gann = GeneAnn(self.raw_count_dict, info_dict)
            gann.ann()
            ann_raw_count_dict = gann.ann_count_dict
            # transf
            gfs = GeneTransfer(ann_raw_count_dict, length_dict)
            gfs.to_fpkm()
            gfs.to_cpm()
            gfs.to_tpm()
            gfs.save("df", f"{res_out}/fpkm.tsv", gfs.fpkm)
            gfs.save("df", f"{res_out}/cpm.tsv", gfs.cpm)
            gfs.save("df", f"{res_out}/tpm.tsv", gfs.tpm)
            gfs.save("df", f"{res_out}/reads.tsv", gfs.count_dict)
            self.make_final_count.logger.info(f"finish {database_name}")


    def start(self):
        self.make_map_tasks()
        self.run_tasks(self.map_tasks, self.parallel)
        self.make_count_json()
        self.make_final_count()

def main():
    runner = GenomoCount(
        fq_json="/home/issas/dev/meta_genome/test/test_final/out/01.prep/clean_data.json",
        genome_fa="/home/issas/dev/metaG/test/test_final/out/03.predict/GeneSet_unique.fa",
        outdir="./test/",
        ann_dir = "/home/issas/dev/metaG/test/test_final/out/04.annotation/"
    )
    runner.start()

if __name__ == '__main__':
    main()
