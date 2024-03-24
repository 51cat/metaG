from distutils.core import  setup

# 测试部署

setup(
    name = "metaG", 
    version = "1.0", 
    author = "liuzihao", 
    py_modules= [
        # common
        'metaG.common.log',
        'metaG.common.pre_check',

        # index
        'metaG.index.run_index',

        # QC
        'metaG.QC.run_qc',

        # software
        'metaG.software.interface',
        'metaG.software.bwa',
        'metaG.software.fastqc',
        'metaG.software.trimmomatic',
        'metaG.software.megahit',
        
        # utils
        'metaG.utils'

    ]
        )