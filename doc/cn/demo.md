# 测试数据分析

1. 新建分析目录

```shell
mkdir demo && cd demo
```

2. 下载测试数据

```shell
m_download test-data
```

3. 查看当前目录

```shell
ls -l
# 生成下面两个文件
#rawdata_table.tsv
#raws/
```

4. 输入分析命令自动生成分析脚本

```shell
genome_run --rawdata_table ./rawdata_table.tsv --host JP_rice --parallel
```

5. 会自动在当前的目录下生成下面的文件

```shell
configs.yaml           # 配置文件
data/			      # 运行所需数据的存放目录
out/                   # 分析结果存放目录
run_metaG_genome.sh    # 分析脚本
```

4. 运行分析脚本

```shell
bash run_metaG_genome.sh 
```