import json
import glob
import pandas as pd
import psutil
from metaG.utils import merge_json_files, merge_fastqc_res

from metaG.tools.seqtools import SeqProcesser
from metaG.core.minana import MinAna
from metaG.core.dataload import DataLoader
from metaG.tools.index_host import IndexHost
from metaG.tools.qc import QCer
from metaG.tools.host_remove import HostRemover, multi_extract
from metaG.softs.fastqc import Fastqc

AVA_PCT = 0.95
BWA_TOTAL_AVA = psutil.virtual_memory().available*AVA_PCT
BWA_RAM = 34359738368/2

class DataPreProcessor(MinAna):
    def __init__(self, 
                 fq_files_table, 
                 host,
                 outdir,
                 host_genome_fa = None,
                 config_file = None,
                 qc_use = "trimmomatic",
                 host_remove_use = "bwa",
                 parallel = True
                 ) -> None:
        super().__init__(outdir=outdir, step_name="prep")

        self.fq_files_table = fq_files_table
        self.host = host
        self.outdir = outdir
        self.qc_use = qc_use
        self.host_remove_use = host_remove_use
        self.host_genome_fa =host_genome_fa
        self.config_file = config_file
        self.parallel = parallel

        self.rawdata_json = None
        self.index_dir = None

        self._qc_dir = "01.prep/qc/"
        self._host_index_dir = "01.prep/host_index/"
        self._host_remove_dir = "01.prep/host_remove/"
        self._fastqc_dir = "01.prep/fastqc/"

        self.qc_outdir = f"{self.outdir}/{self._qc_dir}/"
        self.host_index_dir = f"{self.outdir}/{self._host_index_dir}/"
        self.host_remove_dir = f"{self.outdir}/{self._host_remove_dir}/"
        self.fastqc_dir = f"{self.outdir}/{self._fastqc_dir}/"


        self.make_step_outdir(self._qc_dir)
        self.make_step_outdir(self._host_index_dir)
        self.make_step_outdir(self._host_remove_dir)
        self.make_step_outdir(self._fastqc_dir)
        
        self.prep_start()
        
        self.prep_stat = f"{self.parent_dir}/prep_stat.txt"
        self.host_count_file = f"{self.parent_dir}/host_count.tsv"
        self.clean_fq_json = f"{self.parent_dir}/clean_fastq.json"
        

        self.qc_tasks = []
        self.host_remove_tasks = []
        self.generate_qc_report_task_lst = []
        self.extract_bam_records = []

    def load_rawdata(self):
        runner = DataLoader(
            self.fq_files_table,
            self.outdir
        )
        runner.run()
        with open(runner.rawdata_json) as fd:
            self.rawdata_json = json.load(fd)
    
    def index_host(self):
        runner = IndexHost(
            self.host,
            self.host_index_dir,
            self.host_genome_fa
        )
        runner.set_index_use(self.host_remove_use)
        runner.run()
        self.index_dir = runner.index_dir
    
    def make_qc_tasks(self):
        
        for sample_name in self.rawdata_json.keys():
            r1 = self.rawdata_json[sample_name]["R1"]
            r2 = self.rawdata_json[sample_name]["R2"]
            runner = QCer(
                r1= r1, 
                r2= r2, 
                sample_name=sample_name, 
                outdir=self.qc_outdir,
                config_file = self.config_file
            )
            runner.set_qc_use(self.qc_use)
            self.qc_tasks.append(runner)
    
    def make_host_remove_tasks(self):
        paired_reads_all = merge_json_files(
            glob.glob(f"{self.qc_outdir}/*_trimmomatic_stat.json")
        )
        for sample_name in paired_reads_all.keys():
            r1 = paired_reads_all[sample_name]["R1"]
            r2 = paired_reads_all[sample_name]["R2"]
            print(r1)
            print(r2)
            runner = HostRemover(
                r1 = r1,
                r2 = r2,
                host= self.host,
                genome_dir=self.index_dir,
                sample_name=sample_name,
                outdir=self.host_remove_dir
            )
            runner.set_host_remove_use(self.host_remove_use)
            self.host_remove_tasks.append(runner)

            self.extract_bam_records.append(
                (sample_name, runner.out_bam, runner.out_r1, runner.out_r2, runner.host_count_file)
            )
    
    def make_preprocess_stat(self):
        merge_host_remove_dict = merge_json_files(
            glob.glob(f"{self.host_remove_dir}/*_clean_data.json"))
        merge_count_res = pd.concat(
            [pd.read_table(f) for f in glob.glob(f"{self.host_remove_dir}/*_host_count.tsv")])

        fq_all = []
        for k, v in merge_host_remove_dict.items():
            fq_all.append(merge_host_remove_dict[k]["R1"])
            fq_all.append(merge_host_remove_dict[k]["R2"])
        

        SeqProcesser.stat(self.prep_stat, fq_all)
        self.write_json(
            merge_host_remove_dict, self.clean_fq_json
        )
        merge_count_res.to_csv(self.host_count_file, sep = "\t", index=None)  

    def generate_qc_report(self):
        with open(self.clean_fq_json) as fd:
            clean_fq_dict = json.load(fd)
        reads_lst = []
        
        for sample_name in clean_fq_dict.keys():
            reads_lst.append(clean_fq_dict[sample_name]["R1"])
            reads_lst.append(clean_fq_dict[sample_name]["R2"])
        
        runner = Fastqc(
            reads_list=reads_lst,
            out=self.fastqc_dir)
        runner.run()

    def start(self):
        self.load_rawdata()
        self.index_host()
        self.make_qc_tasks()
        self.run_tasks(self.qc_tasks, self.parallel)
        self.make_host_remove_tasks()
        self.run_tasks(self.host_remove_tasks, self.parallel, n = max(int(BWA_TOTAL_AVA/BWA_RAM), 1))
        multi_extract(self.extract_bam_records)
        self.make_preprocess_stat()
        self.generate_qc_report()
        # merge
        merge_fastqc_res(self.fastqc_dir, self.parent_dir)


def main():
    a = DataPreProcessor(
        fq_files_table="/home/issas/dev/meta_genome/data/raw_file.list",
        outdir="./test/",
        config_file=None,
        host="human"
    )
    
    a.start()

if __name__ == '__main__':
    main()