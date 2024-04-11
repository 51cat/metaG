from metaG.core.minana import MinAna
from metaG.tools.seqtools import SeqProcesser
from metaG.utils import get_target_dir, merge_json_files
import json

from metaG.tools.annotation import Annoater

class GenomeAnnotation(MinAna):
    def __init__(
            self,
            uniq_fa_protein= None,
            uniq_fa  =None,
            outdir= None ,
            database_use=None, # name1:name2:name3...
            config_file = None,
            annota_use = "diamond",
            method = "blastp",
            min_evalue =0.00001,
            min_identity = 80,
            format = 6,
            max_target_seqs = 10,
            block_size = 8,
            parallel = True
            ) -> None:
        super().__init__(outdir=outdir, step_name="annotation")
        self.uniq_fa_protein = uniq_fa_protein
        self.uniq_fa = uniq_fa
        self.outdir = outdir
        self.config_file = config_file
        self.database_use = database_use.split(":")
        self.annota_use = annota_use
        self.parallel =parallel
        self.method = method
        self.min_evalue = min_evalue
        self.min_identity = min_identity
        self.format = format
        self.max_target_seqs = max_target_seqs
        self.block_size = block_size

        self._annota_dir = f"04.annotation/{self.annota_use}_out/"
        self.annota_dir = f"{self.outdir}/{self._annota_dir}/"
        self.make_step_outdir(self._annota_dir)

        self.prep_start()

        self.gene_length_dict = {}
        self.gene_info_dict = {}
        self.final_annota_dict = {}
        self.annotation_tasks_lst = []

        self.final_gene_length_json = f"{self.parent_dir}/gene_length.json"
        self.final_gene_info_json = f"{self.parent_dir}/gene_info.json"
        self.final_annota_json = f"{self.parent_dir}/final_annotation.json"


    def make_annotation_tasks(self):
        for database_name in self.database_use:
                runner = Annoater(
                    query_fa=self.uniq_fa_protein,
                    uniq_gene_fa=self.uniq_fa,
                    database_name=database_name,
                    method=self.method,
                    min_evalue=self.min_evalue,
                    min_identity=self.min_identity,
                    format=self.format,
                    max_target_seqs=self.max_target_seqs,
                    block_size=self.block_size,
                    config_file=self.config_file,
                    outdir=f"{self.annota_dir}/{database_name}"
                )
                runner.set_annoate_use(self.annota_use)

                self.gene_length_dict.update({database_name:runner.gene_length})
                self.gene_info_dict.update({database_name:runner.gene_annoate})
                self.final_annota_dict.update({database_name:runner.anno_filter})

                self.annotation_tasks_lst.append(runner)
        
    def make_annota_stat(self):
         self.write_json(self.gene_length_dict, self.final_gene_length_json)
         self.write_json(self.gene_info_dict, self.final_gene_info_json)
         self.write_json(self.final_annota_dict, self.final_annota_json)


    def start(self):
        self.make_annotation_tasks()
        self.run_tasks(self.annotation_tasks_lst, self.parallel)
        self.make_annota_stat()

def main():
    runner = GenomeAnnotation(
        uniq_fa="/home/issas/dev/metaG/test/test_final/out/03.predict/GeneSet_unique.fa",
        outdir="./test/",
        database_use = "Ncyc:Pcyc:Scyc"
    )
    runner.start()

if __name__ == '__main__':
    main()

