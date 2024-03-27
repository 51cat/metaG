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
        metaG=metaG.metaG_start:main
    """
)