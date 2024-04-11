def get_default_cpus():
    import multiprocessing
    return min(128, multiprocessing.cpu_count())