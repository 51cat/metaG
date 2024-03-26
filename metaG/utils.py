import os
import json
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
