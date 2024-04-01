conda create -n my_cenv python=3.10
souce activate my_cenv

conda install --file ./conda_pkgs.txt
pip install -r ./requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

cp /home/issas/dev/meta_genome/metaG/lib ./metaG/
pip install -e .