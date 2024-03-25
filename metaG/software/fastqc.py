import argparse
import subprocess
from metaG.common.log import add_log
import os
import metaG

FASTQC_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/FastQC/fastqc"

class Fastqc:
    def __init__(self,
                 r1 = None,
                 r2 = None,
                 out = None,
                 ) -> None:
        
        self.r1 = r1
        self.r2 = r2
        self.out = out

    def run(self):
        cmd = (
            f"{FASTQC_PATH} -o {self.out}  {self.r1} {self.r2}"
        )
        subprocess.check_call(cmd, shell=True)

        

def main():
    parser = argparse.ArgumentParser(description='Warpper for fastqc')
    parser.add_argument('--r1', help='', required=True)
    parser.add_argument('--r2', help='', required=True)
    parser.add_argument('--out', help='', required=True)
    
    args = parser.parse_args()

    runner = Fastqc(
            r1 = args.r1,
            r2 = args.r2,
            out = args.out,
    )

    runner.run()
    
if __name__ == '__main__':
    main()