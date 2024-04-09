import click
from metaG.tools.preprocess import DataPreProcessor
from metaG.genome.genome_assembly import GenomeAssembly
from metaG.core.dataload import DataLoader
from metaG.utils import get_target_dir

@click.group()
def main():
    pass

@main.command()
@click.option('--rawdata_table', default='', required=True)
@click.option('--host', required=True)
@click.option('--host_genome', default = None)
@click.option('--outdir', default='', required=True)
@click.option('--config_file', required=False, default =None)
@click.option('--qc_use', required=False, default ="trimmomatic")
@click.option('--host_remove_use', required=False, default ="bwa")
@click.option('--parallel', required=False, is_flag=True)
def pre_process(rawdata_table, host, host_genome, outdir, config_file, qc_use, host_remove_use, parallel):
    runner = DataPreProcessor(
        fq_files_table=rawdata_table,
        host=host,
        host_genome_fa=host_genome,
        outdir=outdir,
        config_file=config_file,
        qc_use = qc_use,
        host_remove_use = host_remove_use,
        parallel = parallel
        
    )
    runner.start()


@main.command()
@click.option('--rawdata_table', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--config_file', required=False, default =None)
@click.option('--min_contig_len', required=False, default =500)
@click.option('--assembly_use', required=False, default ="MEGAHIT")
@click.option('--parallel', required=False, is_flag=True)
def assembly(rawdata_table, outdir, config_file, min_contig_len,assembly_use,parallel):
    
    if rawdata_table is None:
        prep_dir = get_target_dir(outdir, "prep")
        fq_json = f"{prep_dir}/clean_fastq.json"
    else:
        loadder = DataLoader(rawdata_table, outdir)
        loadder.run()
        fq_json = loadder.rawdata_json
    
    runner = GenomeAssembly(
        fq_json=fq_json,
        outdir=outdir,
        min_contig_len=min_contig_len,
        config_file=config_file,
        assembly_use=assembly_use,
        parallel=parallel
    )
    runner.start()

if __name__ == '__main__':
    main()