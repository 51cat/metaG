from metaG.core.minana import MinAna
from metaG.tools.annotation import Annoater
from dataclasses import dataclass

@dataclass
class GenomeAnnotation(MinAna):
    uniq_fa_protein: str = None,
    uniq_fa: str   =None,
    outdir: str = None ,
    database_use: str =None, # name1:name2:name3...
    config_file: str  = None,
    annota_use: str  = "diamond",
    method: str  = "blastp",
    min_evalue: float =0.00001,
    min_identity: int = 80,
    format: int = 6,
    max_target_seqs: int = 10,
    block_size: int = 8,
    parallel: bool = True
    
    def __post_init__(self):
        super().__init__(outdir=self.outdir, step_name="annotation")
        self.database_use = self.database_use.split(":")
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
                    diamond_method=self.method,
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

