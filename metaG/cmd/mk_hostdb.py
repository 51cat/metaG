import click
import metaG
import os
import subprocess
from metaG.core.log import add_log

DBDIR = f"{os.path.dirname(metaG.__file__)}/lib/host_database/"
BWA_PATH = f"{os.path.dirname(metaG.__file__)}/lib/softs/bwa/bwa"

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return round(total_size / (1024 * 1024 * 1024), 2)

@click.group()
def main():
    pass

@click.group()
def main():
    pass

@main.command()
def ls():
    print(f"Database path: {DBDIR}")
    print(f"Database name\tsize ")
    if not os.path.exists(DBDIR):
        print("Not Found database dir! plaease use mk_anndb make to create databse dir")
        return
    dirnames = os.listdir(DBDIR)
    if len(dirnames) == 0:
        print("Not Found database dir! plaease use mk_anndb make to create databse dir")
        return
    
    total = 0
    for db_name in dirnames:
        size = get_directory_size(f'{DBDIR}/{db_name}')
        print(f"\t{db_name}\t{size} G")
        total+=size
    print(f"Total: {round(total,2)} G")
    

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
