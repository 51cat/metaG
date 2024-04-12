import click
import metaG
import os
import subprocess

DBDIR = f"{os.path.dirname(metaG.__file__)}/lib/database/DIAMOND/"
DIAMOND_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/DIAMOND/diamond"

@click.group()
def main():
    pass

@main.command()
def ls():
    print(f"Database path: {DBDIR}")
    print(f"Database name: ")
    for db_name in os.listdir(DBDIR):
        print(f"\t{db_name}")

@main.command()
@click.option('--fa', default = None)
@click.option('--prfx', default = None)
def make(fa, prfx):
    os.system(f"mkdir -p {DBDIR}/{prfx}")
    cmd = f"{DIAMOND_PATH} makedb --in {fa} -d {DBDIR}/{prfx}/{prfx}"
    subprocess.check_call(cmd, shell=True)

@main.command()
@click.option('--db_name', default = None)
def clean(db_name):
    cmd = f"rm -rf {DBDIR}/{db_name}"
    subprocess.check_call(cmd, shell=True)
