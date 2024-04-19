# Analysis of Test Data

1. Create a new analysis directory.

```shell
mkdir demo && cd demo
```

2. Download the test data.

```shell
m_download test-data
```

3. View the current directory.

```shell
ls -l
# Generates the following two files
#rawdata_table.tsv
#raws/
```

4. Input the analysis command to automatically generate the analysis script.

```shell
genome_run --rawdata_table ./rawdata_table.tsv --host JP_rice --parallel
```

5. This will automatically generate the following files in the current directory.

```shell
configs.yaml           # Configuration file
data/			      # Directory for storing required data
out/                   # Directory for storing analysis results
run_metaG_genome.sh    # Analysis script
```

6. Run the analysis script.

```shell
bash run_metaG_genome.sh 
```