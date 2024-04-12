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
    adapters_dir = f"{root_dir}/lib/adapter/"
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