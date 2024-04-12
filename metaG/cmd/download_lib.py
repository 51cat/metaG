import metaG
import os
def main():
    root_dir = f"{os.path.dirname(metaG.__file__)}"
    config_dir = f"{root_dir}/configs/.bypy"
    lib_dir = f"{root_dir}/lib/"
    if not os.path.exists:
        os.system(f"mkdir {lib_dir}")
    cmd = f"bypy syncdown --config-dir {config_dir}  / {lib_dir}"
    print(cmd)

