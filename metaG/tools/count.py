from metaG.core.minana import MinAna
import os
from collections import defaultdict
import pysam
from metaG.softs.bwa import BWA
from functools import partial

class GeneCounter(MinAna):
    def __init__(self,
                 r1,
                 r2,
                 sample_name,
                 outdir,
                 genome_fa
                 ) -> None:
        super().__init__(outdir)

        self.r1 = r1
        self.r2 = r2
        self.outdir = outdir
        self.genome_fa = genome_fa
        self.sample_name = sample_name
        self.outdir = outdir

        self.genome_dir = os.path.dirname(genome_fa)
        self.genome_name = genome_fa.split("/")[-1].split(".")[0]

        self.count_dict = defaultdict(partial(defaultdict, int))
        self.out_bam = f"{self.outdir}/{self.sample_name}.bam"
        self.count_reads_json = f"{self.outdir}/{self.sample_name}_raw_reads.json"
    
    def mapping_gene(self):
        runner = BWA(
            host=self.genome_name,
            r1 = self.r1,
            r2 = self.r2,
            mode = "map",
            genome_dir = self.genome_dir,
            cpu=self.cpu,
            memory=self.memory
        )
        runner.set_mem_out_bam(self.out_bam)
        runner.run()
    
    def count_gene(self):
        for r in pysam.AlignmentFile(self.out_bam):
            f1 = r.reference_name is not None
            f2 = r.is_paired
            if f1 & f2:
                self.count_dict[self.sample_name][r.reference_name] += 1
        self.write_json(self.count_dict, self.count_reads_json)
    
    @property
    def raw_reads_json(self):
        return self.count_reads_json

    @property
    def bam_file(self):
        return self.out_bam

    def run(self):
        self.mapping_gene()
        self.count_gene()


def main():
    r1 = "/home/issas/dev/meta_genome/test/test_final/out/01.prep/remove_host/PM_2_clean_R1.fastq.gz"
    r2 = "/home/issas/dev/meta_genome/test/test_final/out/01.prep/remove_host/PM_2_clean_R2.fastq.gz"
    fa = "/home/issas/dev/meta_genome/test/test_final/out/03.predict/GeneSet_clean_unique.fa"
    sample_name = "PM_2"
    outdir = "./test_out/"
    runner = GeneCounter(
        r1, r2, sample_name, outdir, genome_fa=fa
    )
    
    runner.run()

if __name__ == "__main__":
    main()