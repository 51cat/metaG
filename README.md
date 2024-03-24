# 宏基因组流程开发

# 结构说明

`data/`: 存放一些必要的数据, 例如某些软件需要的必须数据以及数据库等

`metaG/`: 源码目录

`scripts/` 存放一些小脚本小工具性质

`test/`: 测试目录， 包含测试代码和测试数据

`metaG/common`: 公共模块存放位置

`metaG/indexhost`: 宿主构建索引模块

`metaG/QC`: QC模块

`metaG/assembly`: assembly模块

`metaG/software`: 所有的第三方软件的调用模块

`metaG/tools`: 工具模块

`metaG/utils.py`: 可复用的函数

# 部署
pip install -e .