conda install -y ./conda_pkgs.txt
pip install -r ./requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -e .
m_download lib