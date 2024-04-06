from metaG import STEPS
from metaG.common.log import add_log
import metaG
import os
import argparse

class METAG_STARTER:
    def __init__(self, 
                 rawdata_table, 
                 outdir,
                 host= None, 
                 fa = None, 
                 step = "all", 
                 configfile = None,
                 **kwargs):
        self.rawdata_table = rawdata_table
        self.host = host
        self.fa = fa
        self.step = step
        self.outdir = outdir
        self.configfile = configfile

        self._cmd = "metaG "
        self._cmd_lst = []
        self.args_dict = kwargs

        self._hostbase_path = f"{os.path.dirname(metaG.__file__)}/lib/host_database"
        self._supports = os.listdir(self._hostbase_path)

        self.__mk_dict = {
            "pre_process": self.mk_pre_process,
            "assembly": self.mk_assembly,
            "predict_gene": self.mk_predict_gene,
        }
    
    def __init_cmd(self):
        self._cmd = "metaG "

    def __mk_subcmd(self, subcmd):
        return f"{self._cmd}{subcmd}"

    @add_log
    def mk_pre_process(self):
        pre_process_cmd_str = (
            f"{STEPS['pre_process']} "
            f"--rawdata_table {self.rawdata_table} "
            f"--host {self.host} "
            f"--outdir {self.outdir} "
        )
        try:
            pre_process_cmd_str += f"{self.args_dict['fa']} "
        except KeyError:
            if self.host not in self._supports:
                raise KeyError
        self._cmd_lst.append(self.__mk_subcmd(pre_process_cmd_str))
        self.__init_cmd()
    
    @add_log
    def mk_assembly(self):
        assembly_cmd_str = f"{STEPS['assembly']} "
        if self.step != "all":
            assembly_cmd_str += f"--rawdata_table {self.rawdata_table} "
        
        assembly_cmd_str += (
            f"--min_contig_len {self.args_dict['min_contig_len']} "
            f"--outdir {self.outdir} "
        )
        self._cmd_lst.append(self.__mk_subcmd(assembly_cmd_str))
        self.__init_cmd()
    
    @add_log
    def mk_predict_gene(self):
        predict_cmd_str = f"{STEPS['predict_gene']} "
        if self.step != "all":
            predict_cmd_str += f"--rawdata_table {self.rawdata_table} "
        predict_cmd_str += (
            f"--use {self.args_dict['use']} "
            f"--outdir {self.outdir} "
            f"--word_size {self.args_dict['word_size']} "
            f"--identity_threshold {self.args_dict['identity_threshold']} "
            f"--shorter_coverage {self.args_dict['shorter_coverage']} "
        )
        self._cmd_lst.append(self.__mk_subcmd(predict_cmd_str))
        self.__init_cmd()
    
    def add_configfile(self):
        self._cmd_lst = list(
            map(lambda x:f"{x} --config_file {self.configfile}", self._cmd_lst)
            )

    def mk_rundir(self):
        os.system(f"mkdir {self.outdir}")
        os.system(f"mkdir data")
        os.system("get_config")
        adapters_path = f"{os.path.dirname(metaG.__file__)}/lib/adapters/*"
        os.system(f"cp -a {adapters_path} ./data/")

    @add_log
    def mk_all(self):
        self.mk_pre_process()
        self.mk_assembly()
        self.mk_predict_gene()
        self.add_configfile()
    
    @add_log
    def mk_step(self, steps):
        steps_lst = steps.split(",")
        for step in steps_lst:
            self.__mk_dict[step]()
        self.add_configfile()
    
    def write_cmd(self):
        cmd_str = "\n".join(self._cmd_lst)
        with open("./run_metaG.sh", "w") as fd:
            fd.write(cmd_str)

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--rawdata_table', help='', required=True)
    parser.add_argument('--outdir', help='', default="./out/", required=False)
    parser.add_argument('--host', help='', required=False)
    parser.add_argument('--steps', help='', required=False, default="all")

    parser.add_argument('--fa', help='', required=False)
    parser.add_argument('--configfile', help='', default="./configs.yaml", required=False)

    parser.add_argument('--min_contig_len', help='', required=False, default=500)

    parser.add_argument('--use', help='', default="prodigal")
    parser.add_argument('--word_size', help='', default=9)
    parser.add_argument('--identity_threshold', help='', default=0.95)
    parser.add_argument('--shorter_coverage', help='', default=0.9)
    
    args = parser.parse_args()
    runner = METAG_STARTER(
            rawdata_table = args.rawdata_table, 
            outdir = args.outdir,
            host= args.host, 
            fa = args.fa, 
            step = args.steps, 
            configfile = args.configfile,
            min_contig_len = args.min_contig_len,
            use = args.use,
            word_size = args.word_size,
            identity_threshold = args.identity_threshold,
            shorter_coverage = args.shorter_coverage
    )

    runner.mk_rundir()

    if args.steps == "all":
        runner.mk_all()
    else:
        runner.mk_step(args.steps)
    runner.write_cmd()

if __name__ == '__main__':
    main()