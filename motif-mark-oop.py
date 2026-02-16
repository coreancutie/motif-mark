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


#defining the classes ------------------------------------------------------------------------------------

class Sequence():
    #this class is for each sequence in a FASTA
    def __init__(self, sequence, length, exon_list, header):
        #this is the actual sequence (string)
        self.sequence = sequence
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
    def __init__(self, sequence, motif):
        #this is the sequence it came from
        self.sequence = sequence
        #this is the motif we are looking for
        self.motif = motif

        #this is an empty list to store all of the motif locations
        self.motif_locations = []


    def motif_finder(self, sequence, regex):
        '''Given the sequence and the regex for the motif, 
        this function finds all of the motifs in the sequence as a tuple
        and stores their locations in a list'''

        #find all the motifs in the sequence
        motifs = re.finditer(rf'{regex}', sequence)
        #.span() makes a tuple of the start and end position of each motif and puts all the tuples in a list
        self.motif_locations = [motif.span() for motif in motifs]


class Motif():
    #this class finds all of the possible motifs
    def __init__(self, motif:str):
        #this is the motif from the txt file
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

#this is how to get the motif and the regex for the motif from the motif class
# print(motifs[0].motif)


#creating an empty list to store all the sequence classes
sequences:list = []

#go through the FASTA one line at a time
#opening the reading FASTA file!
with open(f, "r") as fasta:
    #initalizing an empty string to hold the sequence
    seq_line = ''
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
                #find all the capital letters (exon) in the sequence
                exons = re.finditer(r'[A-Z]+', seq_line)
                #.span() makes a tuple of the start and end position of each exon 
                #this puts all the tuples in a list
                #this also resets everytime, so it only holds the exon positions for the current sequence
                exon_list = [exon.span() for exon in exons]
                
                #assign the class
                sequence = Sequence(seq_line, len(seq_line), exon_list, header)
                #adding the one sequence class the list of all sequences
                sequences.append(sequence)

                #emptying the sequence holder
                seq_line = ''
                #assigning the next header
                header = line.strip("\n")
        #runs when at sequence line
        else:
            #adds the line to the string to make sequence one line
            line = line.strip("\n")
            seq_line += line
    
    #this is for the last sequence (since there is no header at the end)
    exons = re.finditer(r'[A-Z]+', seq_line)
    exon_list = [exon.span() for exon in exons]
    sequence = Sequence(seq_line, len(seq_line), exon_list, header)
    #adding the one sequence class the list of all sequences
    sequences.append(sequence)


#this is how to get the info from the sequence class
# print(sequences[0].sequence)
# print(sequences[0].length)
# print(sequences[0].exon_list)
# print(sequences[0].header)

#looping though the sequences in the sequecnce class
for sequence in sequences:
    #looping through the motifs in the motif class
    for motif in motifs:
        print(motif.motif)
        #adding to the motif finder class for each sequence and motif
        motif_finder = MotifFinder(sequence, motif)
        motif_finder.motif_finder(sequence.sequence, motif.regex)
       
        print(motif_finder.motif_locations)

#draw a beautiful visual :)