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

## 使用
- [数据库构建](./doc/cn/database.md)
- [测试数据分析](./doc/cn/demo.md)
- [宏基因组数据](./doc/cn/genome.md)