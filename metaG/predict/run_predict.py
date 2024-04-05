from metaG.predict.predict_gene import PREDICTer
from metaG.predict.remove_dup import DupRemover
from metaG.common.minana import MinAna
from metaG.common.seqtools import SeqProcesser
from metaG.utils import get_target_dir, merge_json_files
import json
import os

class GenePredicter(MinAna):
    def __init__(
            self,
            contig_json= None,
            use = "prodigal",
            outdir= None ,
            config_file = None,
            word_size = 9,
            identity_threshold = 0.95,
            shorter_coverage = 0.9
            ) -> None:
        super().__init__(outdir=outdir)
        self.contig_json = contig_json
        self.outdir = outdir
        self.config_file = config_file
        self.use = use
        self.word_size = word_size
        self.identity_threshold = identity_threshold
        self.shorter_coverage = shorter_coverage
        self.jsons = []
        self.gene_fas = []
        self.target_dir = None
        
    
    def mk_geneset(self, out_geneset):
        sp = SeqProcesser()
        sp.set_out_fa(f"{self.target_dir}/__GeneSet_all.fa")
        sp.merge(self.gene_fas)

        # format
        sp.set_in_fa(f"{self.target_dir}/__GeneSet_all.fa")
        sp.set_out_fa(f"{self.target_dir}/GeneSet_all.fa")
        sp.format()

        self.add_rubbish(f"{self.target_dir}/__GeneSet_all.fa")
        self.add_rubbish(f"{self.target_dir}/GeneSet_all.fa")

        with open(f"{self.target_dir}/GeneSet_all.fa") as fd_in:
            with open(f"{out_geneset}", "w") as fd_out:
                for line in fd_in.readlines():
                    if line.startswith(">"):
                        line = line.split("#")[0].replace(" ", "")
                        fd_out.write(f"{line}\n")
                    else:
                        fd_out.write(line)
                

    
    def mk_predict_gene(self):
        with open(self.contig_json, 'r', encoding='utf-8') as fd:
            contig_path_dict = json.load(fd)
        
        for sample_name, contig_path in contig_path_dict.items():
            
            runner = PREDICTer(
                contig_file=contig_path, 
                sample_name=sample_name, 
                outdir=self.outdir,
                use = self.use,
                config_file=self.config_file
            )
            runner.run()
            self.jsons.append(runner.predict_json)
            self.gene_fas.append(runner.ffn)
        
        clean_contig_dict  = merge_json_files(self.jsons)
        self.target_dir = get_target_dir(self.outdir, "predict")
        self.write_json(clean_contig_dict, f"{self.target_dir}/predict_gene.json")
    
    def mk_unique_geneset(self):
        runner = DupRemover(
            in_fa=f"{self.target_dir}/GeneSet_clean_all.fa" ,
            outdir=self.target_dir,
            word_size=self.word_size,
            identity_threshold=self.identity_threshold,
            shorter_coverage=self.shorter_coverage

        )
        runner.run()
        self.geneset_dict = {"GeneSet_unique":os.path.abspath(runner.clean_geneset), 
                             "GeneSet_all":os.path.abspath(f"{self.target_dir}/GeneSet_clean_all.fa")}
        self.gene_fas.append(runner.clean_geneset)

    def write_clean_geneset_json(self):
        self.write_json(self.geneset_dict , f"{self.target_dir}/GeneSet.json")

    def run_predict(self):
        self.mk_predict_gene()
        self.mk_geneset(f"{self.target_dir}/GeneSet_clean_all.fa")
        self.mk_unique_geneset()
        
        # write stat
        self.gene_fas.append(f"{self.target_dir}/GeneSet_clean_all.fa")
        SeqProcesser.stat(f"{self.target_dir}/predict_stat.txt", self.gene_fas)
        self.write_clean_geneset_json()
        self.clean()