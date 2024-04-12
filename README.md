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

3. 下载软件所需数据库

   输入以下命令等待下载:
   
   ```shell
   m_download lib
   ```

3. 测试

   ```shell
   genome_run --help 
   ```

## 数据库构建

### 宿主数据库构建

使用`mk_hostdb`操作宿主数据库：

**查看数据库：**

```shell
mk_hostdb ls
```

**构建数据库**

`--fa`: 宿主fasta文件路径

`--prfx`: 构建的数据库名称

```shell
mk_hostdb make --fa /path/to/human.fa --prfx human 
```

删除数据库：

`--db_name`: 数据库名称，要与`mk_hostdb ls`相对应

```
mk_hostdb clean --db_name human
```

### 基因注释数据库构建

使用`mk_anndb`操作注释数据库：

**查看数据库：**

```shell
mk_anndb ls
```

**构建数据库**

`--fa`:  fasta文件路径

`--prfx`: 构建的数据库名称

```shell
mk_anndb make --fa /path/to/nr.fa --prfx nr 
```

删除数据库：

`--db_name`: 数据库名称，要与`mk_anndb ls`相对应

```
mk_anndb clean --db_name nr
```

## 使用

- [宏基因组数据](./doc/genome.md)