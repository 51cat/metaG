package main

import (
	"flag"
	"os"
	"bufio"
	"strings"
	"log"
	"compress/gzip"
	"strconv"
	"fmt"
)

func main() {

	var fa string
	var fas string
	var method string
	var target_name string
	var outfile string

	flag.StringVar(&fa, "fa", "", "Input Your fastq path")
	flag.StringVar(&fas, "fas", "", "Input Your probe fasta path")
	flag.StringVar(&method, "method", "", "Input Your fastq path")
	flag.StringVar(&target_name, "target_name", "", "Input Your fastq path")
	flag.StringVar(&outfile, "outfile", "test", "Input sample name(prefix of ouput file)")
	flag.Parse()

	if method == "rename" {
		RenameFa(fa, outfile, target_name)
		return
	}

	if method == "merge" {
		MergeFa(fas ,outfile)
	}

}


func getfascaner(f *os.File, path string, format string) (*bufio.Scanner, int, int) {
	var scanner *bufio.Scanner
	var k int
	var seq_line int

	if (strings.HasSuffix(path, ".gz")) {
		gz, err := gzip.NewReader(f)
		
		if err != nil {
			log.SetPrefix("[ERROR] ")
			log.SetFlags(log.Ldate | log.Lmicroseconds)
			log.Fatalln("Error Path: ", path)
		}
		
		scanner = bufio.NewScanner(gz)
	}else {
		scanner = bufio.NewScanner(f)
	}
    
	if format == "fastq" {
		k = 4
		seq_line = 2
	}
	if format == "fasta" {
		k = 2
		seq_line = 0
	}

	return scanner, k, seq_line
}

func RenameFa(fa_path string, outfile string, target string){

	var line int
	var inx int
	var new_name string

	f_in, err := os.Open(fa_path)
	
	if err != nil {
		log.SetPrefix("[ERROR] ")
		log.SetFlags(log.Ldate | log.Lmicroseconds)
		log.Fatalln("Error Path: ", fa_path)
	}
	
	f_out, err := os.OpenFile(outfile, os.O_WRONLY|os.O_CREATE, 0666)
	write := bufio.NewWriter(f_out)

	if err != nil {
		log.SetPrefix("[ERROR] ")
		log.SetFlags(log.Ldate | log.Lmicroseconds)
		log.Fatalln("Error Path: ", fa_path)
	}

	defer f_in.Close()
	defer f_out.Close()

	fa_scanner, _, _ := getfascaner(f_in, fa_path, "fasta")

	for fa_scanner.Scan() {
		line++
		if line % 2 == 1 {
			inx++
			new_name = ">" + target + "_" + strconv.Itoa(inx)
			fmt.Fprintf(write, "%s\n", new_name)
			write.Flush()
		}else {

			fmt.Fprintf(write, "%s\n", fa_scanner.Text())
			write.Flush()
		}
		write.Flush()
	}

}

func MergeFa(fa_paths string, outfile string){

}