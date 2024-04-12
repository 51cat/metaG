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
    softs_dir = f"{root_dir}/lib/softs/"
    if not os.path.exists:
        os.system(f"mkdir {lib_dir}")
    cmd = f"bypy --config-dir {config_dir} syncdown / {lib_dir}"
    cmd2 = f"chmod -R +x {softs_dir}"
    subprocess.check_call(cmd, shell=True)
    subprocess.check_call(cmd2, shell=True)

@main.command()
@click.option('--name', default = None)
def fa(name):
    pass