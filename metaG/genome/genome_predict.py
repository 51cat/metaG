from metaG.tools.predict import Predicter

from metaG.core.minana import MinAna
from metaG.tools.seqtools import SeqProcesser
from metaG.utils import merge_json_files
import json
import os

class GenomoPredict(MinAna):
    def __init__(
            self,
            contig_json= None,
            predict_use = "prodigal",
            outdir= None ,
            config_file = None,
            #word_size = 9,
            #identity_threshold = 0.95,
            #shorter_coverage = 0.9
            ) -> None:
        super().__init__(outdir=outdir, step_name="predict")
        self.contig_json = contig_json
        self.outdir = outdir
        self.config_file = config_file
        self.predict_use = predict_use

        #self.word_size = word_size
        #self.identity_threshold = identity_threshold
        #self.shorter_coverage = shorter_coverage
        


        self._predict_dir = f"03.predict/{self.predict_use}_out/"
        self.predict_dir = f"{self.outdir}/{self._predict_dir}/"

        self.make_step_outdir(self._predict_dir)
        self.prep_start()

        self.jsons = []
        self.gene_fas = []
        self.target_dir = None
        self.predict_tasks_lst = []
        

    def make_predict_tasks(self):
        with open(self.contig_json, 'r', encoding='utf-8') as fd:
            contig_path_dict = json.load(fd)
        
        for sample_name, contig_path in contig_path_dict.items():
            runner = Predicter(
                contig_file=contig_path, 
                sample_name=sample_name, 
                outdir=self.predict_dir,
                config_file=self.config_file
            )
            runner.set_predict_use(self.predict_use)
            self.predict_tasks_lst.append(runner)

            self.jsons.append(runner.predict_json)
            self.gene_fas.append(runner.ffn)
        
    def make_predict_stat(self):
        clean_contig_dict  = merge_json_files(self.jsons)
        self.write_json(clean_contig_dict, f"{self.parent_dir}/predict_gene.json")
        SeqProcesser.stat(f"{self.parent_dir}/predict_gene_stat.txt", self.gene_fas)
    
    def start(self):
        self.make_predict_tasks()
        self.run_tasks(self.predict_tasks_lst, True)
        self.make_predict_stat()


def main():
    r = GenomoPredict(
        contig_json="/home/issas/dev/meta_genome/test/test_final/out/02.assembly/clean_contig.json",
        outdir = "./test/"
    )
    r.start()

if __name__ == '__main__':
    main()