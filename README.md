# metaG宏基因组分析工具

## 安装

1. 克隆仓库

   ```shell
   git clone https://github.com/51cat/metaG.git
   ```

2. 安装软件

   ```shell
   cd ./metaG
   bash scripts/build.sh
   ```

3. 测试

   ```shell
   metaG --help
   ```

## 使用

**必须参数：**

`--rawdata_table`: 测序数据表格，第一列是样本名称，第二三列是reads的路径,**必须使用绝对路径**

格式:

```
PM_1	/path/to/sub1_R1.fastq.gz	/path/to/sub1_R2.fastq.gz
PM_2	/path/to/sub2_R1.fastq.gz	/path/to/sub2_R2.fastq.gz
PM_3	/path/to/sub3_R1.fastq.gz	/path/to//sub3_R2.fastq.gz
```

`--host`: 宿主名称,  自带human, 如果自己提供宿主则需要同时提供`--fa`参数传递基因组路径

**其他参数：**

`--outdir`: 结果输出目录，默认：`./out`

`--steps`: 需要运行的分析步骤, 默认：`all` 

`--fa`: 宿主基因组序列路径 , 如果自己提供宿主则需要此参数传递基因组路径

`--configfile`: 配置文件路径，默认：`./configs.yaml`

`--min_contig_len`: contig的最小长度，默认: `500`

`--use`: 基因预测方法，默认：`prodigal`

`--word_size`: 两两序列进行序列比对时选择的 word size, 默认：`9`

`--identity_threshold`: 聚类相似度阈值，默认：`0.95`

`--shorter_coverage`: 短序列覆盖度阈值，默认：`0.9`

#### 分析步骤

1. 新建分析目录

   ```shell
   mkdir ./test_run/ && cd ./test_run
   ```

2. 运行下面的命令

   ```
   metaG_run --rawdata_table raw_file.tsv --host human
   ```

3. 会自动在当前的目录下生成下面的文件

   ```shell
   configs.yaml     # 配置文件
   data/			 # 运行所需数据的存放目录
   out/             # 分析结果目录
   run_metaG.sh     # 分析脚本
   ```

4. 运行分析脚本

   ```shell
   bash run_metaG.sh 
   ```