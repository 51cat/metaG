# 宏基因组流程开发

```
Python 3.10
```

# 安装步骤

1. clone仓库

```
git clone https://github.com/51cat/metaG.git
```

3. 安装

```
cd ./metaG
bash scripts/build.sh
```

# 测试运行

```
metaG pre-process \
   --rawdata_table raw_file.tsv\
   --host human \
   --outdir ./out/
```

# 输入格式

raw_file.tsv:
```
PM_1	/home/issas/dev/meta_genome/test/fqs/sub1_R1.fastq.gz	/home/issas/dev/meta_genome/test/fqs/sub1_R2.fastq.gz
PM_2	/home/issas/dev/meta_genome/test/fqs/sub2_R1.fastq.gz	/home/issas/dev/meta_genome/test/fqs/sub2_R2.fastq.gz
PM_3	/home/issas/dev/meta_genome/test/fqs/sub3_R1.fastq.gz	//home/issas/dev/meta_genome/test/fqs/sub3_R2.fastq.gz
```