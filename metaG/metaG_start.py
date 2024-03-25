import click
from metaG.indexhost.run_index import IndexHost
from metaG.QC.run_qc import QCfq

@click.group()
def main():
    pass

@main.command()
@click.option('--fq_files', default='', required=True)
def start_all_analysis(fq_files):
    print(fq_files)

@main.command()
@click.option('--host', default='', required=True)
@click.option('--fa', default = None)
@click.option('--outdir', default='', required=True)
def hostindex(host, fa, outdir):
    runner = IndexHost(
        host=host,
        fa=fa,
        outdir=outdir
    )
    runner.run()

@main.command()
def QC():
    runner = QCfq(
        
    )
    runner.run()

if __name__ == '__main__':
    main()