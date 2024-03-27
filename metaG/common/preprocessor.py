from metaG.QC.run_qc import QCfq
from metaG.indexhost.run_index import IndexHost
from metaG.common.load_rawdata import DataLoader
from metaG.utils import merge_json_files, merge_fastqc_res
import json
import glob
import os
from metaG.utils import get_target_dir
class DataPreProcessor:

    def __init__(self, 
                 fq_files_table, 
                 host,
                 outdir,
                 host_genome_fa = None) -> None:
        
        self.fq_files_table = fq_files_table
        self.host = host
        self.outdir = outdir
        self.host_genome_fa =host_genome_fa
        self.rawdata_json = None
    
    def load_rawdata(self):
        runner = DataLoader(
            self.fq_files_table,
            self.outdir
        )
        runner.run()
        with open(runner.get_rawdata_json_path()) as fd:
            #json_str = fd.readlines()
            self.rawdata_json = json.load(fd)
    
    def index_host(self):
        runner = IndexHost(
            self.host,
            self.outdir,
            self.host_genome_fa
        )

        runner.run()
    
    def qc_rawdata(self):
        # 暂时不加多进程, 方便debug
        for sample_name in self.rawdata_json.keys():
            r1 = self.rawdata_json[sample_name]["R1"]
            r2 = self.rawdata_json[sample_name]["R2"]
            runner = QCfq(
                r1 = r1, 
                r2= r2, 
                sample_name=sample_name, 
                outdir=self.outdir
            )
            runner.run()

        trim_dir = get_target_dir(self.outdir, "prep", "QC/TrimmomaticCut/")
        fastqc_dir = get_target_dir(self.outdir, "prep", "QC/Fastqc/")
        prep_dir = get_target_dir(self.outdir, "prep")

        json_files = glob.glob(f"{trim_dir}/*_trimmomatic_stat.json")
        dict_merge = merge_json_files(json_files)

        with open(f"{prep_dir}/paired_data.json", "w") as fd:
            json.dump(dict_merge, fd, indent=4)
        merge_fastqc_res(fastqc_dir, prep_dir)
    
    def run_preprocessor(self):
        self.load_rawdata()
        self.index_host()
        self.qc_rawdata()