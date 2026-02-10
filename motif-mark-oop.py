#!/usr/bin/env python

#adding imports
import cairo
import argparse

#adding argparse statements
def get_args():
    '''these are the arguments that will be parsed in for this python script'''
    parser = argparse.ArgumentParser(description="Getting the input and output arguments for the motif-mark script")
    
    parser.add_argument("-f", help="The absolute path to the input FASTA file", required=True)
    parser.add_argument("-m", help="The absolute path to the input motif file (a txt file with one motif on each line)", required=True)
    
    return parser.parse_args()

#calling the get_args function to get the arguments
args=get_args()

#reassiging args.f filename as f
f:str = args.f
#reassiging args.m filename as m
m:str = args.m


def oneline_fasta(input_file:str, output_file:str):
    '''takes a FASTA file with multiple sequence lines per record
    and converts each record into 2 lines (header and one sequence)'''
    #writting a new file named the output file
    with open(output_file, "w") as f:
        #opening the reading FASTA file!
        with open(input_file, "r") as fh:
            #initalizing an empty string to hold the sequences
            seq_line = ''
            #reading through the lines in the file
            for line in fh:
                #runs only when at a header
                if ">" in line:
                    #this is for the first line case when sequence is
                    #empty but I need the first header
                    if seq_line == '':
                        #writting the first header
                        f.write(line)
                    #this is for when we reach the next header
                    else:
                        #writting the sequence!
                        f.write(f"{seq_line}\n")
                        #emptying the sequence holder
                        seq_line = ''
                        #writting the next header
                        f.write(line)
                #runs when at sequence line
                else:
                    #adds the line to the string to make sequence one line
                    line = line.strip("\n")
                    seq_line += line
            #the last case to write the last sequence
            f.write(seq_line)
