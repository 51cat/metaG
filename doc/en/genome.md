## Usage Method 1: Run All Analysis Steps

1. Create an analysis directory.

   ```shell
   mkdir ./test_run/ && cd ./test_run
   ```

2. Run the following command.

   ```
   genome_run --rawdata_table /path/to/raw_file.tsv --host human --parallel
   ```

3. This will automatically generate the following files in the current directory.

   ```shell
   configs.yaml           # Configuration file
   data/			       # Directory for storing required data
   out/                   # Directory for storing analysis results
   run_metaG_genome.sh    # Analysis script
   ```

4. Run the analysis script.

   ```shell
   bash run_metaG_genome.sh 
   ```

## Usage Method 2: Step-by-Step Execution

**All steps are as follows:**

- pre_process
- assembly
- predict
- ann
- count

Control the execution steps through `--step`. For example, run the quality control and assembly steps:

1. Create an analysis directory.

   ```
   mkdir ./test_run2/ && cd ./test_run2
   ```

2. Run the following command.

   ```
   genome_run --rawdata_table /home/issas/dev/metaG/data/raw_file.list --host human --step pre_process --parallel
   ```

3. This will automatically generate corresponding files.

4. Run the analysis script.

   ```
   bash run_metaG_genome.sh 
   ```

**Running each step separately requires slightly different parameters. Run the following commands to see the required parameter information.**

```shell
metaG_genome pre-process --help
metaG_genome assembly --help
metaG_genome predict --help
metaG_genome ann --help
metaG_genome count --help
```

## Parameter Explanation

**Required Parameters**

`--rawdata_table`: Sequencing data table, where the first column is the sample name, and the second and third columns are the paths to the reads. ***\*Absolute paths must be used\****

Format:

```
s_1  /path/to/sub1_R1.fastq.gz  /path/to/sub1_R2.fastq.gz
s_2  /path/to/sub2_R1.fastq.gz  /path/to/sub2_R2.fastq.gz
s_3  /path/to/sub3_R1.fastq.gz  /path/to//sub3_R2.fastq.gz
```

`--host`: Host name, pre-set with 'human'. If providing a custom host, the `--host_genome` parameter is also required to pass the path to the host genome.

**Other Parameters**

`--outdir`: Output directory for results, default: `./out`

`--steps`: Analysis steps to be executed, default: `all`

`--configfile`: Path to the configuration file, default: `./configs.yaml`

`--parallel`: Whether to enable parallel processing for multiple samples

- Parameters related to data quality control

`--host_genome`: Path to the host genome sequence. If providing a custom host, this parameter is required to pass the genome path.

- Parameters related to assembly

`--min_contig_len`: Minimum length of contigs, default: `500`

- Parameters related to prediction

`--word_size`: Word size used for sequence alignment, default: `9`

`--identity_threshold`: Clustering similarity threshold, default: `0.95`

`--shorter_coverage`: Short sequence coverage threshold, default: `0.9`

`--translate_table`: Translation table number used for translating nucleotide sequences to protein sequences, default `11`

- Parameters related to annotation

`--database_use`: Names of databases used for annotation. Multiple databases are separated by colons. Default is to use all built-in databases for annotation.

`--min_evalue`: E-value threshold, default `0.00001`

`--min_identity`: Identity threshold, default `80`

`--max_target_seqs`: Maximum number of predicted results per gene, default `10`