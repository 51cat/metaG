import os
import json
import glob
import subprocess

def get_software_path(name):
    import metaG
    moduledir = os.path.dirname(metaG.__file__)
    path = os.path.abspath(f'{moduledir}/software/{name}.py')
    return path

def merge_json_files(json_list):
    merged_data = {}
    for json_file in json_list:
        with open(json_file, 'r') as f:
            data = json.load(f)
            merged_data.update(data)
    return merged_data

def merge_fastqc_res(facstqc_dir, outdir):
    cmd = f"multiqc {facstqc_dir} -o {outdir}"
    subprocess.check_call(cmd, shell=True)


def get_target_dir(res_outdir, step_name, sub_step = ""):
    if sub_step == "":
        dir = glob.glob(f"{res_outdir}/*{step_name}/")
        
        if len(dir) > 1 or len(dir) == 0:
            raise KeyError(f"Error {res_outdir}")
        return dir[0]
    
    else:
        dir = glob.glob(f"{res_outdir}/*{step_name}/{sub_step}")
        if len(dir) > 1 or len(dir) == 0:
            raise KeyError(f"Error {res_outdir}")
        return dir[0]

def rename_fa_to_target_name(in_fa, target, out_fa):
    with open(in_fa) as fd_in:
        with open(out_fa, "w") as fd_out:
            pass