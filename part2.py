#Software Application Project (Genomics course)

#PART 2
#Here we have a parent Objective class and 5 additional child classes. 
#All child classe inherit the methods of the parent class and possibly provide additional methods


import pandas as pd

class Objective:
    def __init__(self, dataframe):
        self.df = dataframe

    def column_splitter(self, split):
        if(split == 'strand'):
            split = 'chromosome'
        self.df = self.df.loc[:,[split, 'gene_name']]
        return self.df

    def row_splitter(self, split, row_arg):
        self.df = self.df.loc[self.df[split] == row_arg]
        return self.df

    def get_group(self, group):
        self.df = self.df.groupby([group]).count()
        return self.df

    def give_shape(self, sh_arg):
        return self.df.shape[sh_arg]

class GeneCounter(Objective):
    def ascending_order(self, split, group):
        self.column_splitter(split)
        self.get_group(group)
        self.df = self.df.sort_values(by=['gene_name'], ascending = True)
        return self.df

class ChrCounter(Objective):
    def counter(self, group, sh_arg):
        self.get_group(group)
        return self.give_shape(sh_arg)

class Description(Objective):
    def metadata(self, sh_arg):
        return self.give_shape(sh_arg)
    def labels(self):
        return self.df.columns.values

class Strand(Objective):
    def perc_strand(self, split, group, row_arg):
        df = self.df
        self.row_splitter(split, row_arg)
        self.column_splitter(split)
        one_col = self.get_group(group)
        grouped_tot = df.groupby(['chromosome']).count()
        grouped_tot_split = grouped_tot.loc[:,['gene_name']]
        return 100*one_col/grouped_tot_split

class GeneBiotype(Objective):
    def get_group(self, group):
        var1 = self.df.groupby("gene_biotype")
        for (label, content) in self.df.iteritems():
            if (label == "gene_biotype"):
                array = content.values
                if( group in array):
                    var2 = var1.get_group(group)
                    return var2
                else:
                    return "ERROR"
            else:
                pass
