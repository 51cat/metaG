from metaG.common.minana import MinAna
import os
import json
from metaG.utils import get_target_dir, merge_json_files
from metaG.software.interface import SoftInterface as SIF
from collections import defaultdict
from metaG.count.count_gene import GeneCounter
from multiprocessing import Pool

class Counter(MinAna):
    def __init__(self, 
                 fq_json,
                 genome_fa,
                 outdir= None ,
                 config_file = None
            ) -> None:
        super().__init__(outdir=outdir)
        self.fq_json = fq_json
        self.genome_fa = genome_fa
        self.outdir = outdir
        self.config_file = config_file
        self.count_jsons = []
        self.tasks = []
        self.target_dir = None
    

    def make_tasks(self):
        with open(self.fq_json, 'r', encoding='utf-8') as fd:
            samples_dict = json.load(fd)

        for sample_name in samples_dict.keys():
            r1 = samples_dict[sample_name]["R1"]
            r2 = samples_dict[sample_name]["R2"]

            count_runner = GeneCounter(
                r1, r2, sample_name, self.outdir, self.genome_fa
            )
            self.tasks.append(count_runner)
            self.count_jsons.append(count_runner.raw_reads_json)

    def start(self):
        self.make_tasks()
        self.run_tasks(self.tasks, parallel=True)
        
        self.target_dir = get_target_dir(self.outdir, "count")
        raw_count_dict  = merge_json_files(self.count_jsons)
        self.write_json(raw_count_dict, f"{self.target_dir}/raw_reads.json")