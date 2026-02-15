#!/usr/bin/env python

#adding imports
import cairo
import argparse
import re

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

#making the input file FASTA have one line sequence
oneline_fasta(f, f"oneline_{f}")

#defining the classes ------------------------------------------------------------------------------------

class Sequence():
    #this class is for each sequence in a FASTA
    def __init__(self, length, exon_list, header):
        #this is the overall total length of the sequence
        self.length = length
        #this is a list that holds start and end values for each exon in the sequence
        #example of an exon 25bp long: [(25, 50)]
        #example of 2 exons in a sequence: [(10, 30), (80,95)]
        self.exon_list = exon_list
        #this is the header of the sequence from the FASTA
        self.header = header

class MotifFinder():
    #this class is for finding all of the motifs in the sequence
    def __init__(self, sequence):
        #this is the sequence it came from
        self.sequence = sequence
        #this is an empty list to store all of the motif locations
        self.motifs = []

class Motif():
    #this class finds all of the possible motifs
    def __init__(self, motif:str):
        #this is the motif
        self.motif = motif
        #this is the regex string used to search for the motif
        self.regex = ''

    def regex_motif_maker(self):
        #looping though each character in a motif
        for character in self.motif:
            #making the character uppercase to search in dictionary
            character = character.upper()
            #adding the regex for that character to the motif regex string
            self.regex += f"[{ambiguous[character]}]"


#getting the information --------------------------------------------------------------------------------

#this is a dictionary with all of the ambiguous nucleotides
ambiguous:dict = {'A': 'Aa', 
                  'C': 'Cc',
                  'G': 'Gg',
                  'T': 'Tt',
                  'U': 'Uu',
                  'W': 'AaTt',
                  'S': 'CcGg',
                  'M': 'AaCc',
                  'K': 'GgTt',
                  'R': 'AaGg',
                  'Y': 'CcTt',
                  'B': 'CcGgTt',
                  'D': 'AaGgTt',
                  'H': 'AaCcTt',
                  'V': 'AaCcGg',
                  'N': 'AaCcGgTt'}

#creating an empty list to store all the motif classes
motifs:list = []

#opening the motif file to read
with open(m, "r") as motif_file:
    #reading the file line by line
    for line in motif_file:
        #stripping the line of the new line character
        line:str = line.strip("\n")
        #creating a new motif class
        motif = Motif(line)
        #calling the function in the Motif class to make the regex for the motif
        motif.regex_motif_maker()
        #adding the one motif class the list of all motifs
        motifs.append(motif)

#this is how to gee the motif and the regex for the motif from the motif class
print(motifs[0].motif)

#go through the FASTA one line at a time
#opening the reading FASTA file!
with open(f, "r") as fasta:
    #initalizing an empty string to hold the sequence
    seq_line = ''
    #initalizing an empty list to hold the exon start and end positions
    exon_list = []

    #reading through the lines in the file
    for line in fasta:
        #the line starts with ">" (a header)
        if ">" in line:
            #this is for the first line when the sequence is empty
            if seq_line == '':
                #assigning the header and stripping it of the new line character
                header = line.strip("\n")
            #this is for when we reach any other header and the sequence is not empty (one line)
            else:
                
                #asign the class
                sequence = Sequence(len(seq_line), exon_list, header)
                #emptying the sequence holder
                seq_line = ''
                #assigning the next header
                header = line.strip("\n")
        #runs when at sequence line
        else:
            #adds the line to the string to make sequence one line
            line = line.strip("\n")
            seq_line += line
    #the last case to write the last sequence
    sequence = Sequence(len(seq_line), exon_list, header)

#get the header and save it for title use for the picture
#make the sequence one line/one string with no new line characters
#get the sequence length!
#get the start and end position of all the exons as a list (make a function?)
    #used regex because uppercase wooo1
#assign this information to a sequence class
#start to find all of the motifs (use the regex that i wonderfully make above in the motif class)
#LOOK AT REGEX DOCUMENTATION to get the start and end position for each instance --> span
#assign that information to the motiffinder class 

#draw a beautiful visual :)