import click
from metaG.common.preprocessor import DataPreProcessor
from metaG.assembly.run_assembly import Assembly
from metaG.predict.run_predict import GenePredicter
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
@click.option('--rawdata_table', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--config_file', required=False, default =None)
@click.option('--min_contig_len', required=False, default =500)
def assembly(rawdata_table, outdir, config_file, min_contig_len):
    
    if rawdata_table is None:
        prep_dir = get_target_dir(outdir, "prep")
        fq_json = f"{prep_dir}/clean_data.json"
    else:
        loadder = DataLoader(rawdata_table, outdir)
        loadder.run()
        fq_json = loadder.get_rawdata_json_path()
    
    runner = Assembly(
        fq_json=fq_json,
        outdir=outdir,
        min_contig_len=min_contig_len,
        config_file=config_file
    )
    runner.run_assembly()


@main.command()
@click.option('--rawdata_table', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--config_file', required=False, default =None)
@click.option('--use', required=False, default ="prodigal")
# unique gene args
@click.option('--word_size', default=9, required=False)
@click.option('--identity_threshold', required=False, default =0.95)
@click.option('--shorter_coverage', required=False, default =0.9)
def predict_gene(rawdata_table, outdir, config_file, use,word_size, identity_threshold, shorter_coverage):
    
    if rawdata_table is None:
        prep_dir = get_target_dir(outdir, "assembly")
        contig_json = f"{prep_dir}/clean_contig.json"
    else:
        loadder = DataLoader(rawdata_table, outdir, mode=2)
        loadder.run()
        contig_json = loadder.get_rawdata_json_path()
    
    runner = GenePredicter(
        contig_json=contig_json,
        outdir=outdir,
        use=use,
        config_file=config_file,
        word_size=word_size,
        identity_threshold=identity_threshold,
        shorter_coverage=shorter_coverage
    )
    runner.run_predict()

if __name__ == '__main__':
    main()