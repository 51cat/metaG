## 使用方法1：运行全部分析步骤

1. 新建分析目录

   ```shell
   mkdir ./test_run/ && cd ./test_run
   ```

2. 运行下面的命令

   ```
   genome_run --rawdata_table /path/to/raw_file.tsv --host human --parallel
   ```

3. 会自动在当前的目录下生成下面的文件

   ```shell
   configs.yaml           # 配置文件
   data/			       # 运行所需数据的存放目录
   out/                   # 分析结果目录
   run_metaG_genome.sh    # 分析脚本
   ```

4. 运行分析脚本

   ```shell
   bash run_metaG_genome.sh 
   ```

## 使用方法2：分步骤运行

**所有步骤如下：**

- pre_process
- assembly
- predict
- ann
- count

通过`--step`控制运行的步骤，例如运行质控和assembly步骤

1. 新建分析目录

   ```
   mkdir ./test_run2/ && cd ./test_run2
   ```

2. 运行下面的命令

   ```
   genome_run --rawdata_table /home/issas/dev/metaG/data/raw_file.list --host human --step pre_process --parallel
   ```

3. 会自动生成相应的文件

4. 运行分析脚本

   ```
   bash run_metaG_genome.sh 
   ```

**分步运行每个步骤需要的参数稍有不同运行以下命令查看需要的参数信息**

```shell
metaG_genome pre-process --help
metaG_genome assembly --help
metaG_genome predict --help
metaG_genome ann --help
metaG_genome count --help
```

## 参数说明

**必须参数**

`--rawdata_table`: 测序数据表格，第一列是样本名称，第二三列是reads的路径,***\*必须使用绝对路径\****

格式:

```
s_1  /path/to/sub1_R1.fastq.gz  /path/to/sub1_R2.fastq.gz
s_2  /path/to/sub2_R1.fastq.gz  /path/to/sub2_R2.fastq.gz
s_3  /path/to/sub3_R1.fastq.gz  /path/to//sub3_R2.fastq.gz
```

`--host`: 宿主名称,  自带human, 如果自己提供宿主则需要同时提供`--host_genome`参数传递基因组路径

**其他参数**

`--outdir`: 结果输出目录，默认：`./out`

`--steps`: 需要运行的分析步骤, 默认：`all` 

`--configfile`: 配置文件路径，默认：`./configs.yaml`

`--parallel`: 是否开启多样本并行

- 数据质控相关参数

​`--host_genome`: 宿主基因组序列路径 , 如果自己提供宿主则需要此参数传递基因组路径

- assembly相关参数

​`--min_contig_len`: contig的最小长度，默认: `500`

- predict相关参数

​`--word_size`: 两两序列进行序列比对时选择的 word size, 默认：`9`

​`--identity_threshold`: 聚类相似度阈值，默认：`0.95`

​`--shorter_coverage`: 短序列覆盖度阈值，默认：`0.9`

​`--translate_table`: 核酸序列转换为蛋白序列使用的转换表编号，默认`11`

- 注释相关参数

`--database_use`: 注释使用的数据库名称，多个数据库使用冒号分隔，默认使用所有自带的数据库进行注释

`--min_evalue`: e-value阈值，默认`0.00001`

`--min_identity`: identity阈值，默认`80`

`--max_target_seqs`: 每条基因最大的预测结果数，默认`10`

