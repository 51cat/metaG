import json
from collections import defaultdict
import os
from metaG.common.minana import MinAna
import re
from metaG.common.log import add_log

class DataLoader(MinAna):
    def __init__(self, fq_files_table, outdir) -> None:
        super().__init__(outdir=outdir)

        self.fq_files_table = fq_files_table
        self.fq_table_dict = defaultdict(lambda: defaultdict(str))
        self.all_reads = []
    
    @add_log
    def parse_table_to_dict(self):
        with open(self.fq_files_table) as fd:
            for line in fd.readlines():
                sample_name, r1, r2 = list(map(lambda x: x.strip("\n"), re.split(r" |\t", line)))

                r1, r2 = os.path.abspath(r1), os.path.abspath(r2)

                if not os.path.exists(r1):
                    raise FileNotFoundError(f"Error path of r1 {r1}")

                if not os.path.exists(r2):
                    raise FileNotFoundError(f"Error path of r2 {r2}")

                self.fq_table_dict[sample_name]["R1"] = r1
                self.fq_table_dict[sample_name]["R2"] = r2

                self.all_reads.append(r1)
                self.all_reads.append(r2)
        self.parse_table_to_dict.logger.info(f"Total samples: {len(self.fq_table_dict)}")
    
    def link_data(self):
        self.make_step_outdir("00.rawdata")
        cmds = [f"ln -s {f} {self.outdir}/00.rawdata/" 
                for f in self.all_reads]
        self.run_cmds(cmds)
    
    def write_json(self):
        with open(f"{self.outdir}/00.rawdata/raw_data.json", "w") as fd:
            json.dump(self.fq_table_dict, fd, indent=4)
    
    def get_rawdata_json_path(self):
        return f"{self.outdir}/00.rawdata/raw_data.json"

    def run(self):
        self.parse_table_to_dict()
        self.link_data()
        self.write_json()