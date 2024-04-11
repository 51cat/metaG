from os.path import join, dirname

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
        metaG_genome=metaG.genome:main
        
        get_config=metaG.cmd.get_config:main
        metaG_run=metaG.cmd.metaG_run:main
    """
)