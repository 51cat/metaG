import json
from collections import defaultdict
import os
from metaG.common.minana import MinAna
import re
from metaG.common.log import add_log

class DataLoader(MinAna):
    def __init__(self, data_table, outdir, mode = 1) -> None:
         super().__init__(outdir=outdir, step_name="rawdata")
         self.data_table = data_table
         self.outdir = outdir
         self.mode = mode
         self.mode_dict = defaultdict(lambda: defaultdict(str)) if self.mode == 1 else defaultdict(str)
         self.all_reads = []
    
    @add_log
    def parse_mode_1(self):
        with open(self.data_table) as fd:
            for line in fd.readlines():
                sample_name, r1, r2 = list(map(lambda x: x.strip("\n"), re.split(r" |\t", line)))

                r1, r2 = os.path.abspath(r1), os.path.abspath(r2)

                if not os.path.exists(r1):
                    raise FileNotFoundError(f"Error path of r1 {r1}")

                if not os.path.exists(r2):
                    raise FileNotFoundError(f"Error path of r2 {r2}")

                self.mode_dict[sample_name]["R1"] = r1
                self.mode_dict[sample_name]["R2"] = r2

                self.all_reads.append(r1)
                self.all_reads.append(r2)
        self.parse_mode_1.logger.info(f"Total samples: {len(self.mode_dict)}")

    @add_log
    def parse_mode_2(self):
        with open(self.data_table) as fd:
            for line in fd.readlines():
                sample_name, r = list(map(lambda x: x.strip("\n"), re.split(r" |\t", line)))
                self.mode_dict.update({sample_name:r})
                self.all_reads.append(r)
        self.parse_mode_2.logger.info(f"Total samples: {len(self.mode_dict)}")

    def link_data(self):
        self.make_step_outdir("00.rawdata")
        cmds = [f"ln -s {f} {self.outdir}/00.rawdata/" 
                for f in self.all_reads]
        self.run_cmds(cmds)

    def write_json(self):
        with open(f"{self.outdir}/00.rawdata/raw_data.json", "w") as fd:
            json.dump(self.mode_dict, fd, indent=4)
    
    def get_rawdata_json_path(self):
        return f"{self.outdir}/00.rawdata/raw_data.json"

    def run(self):
        if self.mode == 1:
            self.parse_mode_1()
        else:
            self.parse_mode_2()
        
        self.link_data()
        self.write_json()