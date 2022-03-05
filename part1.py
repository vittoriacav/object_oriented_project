#Software Application Project (Genomics course)

#PART 1 
#a.Here we read and create the DataFrame (Reader class) 
#b/c. We have a Register class that coordinates requestes coming form PART 3 and "forwards" them
#calling appropriate classes of PART 2

import pandas as pd
from part2 import *

class Reader:
    def __init__(self, datafile):
        self.dataf = datafile

    def create_dataframe(self):
        dataframe = pd.read_csv(self.dataf)
        return dataframe

class Register:
    def __init__(self, data, key=None):
        self.df = data
        self.key = key

    def count_rows(self):
       obj = Description(self.df)
       return (obj.metadata(0))

    def count_columns(self):
       obj = Description(self.df)
       return (obj.metadata(1))

    def give_labels(self):
        obj = Description(self.df)
        return (obj.labels())

    def geneNumber_biotype(self):
        obj = GeneCounter(self.df)
        return (obj.ascending_order('gene_biotype', 'gene_biotype'))

    def genes_biotype(self, key):
        obj = GeneBiotype(self.df)
        return obj.get_group(key)

    def chromosomeNumber(self):
        obj = ChrCounter(self.df)
        return obj.counter('chromosome', 0)

    def geneNumber_chromosome(self):
        obj = GeneCounter(self.df)
        return obj.ascending_order('chromosome', 'chromosome')

    def plusStrand(self):
        obj = Strand(self.df)
        return obj.perc_strand('strand', 'chromosome', '+')

    def minusStrand(self):
        obj = Strand(self.df)
        return obj.perc_strand( 'strand', 'chromosome', '-')
