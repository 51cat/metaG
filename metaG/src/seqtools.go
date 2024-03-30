package main

import (
	"flag"
	"os"
	"bufio"
	"strings"
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

	if method == "len" {
		Lenfa(fa, outfile)
	}

}


func getfascaner(f *os.File, path string, format string) (*bufio.Scanner, int, int) {
	var scanner *bufio.Scanner
	var k int
	var seq_line int

	if (strings.HasSuffix(path, ".gz")) {
		gz, err := gzip.NewReader(f)
		
		if err != nil {
			panic("Error Path " + path)
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
		panic("Error Path " + fa_path)
	}
	
	f_out, err := os.OpenFile(outfile, os.O_WRONLY|os.O_CREATE, 0666)
	write := bufio.NewWriter(f_out)

	if err != nil {
		panic("Error Path " + outfile)
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

func Lenfa(fa_path string, outfile string) {
	len_map := make(map[string]string)
	var line int
	var seq_name string
	var seq_len string
	var _slice []string
	
	fa_in, err := os.Open(fa_path)
	if err != nil {
		panic("Error Path " + fa_path)
	}
	len_out, err := os.OpenFile(outfile, os.O_WRONLY|os.O_CREATE, 0666)
	if err != nil {
		panic("Error Path " + outfile)
	}
	defer fa_in.Close()
	defer len_out.Close()

	fa_scanner, _, _ := getfascaner(fa_in, fa_path, "fasta")
	write := bufio.NewWriter(len_out)
	

	for fa_scanner.Scan() {
		line++ 
		if line % 2 == 1 {
			seq_name = strings.Replace(fa_scanner.Text(), ">", "", 1)
			_slice = append(_slice, seq_name)
		}else {
			seq_len = strconv.Itoa(len(fa_scanner.Text()))
		}
		len_map[seq_name] = seq_len
	}
	// write 
	fmt.Fprintf(write, "seq_name\tseq_len\n")
	// fmt.Println(len_map)
	for _, name := range _slice {
		len_value := len_map[name]
		fmt.Fprintf(write, "%s\t%s\n", name, len_value)
		write.Flush()
	 }
	 write.Flush()
}

func MergeFa(fa_paths string, outfile string){

}