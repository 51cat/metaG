import pandas as pd
import numpy as np
from collections import defaultdict
import json

class GeneAnn:
    def __init__(self, count_dict, ann_dict) -> None:
        self.count_dict = count_dict
        self.ann_dict = ann_dict
        self._new_count_dict = defaultdict(lambda: defaultdict(int))
       
    def ann(self):
        for sample_name in self.count_dict.keys():
            for gene, _ in self.count_dict[sample_name].items():
                try:
                    new_gene_name = self.ann_dict[gene]
                    self._new_count_dict[sample_name][new_gene_name] += self.count_dict[sample_name][gene]
                except KeyError:
                    pass
    @property
    def ann_count_dict(self):
        return self._new_count_dict


class GeneTransfer:
    """
    count_dict:
        {
            "sample_1":{
                "gene_1": 100,
                "gene_2: 200,
                ...
            },
            "sample_3: {
                "gene_1: 120,
                "gene_2: 130,
                ....
            },
            ....
        }
    """
    def __init__(self,count_dict, length_dict = None):
        self.count_dict = count_dict
        self.length_dict = length_dict
        
        self.fpkm_dict = defaultdict(lambda: defaultdict(int))
        self.cpm_dict = defaultdict(lambda: defaultdict(int))
        self.tpm_dict = defaultdict(lambda: defaultdict(int))

    def to_fpkm(self):
        for sample_name in self.count_dict.keys():
            counts = list(self.count_dict[sample_name].values())
            genes = list(self.count_dict[sample_name].keys())
            total = sum(counts)
            
            fpkms = map(
                lambda x, y: (x*10e6)/(self.length_dict[y]*total), counts, genes
            )
            
            for gene, fpkm in zip(genes, fpkms):
                self.fpkm_dict[sample_name].update({gene:fpkm})
    

    def to_tpm(self):
        for sample_name in self.count_dict.keys():
            counts = list(self.count_dict[sample_name].values())
            genes = list(self.count_dict[sample_name].keys())
            
            tpms = map(
                lambda x, y: (x*10e6)/(self.length_dict[y]*(np.sum(x/self.length_dict[y]))), counts, genes
            )
            for gene, tpm in zip(genes, tpms):
                self.tpm_dict[sample_name].update({gene:tpm})


    def to_cpm(self):
        for sample_name in self.count_dict.keys():
            counts = list(self.count_dict[sample_name].values())
            genes = list(self.count_dict[sample_name].keys())
            total = sum(counts)
            cpms = map(
                lambda x: 10e6 * x/total, counts
                )
            
            for gene, cpm in zip(genes, cpms):
                self.cpm_dict[sample_name].update({gene:cpm})


    def out_to_json(self, in_dict, outfile):
        json_str=json.dumps(in_dict, indent=4, ensure_ascii=False)
        with open(outfile, "w") as fd:
            fd.write(json_str)

    def out_to_df(self, in_dict, outfile):
        rows = []
        for k in in_dict.keys():
            for gene, exp in in_dict[k].items():
                row = (k, gene, exp)
                rows.append(row)
        df = pd.DataFrame(rows)
        df.columns = ["sample_name", "gene", "expression"]
        df = df.pivot(index='gene', columns='sample_name', values='expression').reset_index()
        df.fillna(0).to_csv(outfile, sep="\t", index = None)


    def save(self, outformat, outfile, res):
        if outformat == "df":
            self.out_to_df(res, outfile)
        if outformat == "json":
            self.out_to_json(res, outfile)    

    @property
    def fpkm(self):
        return self.fpkm_dict

    @property
    def tpm(self):
        return self.tpm_dict

    @property
    def cpm(self):
        return self.cpm_dict
    
    @property
    def count(self):
        return self.count_dict