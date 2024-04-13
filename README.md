# metaG宏基因组分析工具

## 安装

1. 克隆仓库

   ```shell
   git clone https://github.com/51cat/metaG.git
   ```

2. 安装软件

   ```shell
   cd ./metaG
   conda create -n my_cenv python=3.10
   ```

3. 运行安装脚本(根据网速快慢: 大多消耗时间在30-60 min)
   ```
   conda activate my_cenv
   bash install.sh
   ```


## 数据库构建

### 宿主数据库构建

使用`hostdb_tk`操作宿主数据库：

**查看数据库：**

```shell
hostdb_tk ls
```

**构建数据库**

以Japanese rice为例

1. 切换到其他的任意目录

2. 下载Japanese rice基因组, 自动下载到当前目录, 文件名: `JP_rice_genomic.fna`
```shell
m_download jp-rice
```
3. 构建宿主数据库

`--fa`: 宿主fasta文件路径

`--prfx`: 构建的数据库名称

```shell
hostdb_tk make --fa ./JP_rice_genomic.fna --prfx JP_rice 
```
4. 查看构建是否成功
```shell
hostdb_tk ls 
# 输出
#Database path: /home/issas/dev/metaG/metaG/lib/host_database/
#Database name	size 
#	JP_rice	0.97 G
#Total: 0.97 G
```

删除数据库：

`--db_name`: 数据库名称，要与`mk_hostdb ls`相对应

```
hostdb_tk clean --db_name JP_rice
```

### 基因注释数据库构建

使用`anndb_tk`操作注释数据库：

**查看数据库：**

```shell
anndb_tk ls
```

**构建数据库**

以硫循环基因为例

1. 切换到其他的任意目录

2. 下载硫循环基因数据库, 自动下载到当前目录, 文件名: `scyc.fa`
```shell
m_download scyc
```
3. 构建基因注释数据库

`--fa`: 基因fasta文件路径

`--prfx`: 构建的数据库名称

```shell
anndb_tk make --fa ./scyc.fa --prfx SCYC
```

4. 查看构建是否成功
```shell
anndb_tk ls 
# 输出
#Database path: /home/issas/dev/metaG/metaG/lib/database/DIAMOND/
#Database name	size 
#	Scyc	0.2 G
#Total: 0.2 G
```

删除数据库：

`--db_name`: 数据库名称，要与`mk_hostdb ls`相对应

```shell
anndb_tk clean --db_name SCYS
```

## 使用
- [测试数据分析](./doc/demo.md)
- [宏基因组数据](./doc/genome.md)