def get_default_cpus():
    import multiprocessing
    return min(128, multiprocessing.cpu_count())

STEPS = {
    "pre_process":"pre-process",
    "assembly":"assembly",
    "predict_gene":"predict-gene"
}
