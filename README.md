# motif-mark

## Overview Of Script
This script identifies motifs in pre-mRNA and outputs a visual (png) of the sequence and where all the motifs are located. The visual shows intron as a line and exons as a black rectangles. Each FASTA file has one visual output with each sequence drawn to scale in relation to the others. 

Each motif are color coded and marked along the sequence. The script will identify motifs that overlap intron and exons, and in the case of ambiguaty (such a motif NNN that will find AAA, TTT, GGG, and CCC) will identify overlaping regions indicated by the tickmarks under the sequence. The script utalizes object oriented programing (OOP). 

## Inputs

1.  A FATSA file
    - This file could be one-line sequence FASTA or multiple-lined sequence FASTA
    - In the sequence line(s) the introns are lowercase characters
    - In the sequence line(s) the exons are uppercase characters

2.  A motif file
    - A txt file where each line is one motif sequence
    - Each motif can be of any length
    - The motifs can be both upper and lowercase characters
    - The maximum amount of motifs this script will output is 10 different motifs (there are a max of 10 different colors available to be used as a visual)

## Output

- One image (png) per FASTA file input

## Other Notes

- This is Python3 combatable
- This script can be used for both DNA and RNA input FASTA files
- The script doesn't handle case-sensitive motifs, and will find where the motif occurs in both intron and exon sections regardless of their case
    - The motif "ACT" will be found in both exon (uppercase) and introns (lowercase)
- The script can account for motifs that have ambiguous nucleotides (all ambiguous nucleotides can be found [here](https://en.wikipedia.org/wiki/Nucleic_acid_notation))
    - The motif `YGCY` (where the `Y` is either a `C` or a `T`) will find `CGCC`, `TGCT` `TGCC`, and `CGCT` in the sequence. 

## Potential Improvements
- Could output some stats along with the figure
    - how many motifs were in each sequence 
    - how many of each motif were found throughout the entire FASTA file