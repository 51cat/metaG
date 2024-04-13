from metaG.core.log import add_log
import metaG
import os
import argparse
from metaG.genome import STEPS, ARGS_DICT

class GENOME_STARTER:
    def __init__(self, 
                 rawdata_table, 
                 outdir,
                 host= None, 
                 host_genome = None, 
                 step = "all", 
                 configfile = None,
                 parallel = False,
                 **kwargs):
        self.rawdata_table = rawdata_table
        self.host = host
        self.host_genome = host_genome
        self.step = step
        self.outdir = outdir
        self.parallel = parallel
        self.configfile = configfile

        self._cmd = "metaG_genome "
        self._cmd_lst = []
        self.args_dict = kwargs

        self._hostbase_path = f"{os.path.dirname(metaG.__file__)}/lib/host_database"
        self._supports = os.listdir(self._hostbase_path)
    
        self.__mk_dict = {
            "pre_process":self.mk_pre_process,
            "assembly":self.mk_assembly,
            "predict":self.mk_predict_gene,
            "ann":self.mk_ann,
            "count": self.mk_count
        }
        
        self.default_args_dict =ARGS_DICT
        self.steps_dict = STEPS
    
    def __init_cmd(self):
        
        self._cmd = "metaG_genome "


    def __mk_subcmd(self, subcmd):
        return f"{self._cmd}{subcmd}"

    @add_log
    def mk_pre_process(self):
        pre_process_cmd_str = (
            f"{self.steps_dict['pre_process']} "
            f"--rawdata_table {self.rawdata_table} "
            f"--host {self.host} "
            f"--outdir {self.outdir} "
        )
        if self.host_genome not in ["None", None]:
            pre_process_cmd_str += f"--host_genome {self.host_genome} "

        self._cmd_lst.append(self.__mk_subcmd(pre_process_cmd_str))
        self.__init_cmd()
    
    @add_log
    def mk_assembly(self):
        assembly_cmd_str = f"{self.steps_dict['assembly']} "
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
        predict_cmd_str = f"{self.steps_dict['predict']} "
        if self.step != "all":
            predict_cmd_str += f"--rawdata_table {self.rawdata_table} "
        predict_cmd_str += (
            f"--outdir {self.outdir} "
            f"--word_size {self.args_dict['word_size']} "
            f"--identity_threshold {self.args_dict['identity_threshold']} "
            f"--shorter_coverage {self.args_dict['shorter_coverage']} "
            f"--translate_table {self.args_dict['translate_table']} "
        )
        self._cmd_lst.append(self.__mk_subcmd(predict_cmd_str))
        self.__init_cmd()
    
    @add_log
    def mk_ann(self):
        ann_cmd_str = f"{self.steps_dict['ann']} "
        if self.step != "all":
            ann_cmd_str += f"--query_fa {self.args_dict['query_fa']} "
            ann_cmd_str += f"--uniq_gene_fa {self.args_dict['uniq_gene_fa']} "
        else:
            ann_cmd_str += (
            f"--outdir {self.outdir} "
            f"--database_use {self.args_dict['database_use']} "
            f"--min_evalue {self.args_dict['min_evalue']} "
            f"--min_identity {self.args_dict['min_identity']} "
            f"--max_target_seqs {self.args_dict['max_target_seqs']} "
            )
        self._cmd_lst.append(self.__mk_subcmd(ann_cmd_str))
        self.__init_cmd()

    @add_log
    def mk_count(self):
        count_cmd_str = f"{self.steps_dict['count']} "
        if self.step != "all":
            count_cmd_str += f"--rawdata_table {self.args_dict['rawdata_table']} "
            count_cmd_str += f"--db_ann_dir {self.args_dict['db_ann_dir']} "
            count_cmd_str += f"--genome_fa {self.args_dict['genome_fa']} "
        else:
            count_cmd_str += (
            f"--outdir {self.outdir} "
            )
        self._cmd_lst.append(self.__mk_subcmd(count_cmd_str))
        self.__init_cmd()

    def add_configfile(self):
        self._cmd_lst = list(
            map(lambda x:f"{x} --config_file {self.configfile}", self._cmd_lst)
            )

    def add_parallel(self):
        self._cmd_lst = list(
            map(lambda x:f"{x} --parallel ", self._cmd_lst)
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
        self.mk_ann()
        self.mk_count()
        if self.parallel:
            self.add_parallel()
        self.add_configfile()
    
    @add_log
    def mk_step(self, steps):
        steps_lst = steps.split(",")
        for step in steps_lst:
            self.__mk_dict[step]()
        self.add_configfile()
    
    def write_cmd(self):
        cmd_str = "\n".join(self._cmd_lst)
        with open("./run_metaG_genome.sh", "w") as fd:
            fd.write(cmd_str)

def main():
    from metaG import get_default_dbs
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--rawdata_table', help='', required=True)
    parser.add_argument('--outdir', help='', default="./out/", required=False)
    parser.add_argument('--host', help='', required=False)
    parser.add_argument('--step', help='', required=False, default="all")
    parser.add_argument('--host_genome', help='', required=False)
    parser.add_argument('--configfile', help='', default="./configs.yaml", required=False)

    parser.add_argument('--min_contig_len', help='', required=False, default=500)

    parser.add_argument('--word_size', help='', default=9)
    parser.add_argument('--identity_threshold', help='', default=0.95)
    parser.add_argument('--shorter_coverage', help='', default=0.9)
    parser.add_argument('--translate_table', help='', default=11)
    
    parser.add_argument('--query_fa', help='', default="")
    parser.add_argument('--uniq_gene_fa', help='', default="")
    parser.add_argument('--database_use', help='', default=get_default_dbs())
    parser.add_argument('--min_evalue', help='', default=0.00001)
    parser.add_argument('--min_identity', help='', default=80)
    parser.add_argument('--max_target_seqs', help='', default=10)

    parser.add_argument('--parallel', help='', action="store_true")

    args = parser.parse_args()
    runner = GENOME_STARTER(
            rawdata_table = args.rawdata_table, 
            outdir = args.outdir,
            host= args.host, 
            host_genome = args.host_genome, 
            step = args.step, 
            configfile = args.configfile,
            min_contig_len = args.min_contig_len,
            word_size = args.word_size,
            identity_threshold = args.identity_threshold,
            query_fa = args.query_fa,
            uniq_gene_fa = args.uniq_gene_fa,
            database_use = args.database_use,
            min_evalue = args.min_evalue,
            min_identity = args.min_identity,
            max_target_seqs = args.max_target_seqs,
            shorter_coverage = args.shorter_coverage,
            translate_table = args.translate_table,
            parallel = args.parallel

    )

    runner.mk_rundir()

    if args.step == "all":
        runner.mk_all()
    else:
        runner.mk_step(args.step)
    runner.write_cmd()

if __name__ == '__main__':
    main()