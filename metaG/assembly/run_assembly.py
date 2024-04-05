from metaG.assembly.assembly_megahit import MEGAHITer
from metaG.common.minana import MinAna
from metaG.common.seqtools import SeqProcesser
from metaG.utils import get_target_dir, merge_json_files
import json

class Assembly(MinAna):
    def __init__(
            self,
            fq_json= None,
            outdir= None ,
            min_contig_len=500,
            config_file = None
            ) -> None:
        super().__init__(outdir=outdir)
        self.fq_json = fq_json
        self.outdir = outdir
        self.config_file = config_file
        self.min_contig_len = min_contig_len
        self.jsons = []

    def start(self):
        with open(self.fq_json, 'r', encoding='utf-8') as fd:
            fq_path_dict = json.load(fd)
        
        for sample_name in fq_path_dict.keys():
            r1 = fq_path_dict[sample_name]["R1"]
            r2 = fq_path_dict[sample_name]["R2"]
            runner = MEGAHITer(
                r1=r1, 
                r2=r2, 
                sample_name=sample_name, 
                outdir=self.outdir,
                min_contig_len = self.min_contig_len,
                config_file=self.config_file
            )
            runner.run()
            self.jsons.append(runner.get_clean_json())
        clean_contig_dict  = merge_json_files(self.jsons)
        target_dir = get_target_dir(self.outdir, "assembly")
        self.write_json(clean_contig_dict, f"{target_dir}/clean_contig.json")
        # write stat
        reads = []
        for k, _ in clean_contig_dict.items():
            reads.append(clean_contig_dict[k])
        SeqProcesser.stat(f"{target_dir}/assembly_fa_stat.txt", reads)