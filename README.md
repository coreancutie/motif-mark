# motif-mark

The goal:

- Given pre-mRNA sequences in a FASTA file, output a visual that show where motifs are along certain chunks of DNA that are structured: intron-exon-intron 

The Input:

- A FATSA file
    - In the sequence line(s) the introns are in lowercase
    - In the sequence line(s) the exons are uppercase
- A motif file
    - Each line is one motif sequence


Other notes:

- This is Python3 combatable
- This script was tested on FASTA files with seqs ≤1000 bases and a motifs file where each motif is ≤10 bases each
- This script should be flexable for DNA and RNA input FASTA files
- The motifs are given as both uppercase and lowercase. This does not matter and you need to find the motif anywhere it occurs
- If a motif goes across intron and exon, mark it!
- The motifs will have ambigutary such as `YGCY` where the `Y` is either a `C` or a `T`. A sequence of `CGCC` `TGCT` `TGCC` and `CGCT` are all under that one motif. 
- If two motifs overlap you can set the bars to be transparent or have the bars be offset
- If there is a `U` in a motif look for both `T` and `U`

Other notes: 
- Could output some stats along with the figure