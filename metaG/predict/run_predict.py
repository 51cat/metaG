from metaG.predict.predict_orf import PREDICTer
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
        self.orf_fas = []
    
    def run_pretict(self):
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
            self.orf_fas.append(runner.ffn)
            #self.orf_fas.append(runner.faa)
        
        clean_contig_dict  = merge_json_files(self.jsons)
        target_dir = get_target_dir(self.outdir, "predict")
        self.write_json(clean_contig_dict, f"{target_dir}/clean_gene.json")

        # merge
        seqtools_run(f"{target_dir}/__GeneSet_all.fa", do = "merge", fa_lst=self.orf_fas)
        seqtools_run(f"{target_dir}/GeneSet_all.fa", do = "format", in_fa=f"{target_dir}/__GeneSet_all.fa")
        os.system(f"rm -rf {target_dir}/__GeneSet_all.fa")
        
        # write stat
        get_fa_stat(f"{target_dir}/orf_fa_stat.txt", self.orf_fas)
        