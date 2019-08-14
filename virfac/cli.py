# -*- coding: utf-8 -*-

"""Console script for virfac."""
import sys
import click

# Heng Li's FASTQ reader, faster than Biopython
# https://github.com/lh3/readfq/blob/master/readfq.py
def readfq(fp): # this is a generator function
    last = None # this is a buffer keeping the last unprocessed line
    while True: # mimic closure; is it a bad idea?
        if not last: # the first record or a record following a fastq
            for l in fp: # search for the start of the next record
                if l[0] in '>@': # fasta/q header line
                    last = l[:-1] # save this line
                    break
        if not last: break
        name, seqs, last = last[1:].partition(" ")[0], [], None
        for l in fp: # read the sequence
            if l[0] in '@+>':
                last = l[:-1]
                break
            seqs.append(l[:-1])
        if not last or last[0] != '+': # this is a fasta record
            yield name, ''.join(seqs), None # yield a fasta record
            if not last: break
        else: # this is a fastq record
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp: # read the quality
                seqs.append(l[:-1])
                leng += len(l) - 1
                if leng >= len(seq): # have read enough quality
                    last = None
                    yield name, seq, ''.join(seqs); # yield a fastq record
                    break
            if last: # reach EOF before reading enough quality
                yield name, seq, None # yield a fasta record instead
                break

# class FastqInputFileType(click.FileType):
#     name = "fastq"
#     def convert(self, value, param, ctx):
#         import gzip
        

@click.group()
def main(args=None):
    pass

@main.command('get-data')
def run_get_data():
    import get_data
    get_data.get_data_from_ncbi(get_data.bad_bugs, "pathogens")
    get_data.get_data_from_ncbi(get_data.good_bugs, "commesurals")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
