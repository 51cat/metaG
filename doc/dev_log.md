# 2024-03-24

## 工作时长

3.5 天 预计

## 概述
1. 开发环境构建(metaG_dev2)，流程梳理
2. 软件流程框架开发(见README.md)
3. 索引构建分析模块开发, 支持所有物种的index构建，目前只支持单一物种的index
4. 新物种构建过后, 会把相应的index写入数据库, 下次运行直接指定host名无需重新构建
5. 增加命令行接口
6. 原始数据读入模块

## 测试代码
/home/issas/dev/meta_genome/test/test_index/

## 测试

```shell
cd /home/issas/dev/meta_genome/test/test_index/
python test_index.py
```


## 输出目录结构

```
test_host_index/
└── 01.prep
    └── ref_index
        ├── rice3.fa
        ├── rice3.fa.amb
        ├── rice3.fa.ann
        ├── rice3.fa.bwt
        ├── rice3.fa.pac
        └── rice3.fa.sa

```
