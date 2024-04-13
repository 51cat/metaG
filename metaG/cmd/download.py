import metaG
import os
import subprocess
import click

@click.group()
def main():
    pass

@main.command()
def lib():
    root_dir = f"{os.path.dirname(metaG.__file__)}"
    config_dir = f"{root_dir}/configs/.bypy"
    lib_dir = f"{root_dir}/lib/"
    adapters_dir = f"{root_dir}/lib/adapters/"
    softs_dir = f"{root_dir}/lib/softs/"
    if not os.path.exists:
        os.system(f"mkdir {lib_dir}")
    cmd1 = f"bypy --config-dir {config_dir} downdir /adapters {adapters_dir}"
    cmd2 = f"bypy --config-dir {config_dir} downdir /softs {softs_dir}"
    cmd3 = f"chmod -R +x {softs_dir}"
    subprocess.check_call(cmd1, shell=True)
    subprocess.check_call(cmd2, shell=True)
    subprocess.check_call(cmd3, shell=True)

@main.command()
def jp_rice():
    root_dir = f"{os.path.dirname(metaG.__file__)}"
    config_dir = f"{root_dir}/configs/.bypy"
    cmd = f"bypy --config-dir {config_dir} downfile /genome/JP_rice_genomic.fna ./"
    subprocess.check_call(cmd, shell=True)

@main.command()
def scyc():
    root_dir = f"{os.path.dirname(metaG.__file__)}"
    config_dir = f"{root_dir}/configs/.bypy"
    cmd = f"bypy --config-dir {config_dir} downfile /genome/scyc.fa ./"
    subprocess.check_call(cmd, shell=True)

@main.command()
def test_data():
    root_dir = f"{os.path.dirname(metaG.__file__)}"
    config_dir = f"{root_dir}/configs/.bypy"
    cmd = f"bypy --config-dir {config_dir} syncdown /test_data/ ./raws/"
    subprocess.check_call(cmd, shell=True)
    # make rawdata_tabel
    names = {"test_1":"sub1", "test_2":"sub2", "test_3":"sub3"}
    with open("./rawdata_table.tsv", "w") as fd:
        for k, v in names.items():
            r1_path = os.path.abspath(f"./raws/{v}_R1.fastq.gz")
            r2_path = os.path.abspath(f"./raws/{v}_R2.fastq.gz")
            fd.write(f"{k}\t{r1_path}\t{r2_path}\n")

