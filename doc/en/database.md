# Database Construction

## Host Database Construction

Building quality control step `--host` analysis parameters using host index.

Using `hostdb` to operate on the host database:

**View the database:**

```shell
hostdb ls
```

**Build the database**

Using Japanese rice as an example:

1. Switch to any other directory.

2. Download the Japanese rice genome, which will be automatically downloaded to the current directory with the filename `JP_rice_genomic.fna`.

```shell
m_download jp-rice
```

3. Build the host database.

`--fa`: Path to the host fasta file.

`--prfx`: Name of the database being built.

```shell
hostdb make --fa ./JP_rice_genomic.fna --prfx JP_rice 
```

4. Check if the construction was successful.

```shell
hostdb ls 
# Output
# Database path: /home/issas/dev/metaG/metaG/lib/host_database/
# Database name	size 
#	JP_rice	0.97 G
# Total: 0.97 G
```

Delete the database:

`--db_name`: Name of the database, corresponding to `mk_hostdb ls`.

```
hostdb clean --db_name JP_rice
```

## Gene Annotation Database Construction

Building annotation step `--database` analysis parameters using index.

Using `anndb` to operate on the annotation database:

**View the database:**

```shell
anndb ls
```

**Build the database**

Using sulfur cycle genes as an example:

1. Switch to any other directory.

2. Download the sulfur cycle gene database, which will be automatically downloaded to the current directory with the filename `scyc.fa`.

```shell
m_download scyc
```

3. Build the gene annotation database.

`--fa`: Path to the gene fasta file.

`--prfx`: Name of the database being built.

```shell
anndb make --fa ./scyc.fa --prfx SCYC
```

4. Check if the construction was successful.

```shell
anndb ls 
# Output
# Database path: /home/issas/dev/metaG/metaG/lib/database/DIAMOND/
# Database name	size 
#	Scyc	0.2 G
# Total: 0.2 G
```

Delete the database:

`--db_name`: Name of the database, corresponding to `mk_hostdb ls`.

```shell
anndb clean --db_name SCYS
```