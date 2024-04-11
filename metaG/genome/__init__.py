STEPS = {
    "pre_process":"pre-process",
    "assembly":"assembly",
    "predict":"predict",
    "ann":"ann",
    "count":"count"
}

ARGS_DICT = {
    "pre-process": {
        "host": None,
        "host_genome": None,
        "outdir": None,
        "config_file": None,
        "qc_use": "trimmomatic",
        "host_remove_use": "bwa"
    },
    "assembly": {
        'outdir':None,
        "config_file": None,
        'min_contig_len':500,
        'assembly_use': "MEGAHIT"
    },
    "predict": {
        'outdir':None,
        'word_size':9,
        'identity_threshold':0.95,
        'shorter_coverage':0.9,
        'translate_table': 11,
        'config_file':None
    },
    "ann": {
        'outdir':None,
        'database_use':None,
        'annota_use':"diamond",
        'method':"blastp",
        'min_evalue':0.00001,
        'min_identity': 80,
        'format':6,
        'max_target_seqs':10,
        'block_size':8,
        "config_file": None
    },
    "count": {
        'outdir':None
    }
}