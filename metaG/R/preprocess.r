pre_process <- function(
    raw.data.file,
    host = "",
    outdir = ""
) {

    cmd = stringr::str_glue(
        "metaG pre-process --rawdata_table {raw.data.file} --host {host} --outdir {outdir}"
    )
    system(cmd, intern=FALSE, wait=TRUE)

}