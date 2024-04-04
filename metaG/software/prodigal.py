import argparse
import subprocess
import os
import metaG
from metaG.utils import parse_config_file

PRODIGAL_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/prodigal/prodigal"
ARGS_JSON = f"{os.path.dirname(metaG.__file__)}/lib/softs/prodigal/args.json"

class PRODIGAL:
    def __init__(self,
                 contig_file,
                 faa_out,
                 ffn_out,
                 out,
                 config_file = None
                 ) -> None:
        
        self.contig_file = contig_file
        self.faa_out = faa_out
        self.ffn_out = ffn_out
        self.out = out
        self.config_file = config_file
    
    def run(self):
        cmd = (
            f"{PRODIGAL_PATH} -i {self.contig_file} -p meta -q -a {self.faa_out} -d {self.ffn_out} -o {self.out} "
        )
        if self.config_file  not in [ None, "None"]:
            advance_args = parse_config_file(self.config_file, "PRODIGAL", args_json=ARGS_JSON,args_prfx="-")
            cmd += advance_args
        
        subprocess.check_call(cmd, shell=True)
        

def main():
    parser = argparse.ArgumentParser(description='Warpper for fastqc')
    parser.add_argument('--contig_file', help='', required=True)
    parser.add_argument('--faa_out', help='', required=True)
    parser.add_argument('--ffn_out', help='', required=True)
    parser.add_argument('--out', help='', required=False, default= None)
    parser.add_argument('--config_file', help='', required=False, default= None)
    
    args = parser.parse_args()

    runner = PRODIGAL(
                 contig_file = args.contig_file,
                 faa_out = args.faa_out,
                 ffn_out = args.ffn_out,
                 out = args.out,
                 config_file = args.config_file
    )

    runner.run()
    
if __name__ == '__main__':
    main()