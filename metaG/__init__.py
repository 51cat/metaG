def get_default_cpus():
    import multiprocessing
    return min(128, multiprocessing.cpu_count())

def get_default_dbs():
    import metaG
    import os 
    dbuse = os.listdir(f"{os.path.dirname(metaG.__file__)}/lib/database/DIAMOND/")
    return ":".join(dbuse)