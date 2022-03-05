#Software Application Project (Genomics course)

#PART 3
#Here we have the Web-based user interface, where he can perform actions ad analyze the dataset

import pandas as pd
from flask import Flask
from flask import request, render_template
import part1

app = Flask(__name__)

#We create the DataFrame from the gene_table file, calling the Reader class present in PART 1.
object_df = part1.Reader("gene_table.csv")
df = object_df.create_dataframe()

#Below we have all the pages accessible from the user.
#Besides the pages dedicated to actual results of operetations performed by PART 2
#we have also a login page, an introduction page and an index.
#All pages are provided with a link to go back to the index (or other pages if needed).

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/ready', methods = ["POST"])
def ready():
    name = request.form['name']
    return render_template('ready.html', name = name)


@app.route('/index')
def index():

    topic = [("Number of rows and columns", "n_roco"),
            ("Labels of the columns", "lab"),
            ("Number of genes for each biotype", "ng_bio"),
            ("Choose a biotype and get the associated genes", "g_bio"),
            ("Number of chromosomes", "n_chr"),
            ("Number of genes for each chromosome", "ng_chr"),
            ("Percentage of + strand genes, for each chromosome", "plus_strand"),
            ("Percentage of - strand genes, for each chromosome", "min_strand")
            ]

    return render_template('index.html', topics = topic)


@app.route('/n_roco')
def n_roco():
    obj=part1.Register(df)
    rows = obj.count_rows()
    cols = obj.count_columns()
    return render_template('n_roco.html', rows = rows, columns = cols)

@app.route('/lab')
def lab():
    obj=part1.Register(df)
    var = obj.give_labels()
    return render_template('lab.html', variable = var)

@app.route('/ng_bio')
def ng_bio():
    obj=part1.Register(df)
    var = obj.geneNumber_biotype()
    var = var.rename(columns={'gene_name': 'number of genes'})
    #As our output is a DataFrame we use the pandas attribute DataFrame.to_html() to convert it
    #in an html file to be able to diplay to the user and understandable table
    html = var.to_html()
    text_file = open("templates/ng_bio.html", "w")
    text_file.write("""<head><title>Gene number (biotype)</title></head>""")
    text_file.write("""<p><a href = "/index"> Home</a></p>""")
    text_file.write("""<h2> <i><font color='crimson'> Number of genes for each biotype </font></i></h2>""")
    text_file.write(html)
    text_file.close()
    return render_template('ng_bio.html')

@app.route('/g_bio')
def g_bio():
    return render_template('g_bio.html')

@app.route('/g_bio/result', methods = ["POST"])
def my_form():
    biotype = request.form['biotype']
    obj=part1.Register(df)
    var = obj.genes_biotype(key=biotype)
    #As in this case the user is asked to enter an input, we menage the "invalid input" case
    #with an if/else test,testing if the output received is a string or not
    if isinstance(var, str) == True:
        text_file = open("templates/g_bio_result.html", "w")
        text_file.write("""<head><title>Biotype ERROR</title></head>""")
        text_file.write("""<br><center><h1><font color='red'><b>ERROR!</b></font></h1><h2>This biotype does not exist</h2></center>""")
        text_file.write("""<p><center>Click <a href = "/g_bio">here</a> to try again </center></p>""")
        text_file.close()
    else:
        html = var.to_html()
        text_file = open("templates/g_bio_result.html", "w")
        text_file.write("""<title>Genes per biotype</title>""")
        text_file.write("""<h2> <i><font color='crimson'> <center> Genes associated with the chosen biotype </center></font></i></h2>""")
        text_file.write("""<p><center><a href = "/index"> Home</a> <a href = "/g_bio"> Back</a></center></p> <br>""")
        text_file.write(html)
        text_file.close()
    return render_template('g_bio_result.html')

@app.route('/n_chr')
def n_chr():
    obj=part1.Register(df)
    var = obj.chromosomeNumber()
    return render_template('n_chr.html', variable = var)

@app.route('/ng_chr')
def ng_chr():
    obj=part1.Register(df)
    var = obj.geneNumber_chromosome()
    var = var.rename(columns={'gene_name': 'number of genes'})
    html = var.to_html()
    text_file = open("templates/ng_chr.html", "w")
    text_file.write("""<head><title>Gene number (chromosome)</title></head>""")
    text_file.write("""<p><a href = "/index"> Home</a></p>""")
    text_file.write("""<h2> <i><font color='crimson'> Number of genes for each chromosome</font></i></h2>""")
    text_file.write(html)
    text_file.close()
    return render_template('ng_chr.html')

@app.route('/plus_strand')
def plus_strand():
    obj = part1.Register(df)
    var = obj.plusStrand()
    var = var.rename(columns={'gene_name': 'percentage'})
    html = var.to_html()
    text_file = open("templates/plus_strand.html", "w")
    text_file.write("""<head><title>Plus strand</title></head>""")
    text_file.write("""<p><a href = "/index"> Home</a></p>""")
    text_file.write("""<h2> <i><font color='crimson'> Percentage of + strand genes for each chromosome </font></i></h2>""")
    text_file.write(html)
    text_file.close()
    return render_template('plus_strand.html')

@app.route('/min_strand')
def min_strand():
    obj = part1.Register(df)
    var = obj.minusStrand()
    var = var.rename(columns={'gene_name': 'percentage'})
    html = var.to_html()
    text_file = open("templates/min_strand.html", "w")
    text_file.write("""<head><title>Minus strand</title></head>""")
    text_file.write("""<p><a href = "/index"> Home</a></p>""")
    text_file.write("""<h2> <i><font color='crimson'> Percentage of - strand genes for each chromosome </font></i></h2>""")
    text_file.write(html)
    text_file.close()
    return render_template('min_strand.html')


if __name__ == '__main__':
    app.run(debug = True)
