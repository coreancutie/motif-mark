#!/usr/bin/env python

#adding imports
from random import random

from random import random

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

class Motif():
    #this class finds all of the possible motifs
    def __init__(self, motif:str, color:tuple):
        #this is the motif from the txt file
        self.motif = motif
        #this is the color of the motif in normalized RGB values from the motif_colors list
        self.color = color
        #this is the regex string used to search for the motif
        self.regex = ''

    def regex_motif_maker(self):
        #looping though each character in a motif
        for character in self.motif:
            #making the character uppercase to search in dictionary
            character = character.upper()
            #adding the regex for that character to the motif regex string
            self.regex += f"[{ambiguous[character]}]"

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
        #the regex uses a positive lookahead assertion (?=) that it can find overlapping motifs
        motifs = re.finditer(rf'(?=({regex}))', sequence)
        #.span() makes a tuple of the start and end position of each motif and puts all the tuples in a list
        self.motif_locations = [motif.span(1) for motif in motifs]

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
                  'N': 'AaCcGgTtUuNn'}

#this is a list holding normalized rgb values for max 10 different motifs
motif_colors:list = [(0.678, 0.847, 0.902), #light blue 
                     (0.314, 0.784, 0.471), #emerland green 
                     (0.545, 0.0, 0.545), #magenta
                     (0.890, 0.325, 0.212), #terracotta
                     (0.188, 0.361, 0.871), #royal blue
                     (0.4, 0.0, 0.2), #burgandy
                     (1.000, 0.651, 0.788), #light pink
                     (0.929, 0.910, 0.816), #beige
                     (0.035, 0.424, 0.424), #teal (peacock blue)
                     (1.0, 0.8078, 0.1059) #mustard yellow
                     ]

#creating an empty list to store all the motif classes
motifs_list:list = []

#opening the motif file to read
with open(m, "r") as motif_file:
    #initalizing the line number (for the color assignment)
    line_num = 0
    #reading the file line by line
    for line in motif_file:
        #incrementing the line number
        line_num += 1
        #stripping the line of the new line character
        line:str = line.strip("\n")
        #creating a new motif class)
        motif = Motif(line, motif_colors[line_num])
        #calling the function in the Motif class to make the regex for the motif
        motif.regex_motif_maker()
        #adding the one motif class the list of all motifs
        motifs_list.append(motif)

#this is how to get the motif and the regex for the motif from the motif class
# print(motifs_list[0].motif)
# print(motifs_list[0].color)
# print(motifs_list[0].regex)

#creating an empty list to store all the sequence classes
sequences_list:list = []

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
                sequences_list.append(sequence)

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
    sequences_list.append(sequence)

#this is how to get the info from the sequence class
# print(sequences_list[0].sequence)
# print(sequences_list[0].length)
# print(sequences_list[0].exon_list)
# print(sequences_list[0].header)

#creating an empty list to store all the motif finder classes
motif_finders_list:list = []

#looping though the sequences in the sequecnce class
for sequence in sequences_list:
    #looping through the motifs in the motif class
    for motif in motifs_list:
        #adding to the motif finder class for each sequence and motif
        motif_finder = MotifFinder(sequence, motif)
        motif_finder.motif_finder(sequence.sequence, motif.regex)
        
        #appending the motif finder class to the list of all motif finders
        motif_finders_list.append(motif_finder)
       
#this is how to get the info from the motif finder class
# print(motif_finders_list[0].sequence.sequence)
# print(motif_finders_list[0].motif.motif)
# print(motif_finders_list[0].motif_locations)


#draw a beautiful visual --------------------------------------------------------------------------------

#getting the longest sequence length
max_seq_length = max([seq.length for seq in sequences_list])
#getting the number of sequences 
num_sequences = len(sequences_list)
#assigning the width of the image + 100 (50 on each margin)
width = max_seq_length + 100
#assigning the height of the image (each sequence gets 100 pixels and then 50 for each margin)
height = num_sequences * 100 + 100

#making the parameters (the size of the output) 
'''surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)'''
surface = cairo.SVGSurface(f"{f.split('.')[0]}.svg", width, height)
context = cairo.Context(surface)

#set color
context.set_source_rgb(1, 1, 1) #white
#paint the entire surface white
context.paint()

#initalizing a sequence number to keep track of which sequence I am on while drawing
seq_num:int = 0

for current_sequence in sequences_list:
    #incrementing the sequence number 
    seq_num += 1

    #WRITING THE HEADER
    #font 
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    #font size
    context.set_font_size(13)
    #font color
    context.set_source_rgb(0, 0, 0) #black
    #position of text (starts at 50 from the left margin) (50 from the top margin going every 100 for each sequence)
    context.move_to(50, (seq_num * 100) - 50)
    #writing the header of the sequence
    context.show_text(current_sequence.header)

    #DRAWING THE SEQUENCE LINES
    #line width
    context.set_line_width(3)
    #line color
    context.set_source_rgba(0, 0, 0) #black
    #position of line start
    context.move_to(50, (seq_num * 100) - 10)
    #position of line end
    context.line_to(current_sequence.length + 50, (seq_num * 100) - 10)
    context.stroke()

    
    #DRAWING THE EXON BOXES
    #looping through the length of the exon list (this is incase there are multiple exons in a sequence)
    for i in range(len(current_sequence.exon_list)):
        #set color
        context.set_source_rgb(0, 0, 0) #black
        #(x_start, y_start, x_distance, y_distance)
        context.rectangle(current_sequence.exon_list[i][0] + 50, (seq_num * 100) - 20, 
                          current_sequence.exon_list[i][1] - current_sequence.exon_list[i][0], 20)
        #fill the rectangle
        context.fill()

    #DRAWING THE MOTIF BOXES
    #looping though the length of the motif finder class (looping through length because there are multiple matched motifs in a sequence)
    for i in range(len(motif_finders_list)):
        #getting the motif finder class for the current sequence
        if motif_finders_list[i].sequence == current_sequence:
            #looping through the length of the motif finder class for the current sequence
            for j in range(len(motif_finders_list[i].motif_locations)):
                #setting the color of the motif box to what it is assigned to in the class
                context.set_source_rgb(motif_finders_list[i].motif.color[0], motif_finders_list[i].motif.color[1], motif_finders_list[i].motif.color[2])
                #(x_start, y_start, x_distance, y_distance)
                context.rectangle(motif_finders_list[i].motif_locations[j][0] + 50, (seq_num * 100) - 20, 
                                  motif_finders_list[i].motif_locations[j][1] - motif_finders_list[i].motif_locations[j][0], 20)
                #fill the rectangle
                context.fill()


# surface.finish()
#naming the output (the same as the input but without .fasta)
'''surface.write_to_png(f"{f.split('.')[0]}.png",)'''


#pseudocode!!!!!!!
#make a legend for the motifs and their colors :)
