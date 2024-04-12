from setuptools import setup
import setuptools

setup(
    name="metaG",
    version='0.1',
    description='',
    url='',
    packages=setuptools.find_packages(),
    keywords=['keyword'],
    install_requires=[
    
    ],
    python_requires=">=3",
    entry_points="""
        [console_scripts]
        metaG_genome=metaG.genome.start:main

        mk_anndb=metaG.cmd.mk_anndb:main
        mk_hostdb=metaG.cmd.mk_hostdb:main
        m_download=metaG.cmd.download:main
        
        get_config=metaG.cmd.get_config:main
        genome_run=metaG.cmd.genome_run:main
    """
)