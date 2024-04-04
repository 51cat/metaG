from metaG.predict.predict_gene import PREDICTer
from metaG.common.minana import MinAna
from metaG.utils import get_target_dir, get_fa_stat, merge_json_files, seqtools_run
import json
import os

class GenePredicter(MinAna):
    def __init__(
            self,
            contig_json= None,
            use = "prodigal",
            outdir= None ,
            config_file = None
            ) -> None:
        super().__init__(outdir=outdir)
        self.contig_json = contig_json
        self.outdir = outdir
        self.config_file = config_file
        self.use = use
        self.jsons = []
        self.gene_fas = []
        
    
    def mk_geneset(self, out_geneset):
        seqtools_run(f"{self.target_dir}/__GeneSet_all.fa", do = "merge", fa_lst=self.gene_fas)
        seqtools_run(f"{self.target_dir}/GeneSet_all.fa", do = "format", in_fa=f"{self.target_dir}/__GeneSet_all.fa")
        self.add_rubbish(f"{self.target_dir}/__GeneSet_all.fa")
        self.add_rubbish(f"{self.target_dir}/GeneSet_all.fa")

        with open(f"{self.target_dir}/GeneSet_all.fa") as fd_in:
            #with open(f"{self.target_dir}/GeneSet_all_clean.fa", "w") as fd_out:
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
        self.write_json(clean_contig_dict, f"{self.target_dir}/clean_gene.json")
        
        # write stat
        get_fa_stat(f"{self.target_dir}/predict_gene_stat.txt", self.gene_fas)
    
    def run_predict(self):
        self.mk_predict_gene()
        self.mk_geneset(f"{self.target_dir}/GeneSet_clean_all.fa")
        self.clean()