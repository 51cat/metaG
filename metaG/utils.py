import os

def get_software_path(name):
    import metaG
    moduledir = os.path.dirname(metaG.__file__)
    path = os.path.abspath(f'{moduledir}/software/{name}.py')
    return path


def merge_fastqc_res(facstqc_dir, outdir):
    pass