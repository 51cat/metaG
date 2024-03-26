import click
from metaG.common.preprocessor import DataPreProcessor

@click.group()
def main():
    pass

@main.command()
@click.option('--rawdata_table', default='', required=True)
@click.option('--host', default='', required=True)
@click.option('--host_genome', default = None)
@click.option('--outdir', default='', required=True)
def pre_process(rawdata_table, host, host_genome, outdir):
    runner = DataPreProcessor(
        fq_files_table=rawdata_table,
        host=host,
        host_genome_fa=host_genome,
        outdir=outdir
    )
    runner.run_preprocessor()


if __name__ == '__main__':
    main()