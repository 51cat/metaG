from metaG.tools.predict import Predicter
from metaG.tools.drop_redundancy import RedundancyRemover
from metaG.softs.bwa import BWA

from metaG.core.minana import MinAna
from metaG.tools.seqtools import SeqProcesser
from metaG.utils import merge_json_files
import glob
import json
import os

class GenomoPredict(MinAna):
    def __init__(
            self,
            contig_json= None,
            predict_use = "prodigal",
            outdir= None ,
            word_size = 9,
            identity_threshold = 0.95,
            shorter_coverage = 0.9,
            config_file = None,
            parallel = True
            ) -> None:
        super().__init__(outdir=outdir, step_name="predict")
        self.contig_json = contig_json
        self.outdir = outdir
        self.config_file = config_file
        self.predict_use = predict_use
        self.parallel = parallel

        self.word_size = word_size
        self.identity_threshold = identity_threshold
        self.shorter_coverage = shorter_coverage

        self._predict_dir = f"03.predict/{self.predict_use}_out/"
        self.predict_dir = f"{self.outdir}/{self._predict_dir}/"

        self.make_step_outdir(self._predict_dir)
        self.prep_start()

        self.geneset_all = f"{self.parent_dir}/GeneSet_all.fa"
        self.geneset_unique = f"{self.parent_dir}/GeneSet_unique.fa"

        self.jsons = []
        self.gene_fas = []
        self.predict_tasks_lst = []
        self.remove_redu_tasks_lst = []


    def mk_geneset(self):
        sp = SeqProcesser()
        sp.set_out_fa(f"{self.parent_dir}/GeneSet_all.fa.1")
        sp.merge(self.gene_fas)

        # format
        sp.set_in_fa(f"{self.parent_dir}/GeneSet_all.fa.1")
        sp.set_out_fa(f"{self.parent_dir}/GeneSet_all.fa.2")
        sp.format()

        self.add_rubbish(f"{self.parent_dir}/GeneSet_all.fa.1")
        self.add_rubbish(f"{self.parent_dir}/GeneSet_all.fa.2")

        with open(f"{self.parent_dir}/GeneSet_all.fa.2") as fd_in:
            with open(f"{self.geneset_all}", "w") as fd_out:
                for line in fd_in.readlines():
                    if line.startswith(">"):
                        line = line.split("#")[0].replace(" ", "")
                        fd_out.write(f"{line}\n")
                    else:
                        fd_out.write(line)     

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
            self.gene_fas.append(runner.faa)
        
    def make_predict_stat(self):
        clean_contig_dict  = merge_json_files(self.jsons)
        self.write_json(clean_contig_dict, f"{self.parent_dir}/predict_gene.json")
        self.write_json(
            {"GeneSet_unique":os.path.abspath(self.geneset_unique)},
            f"{self.parent_dir}/GeneSet.json"
        )
        SeqProcesser.stat(f"{self.parent_dir}/predict_gene_stat.txt", self.gene_fas)
    
    def make_remove_redu_task(self):
        runner = RedundancyRemover(
            input_fa=self.geneset_all,
            output_fa=self.geneset_unique,
            word_size=self.word_size,
            shorter_coverage=self.shorter_coverage,
            identity_threshold=self.identity_threshold,
            config_file=self.config_file,
            outdir=self.parent_dir
        )
        self.remove_redu_tasks_lst.append(runner)
        self.gene_fas.append(self.geneset_all)
        self.gene_fas.append(self.geneset_unique)

    def index_uniqu_gene(self):
        runner = BWA(
            host = "GeneSet_unique",
            fa = self.geneset_unique,
            mode="index"
        )
        runner.run()
        index_files = glob.glob(f"GeneSet_unique*[fa,amd,ann,bwt,pac,sa]")
        self.run_cmds([f"mv {os.path.abspath(file)} {self.parent_dir}"
                        for file in index_files])

    def start(self):
        self.make_predict_tasks()
        self.run_tasks(self.predict_tasks_lst, self.parallel)
        self.mk_geneset()
        self.make_remove_redu_task()
        self.run_tasks(self.remove_redu_tasks_lst, parallel=False)
        self.index_uniqu_gene()
        self.make_predict_stat()
        self.clean()



def main():
    r = GenomoPredict(
        contig_json="/home/issas/dev/meta_genome/test/test_final/out/02.assembly/clean_contig.json",
        outdir = "./test/"
    )
    r.start()

if __name__ == '__main__':
    main()