from metaG.common.minana import MinAna
import os
import json
from metaG.utils import get_target_dir, merge_json_files
from metaG.software.interface import SoftInterface as SIF
from collections import defaultdict
from metaG.count.count_gene import GeneCounter
from multiprocessing import Pool

def run_task(task):
    task.run()

class Counter(MinAna):
    def __init__(self, 
                 fq_json,
                 genome_fa,
                 outdir= None ,
                 config_file = None,
                 ppp = False
            ) -> None:
        super().__init__(outdir=outdir)
        self.fq_json = fq_json
        self.genome_fa = genome_fa
        self.outdir = outdir
        self.config_file = config_file
        self.count_jsons = []
        self.tasks = []
        self.target_dir = None

        self.ppp = ppp
    

    def multi_map(self):
        with open(self.fq_json, 'r', encoding='utf-8') as fd:
            samples_dict = json.load(fd)
        
        each_ncpu = int(128/3) - 1

        for sample_name in samples_dict.keys():
            r1 = samples_dict[sample_name]["R1"]
            r2 = samples_dict[sample_name]["R2"]

            count_runner = GeneCounter(
                r1, r2, sample_name, self.outdir, self.genome_fa
            )
            if self.ppp:
                count_runner.set_cpu(each_ncpu)
            else:
                count_runner.set_cpu(64)
            self.tasks.append(count_runner)
            self.count_jsons.append(count_runner.raw_reads_json)

    def start(self):
        self.multi_map()
        
        for t in self.tasks:
            t.run()
        
        self.target_dir = get_target_dir(self.outdir, "count")
        raw_count_dict  = merge_json_files(self.count_jsons)
        self.write_json(raw_count_dict, f"{self.target_dir}/raw_reads.json")


def main():
    fq_json = "/home/issas/dev/meta_genome/test/test_final/out/01.prep/clean_data.json"
    genome_fa = "/home/issas/dev/meta_genome/test/test_final/out/03.predict/GeneSet_clean_unique.fa"
    outdir = "./test_out/"

    s = Counter(
        fq_json, genome_fa, outdir, ppp=False
    )

    s.start()

if __name__ == '__main__':
    main()