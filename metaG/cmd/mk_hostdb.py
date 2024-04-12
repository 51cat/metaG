import click
import metaG
import os
import subprocess
from metaG.core.log import add_log

DBDIR = f"{os.path.dirname(metaG.__file__)}/lib/host_database/"
BWA_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/bwa/bwa"

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
    from metaG.softs.bwa import BWA
    import glob
    
    runner = BWA(
        host=prfx,
        fa=fa,
        mode = "index"
    )
    runner.run()
    # 写入数据库
    print(f"Write {prfx} to {DBDIR} ")
    
    new_host_path = f"{DBDIR}/{prfx}/"
    subprocess.check_call(f"mkdir -p {new_host_path}", shell=True)
    index_files = glob.glob(f"{prfx}*[fa,amd,ann,bwt,pac,sa]")
    
    mv_to_database_cmds = [f"mv {os.path.abspath(file)} {new_host_path}"
                for file in index_files]
    
    for cmd in mv_to_database_cmds:
        subprocess.check_call(cmd, shell=True)
    print(f"Finish!")

@main.command()
@click.option('--db_name', default = None)
def clean(db_name):
    cmd = f"rm -rf {DBDIR}/{db_name}"
    subprocess.check_call(cmd, shell=True)
