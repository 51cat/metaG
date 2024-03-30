import click
from metaG.common.preprocessor import DataPreProcessor
from metaG.assembly.run_assembly import Assembly
from metaG.utils import get_target_dir
from metaG.common.load_rawdata import DataLoader

@click.group()
def main():
    pass

@main.command()
@click.option('--rawdata_table', default='', required=True)
@click.option('--host', required=True)
@click.option('--host_genome', default = None)
@click.option('--outdir', default='', required=True)
@click.option('--config_file', required=False, default =None)
def pre_process(rawdata_table, host, host_genome, outdir, config_file):
    runner = DataPreProcessor(
        fq_files_table=rawdata_table,
        host=host,
        host_genome_fa=host_genome,
        outdir=outdir,
        config_file=config_file
        
    )
    runner.run_preprocessor()


@main.command()
@click.option('--fq_table', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--config_file', required=False, default =None)
@click.option('--min_contig_len', required=False, default =500)
def assembly(fq_table, outdir, config_file, min_contig_len):
    
    if fq_table is None:
        prep_dir = get_target_dir(outdir, "prep")
        fq_json = f"{prep_dir}/clean_data.json"
    else:
        loadder = DataLoader(fq_table, outdir)
        fq_json = loadder.get_rawdata_json_path()
    
    runner = Assembly(
        fq_json=fq_json,
        outdir=outdir,
        min_contig_len=min_contig_len,
        config_file=config_file
    )
    runner.run_assembly()



if __name__ == '__main__':
    main()