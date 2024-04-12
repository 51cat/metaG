import click
from metaG.tools.preprocess import DataPreProcessor
from metaG.genome.genome_assembly import GenomeAssembly
from metaG.genome.genome_predict import GenomoPredict
from metaG.genome.genome_annotation import GenomeAnnotation
from metaG.genome.genome_count import GenomoCount
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

@main.command()
@click.option('--rawdata_table', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--predict_use', required=False, default ="prodigal")
@click.option('--word_size', required=False, default =9)
@click.option('--identity_threshold', required=False, default =0.95)
@click.option('--shorter_coverage', required=False, default =0.9)
@click.option('--translate_table', required=False, default =11)
@click.option('--config_file', required=False, default =None)
@click.option('--parallel', required=False, is_flag=True)
def predict(rawdata_table, outdir, predict_use, word_size,
            identity_threshold,translate_table,shorter_coverage,config_file,parallel):
    
    if rawdata_table is None:
        assembly_dir = get_target_dir(outdir, "assembly")
        clean_contig_json = f"{assembly_dir}/clean_contig.json"
    else:
        loadder = DataLoader(rawdata_table, outdir,mode=2)
        loadder.run()
        clean_contig_json = loadder.rawdata_json   
    
    runner = GenomoPredict(
       contig_json=clean_contig_json,
        predict_use = predict_use,
        outdir= outdir ,
        word_size = word_size,
        identity_threshold = identity_threshold,
        shorter_coverage = shorter_coverage,
        config_file = config_file,
        table_code=translate_table,
        parallel = parallel
    )
    runner.start()


@main.command()
@click.option('--query_fa', default=None, required=False)
@click.option('--uniq_gene_fa', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--database_use', required=True, default =None)
@click.option('--annota_use', required=False, default ='diamond')
@click.option('--method', required=False, default ='blastp')
@click.option('--min_evalue', required=False, default =0.00001)
@click.option('--min_identity', required=False, default =80)
@click.option('--format', required=False, default =6)
@click.option('--max_target_seqs', required=False, default =10)
@click.option('--block_size', required=False, default =8)
@click.option('--config_file', required=False, default =None)
@click.option('--parallel', required=False, is_flag=True)
def ann(query_fa, uniq_gene_fa, outdir, database_use, annota_use,
            method,min_evalue,min_identity,format,max_target_seqs,
            block_size,config_file,parallel):
    
    if query_fa is None:
        predict_dir = get_target_dir(outdir, "predict")
        uniq_fa_protein = f"{predict_dir}/GeneSet_unique_protein.fa"
        uniq_gene_fa = f"{predict_dir}/GeneSet_unique.fa"
    else:
        uniq_fa_protein = query_fa
        uniq_gene_fa = uniq_gene_fa
    
    runner = GenomeAnnotation(
            uniq_fa_protein= uniq_fa_protein,
            uniq_fa = uniq_gene_fa,
            outdir= outdir ,
            database_use=database_use,
            config_file = config_file,
            annota_use = annota_use,
            method = method,
            min_evalue= min_evalue,
            min_identity = min_identity,
            format = format,
            max_target_seqs = max_target_seqs,
            block_size = block_size,
            parallel = parallel
    )
    runner.start()

@main.command()
@click.option('--rawdata_table', default=None, required=False)
@click.option('--outdir', default='', required=True)
@click.option('--db_ann_dir', default=None, required=False)
@click.option('--genome_fa', required=False, default =None)
@click.option('--parallel', required=False, is_flag=True)
@click.option('--config_file', required=False, default =None)
def count(rawdata_table, outdir, db_ann_dir, genome_fa, parallel, config_file):
    if rawdata_table is None:
        prep_dir = get_target_dir(outdir, "prep")
        fq_json = f"{prep_dir}/clean_fastq.json"
    else:
        loadder = DataLoader(rawdata_table, outdir,mode=1)
        loadder.run()
        fq_json = loadder.rawdata_json   
    
    if db_ann_dir is None:
        ann_dir = get_target_dir(outdir, "annotation")
    else:
        ann_dir = db_ann_dir
    
    if genome_fa is None:
        predict_dir =  get_target_dir(outdir, "predict")
        genome_fa = f"{predict_dir}/GeneSet_unique.fa"

    runner = GenomoCount(
        fq_json = fq_json,
        ann_dir = ann_dir,
        outdir=outdir,
        genome_fa=genome_fa,
        parallel = parallel
    )
    runner.start()


if __name__ == '__main__':
    main()