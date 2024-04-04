package main

import (
	"flag"
	"os"
	"bufio"
	"strings"
	"compress/gzip"
	"strconv"
	"fmt"
	"bytes"
)

func main() {

	var fa string
	var fas string
	var method string
	var target_name string
	var outfile string
	//var buffer bytes.Buffer

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

	if method == "format" {
		Format(fa, outfile)
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
	var buffer bytes.Buffer
	buffer.Truncate(0)

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
	var buffer bytes.Buffer
	buffer.Truncate(0)
	
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
	var buffer bytes.Buffer
	buffer.Truncate(0)

	file, _ := os.OpenFile(outfile, os.O_WRONLY|os.O_CREATE, 0666)
	defer file.Close()
	write := bufio.NewWriter(file)

	for _, path := range strings.Split(fa_paths,  "::"){
		f, err := os.Open(path)
		
		if err != nil {
			panic("Error Path " + path)
		}

		fq_scaner, _, _ := getfascaner(f, path, "fasta")

		for fq_scaner.Scan() {
			fmt.Fprintf(write,"%s\n",fq_scaner.Text())
			write.Flush()
		}
		write.Flush()
	}
	write.Flush()

}

func writeRes(res map[string][]string, outfile string, names []string) {
	var buffer bytes.Buffer
	buffer.Truncate(0)
	file, _ := os.OpenFile(outfile, os.O_WRONLY|os.O_CREATE, 0666)
	//CheckError(err)
	defer file.Close()
	write := bufio.NewWriter(file)

	for _, k := range names {
		vv := strings.Join(res[k], "")
		s := fmt.Sprintf("%s\n%s\n",k, vv)
		fmt.Fprintf(write,s)
		write.Flush()
	}
	write.Flush()
}

func Format(fa_path string, outfile string){
	var seqs string
	var name string
	var names []string
	outs := make(map[string][]string)

	f, err := os.Open(fa_path)
	if err != nil {
		panic("Error Path " + outfile)
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		record := scanner.Text()
		if strings.HasPrefix(record, ">") {
			name = record
			names = append(names, name)
		}else {
			seqs = strings.ReplaceAll(record, "\n", "")
			outs[name] = append(outs[name], seqs)
		}
	}
	writeRes(outs, outfile, names)
}

	

