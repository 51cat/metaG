import os
import json
import glob
import subprocess
import yaml

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

def seqtools_run(out_file, do, target_name = None, in_fa= None, fa_lst = None):
    import metaG
    moduledir = os.path.dirname(metaG.__file__)
    path = os.path.abspath(f'{moduledir}/src/seqtools')        
    
    cmd_basic = (
         f"{path} "
         f"--outfile {out_file} "
    )

    if do == "rename":
        cmd_basic += f" --fa {in_fa} "
        cmd_basic += f" --target_name {target_name} "
        cmd_basic += f" --method {do} "
    
    if do == "merge":
        fas = "::".join(fa_lst)
        return

    if do == "len":
        cmd_basic += f" --fa {in_fa} "
        cmd_basic += f" --method {do} "
    subprocess.check_call(cmd_basic, shell=True)

def parse_config_file(config_yaml, key, args_prfx = "--", return_dict = False):
    flag1 = ["True", "TRUE", "true", "T", "t", True]
    flag2 = ["False", "FALSE", "false", "F", "f", False]

    with open(config_yaml,encoding='utf-8') as fd:
        data = yaml.load(fd,Loader=yaml.FullLoader)
    use = data[key]
    
    if return_dict:
        return use
    
    args_str = ""
    for arg, value in use.items():
        if value in flag1:
            args_str += f"{args_prfx}{arg} "
        elif value in flag2 :
            continue
        else: 
            args_str += f"{args_prfx}{arg} {value} "
    return args_str