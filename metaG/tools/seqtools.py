import subprocess
import os
from collections import defaultdict

class SeqProcesser:
    def __init__(self):
        self.in_fa = None
        self.out_fa = None
    
    def set_in_fa(self, in_fa):
        self.in_fa = in_fa

    def set_out_fa(self, out_fa):
        self.out_fa = out_fa

    def in_fa_iter(self):
        with open(self.in_fa) as fd:
            while True:
                line = fd.readline()
                line = line.strip("\n")
                if not line:
                    break
                yield line

    def rename(self, target_name):
        inx = 0
        with open(self.out_fa, "w") as fd_out:
            for line in self.in_fa_iter():
                
                if line.startswith(">"):
                    inx += 1
                    fd_out.write(f">{target_name}_{inx}\n")
                else:
                    fd_out.write(f"{line}\n")


    def getlen(self, out_count_file):
        len_dict = {}
        with open(out_count_file, "w") as fd:
            fd.write("seq_name\tseq_len\n")
            for line in self.in_fa_iter():
                if line.startswith(">"):
                    seq_name = line
                    len_dict.update({seq_name:0})
                else:
                    seq_len = len(line)
                    len_dict.update({seq_name:seq_len})
                
            
            for k, v in len_dict.items():
                fd.write(f"{k}\t{v}\n")

    def format(self):
        cache = 500000
        cache_dict = defaultdict(lambda:defaultdict(str))
        with open(self.out_fa, "w") as fd:
            for line in self.in_fa_iter():
                if line.startswith(">"):
                    seq_name = line.strip("\n")
                    cache_dict.update({seq_name:[]})
                else:
                    cache_dict[seq_name].append(line.strip("\n"))

                if len(cache_dict) == cache:
                    for s_name, s in cache_dict.items():
                        seq = "".join(s)
                        fd.write(f"{s_name}\n{seq}\n")
            
            if len(cache_dict) != 0:
                for s_name, s in cache_dict.items():
                    seq = "".join(s)
                    fd.write(f"{s_name}\n{seq}\n")
    
    @staticmethod
    def stat(stat_file_out,fa_lst):
        import metaG
        seqkit_exec = f"{os.path.dirname(metaG.__file__)}/lib/softs/seqkit/seqkit"
        files = " ".join(fa_lst)
        cmd = f"{seqkit_exec} stat {files} -b -a > {stat_file_out}"
        subprocess.check_call(cmd, shell=True)


    def merge(self, fa_lst):
        with open(self.out_fa, "w") as fd_out:
            for file in fa_lst:
                self.set_in_fa(file)
                for line in self.in_fa_iter():
                    fd_out.write(f"{line}\n")