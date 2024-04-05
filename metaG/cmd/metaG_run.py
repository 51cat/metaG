STEPS = {
    "pre_process":"pre-process",
    "assembly":"assembly",
    "predict_gene":"predict-gene"
}

class METAG_STARTER:
    def __init__(self, 
                 rawdata_table, 
                 outdir,
                 host= None, 
                 fa = None, 
                 step = "all", 
                 **kwargs):
        self.rawdata_table = rawdata_table
        self.host = host
        self.fa = fa
        self.step = step
        self.args_dict = kwargs