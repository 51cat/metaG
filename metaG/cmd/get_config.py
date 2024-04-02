import metaG
import os
def get_config():
    file = f"{os.path.dirname(metaG.__file__)}/configs/configs.yaml"
    os.system(f"cp -a {file} ./")

def main():
    get_config()