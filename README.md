# 宏基因组流程开发

```
Python 3.10
```

# 安装步骤

1. 创建conda环境

```
conda create -n my_cenv python=3.10
```

1. clone仓库

```
git clone git@github.com:51cat/metaG.git
or
git clone https://github.com/51cat/metaG.git

cd ./metaG
```

2. 安装必要的库

```
conda install --file ./conda_pkgs.txt
pip install -r ./requirement.txt 
```

3. 安装软件所需数据库(后期会直接挂在阿里云上面可以简单快速下载)

```
cp /home/issas/dev/meta_genome/metaG/lib ./metaG/
```

4. 安装metaG

```
pip install -e .
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