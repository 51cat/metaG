def seqtools_run(out_file, do, target_name = None, in_fa= None, fa_lst = None):
    import metaG
    moduledir = os.path.dirname(metaG.__file__)
    path = os.path.abspath(f'{moduledir}/src/seqtools')        
    
    cmd_basic = (
         f"{path} "
         f"--outfile {out_file} "
    )

    if do == "rename":
        cmd_basic += f" --fa {in_fa} "
        cmd_basic += f" --target_name {target_name} "
        cmd_basic += f" --method {do} "
    
    if do == "merge":
        fas = "::".join(fa_lst)
        cmd_basic += f" --fas {fas} "
        cmd_basic += f" --method {do} "

    if do in ["len", "format"]:
        cmd_basic += f" --fa {in_fa} "
        cmd_basic += f" --method {do} "
    subprocess.check_call(cmd_basic, shell=True)

def get_fa_stat(stat_file_out, fa_lst):
    import metaG
    seqkit_exec = f"{os.path.dirname(metaG.__file__)}/lib/softs/seqkit/seqkit"
    files = " ".join(fa_lst)
    cmd = f"{seqkit_exec} stat {files} -b -a > {stat_file_out}"
    subprocess.check_call(cmd, shell=True)
