import subprocess
import os

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
        pass
    
    @staticmethod
    def stat(stat_file_out,fa_lst):
        import metaG
        seqkit_exec = f"{os.path.dirname(metaG.__file__)}/lib/softs/seqkit/seqkit"
        files = " ".join(fa_lst)
        cmd = f"{seqkit_exec} stat {files} -b -a > {stat_file_out}"
        subprocess.check_call(cmd, shell=True)


    def merge(self, fa_lst):
        pass

def main():
    fa = "/home/issas/dev/meta_genome/test/test_preprocess2/02.assembly/megahit_out/test_3/final.contigs.fa"
    r = SeqProcesser()
    r.set_in_fa(fa)
    r.set_out_fa("./test.fa")
    r.rename("test")

    r.set_in_fa("./test.fa")
    r.getlen("./res.txt")

    SeqProcesser.stat("./stat.txt",[fa, "./test.fa"] )

if __name__ == '__main__':
    main()
