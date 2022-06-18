#ARGUMENTS: (1) from_file, (2) to_file, (3) num_annotations
#MODIFIES: to_file
#EFFECTS: parses from_file for core protein annotations. Writes maximum=*num_annotations* of 
#each GO Annotation namespace to to_file.

import sys
from textwrap import wrap
import csv

from requests import head

#from_file = sys.argv[1]
#to_file = sys.argv[2]
num_annotations = 4 #int(sys.argv[3])

proteins = [
    {'name':"KLF4",'P':0, 'F':0, 'C':0},
    {'name':"MYC",'P':0, 'F':0, 'C':0},
    {'name':"SOX17",'P':0, 'F':0, 'C':0},
    {'name':"SOX2",'P':0, 'F':0, 'C':0},
    {'name':"POU5F1",'P':0, 'F':0, 'C':0}]

header = ['DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','Reference','Evidence_Code','With_Or_From','Aspect','DB_Object_Name','DB_Object_Synonym','DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension','Gene_Product_Form_ID']

with open('/Users/samuelsalitra/WassermanGraphTF-1/graph_data/gene_annotations/namayura_GAF.csv') as from_csv:
    r = csv.reader(from_csv)
    with open('graph_data/gene_annotations/namayura_GAF_Pruned.csv', mode='w') as to_csv:
        w = csv.writer(to_csv)
        w.writerow(header)
        next(r)
        for row in r:
            for protein in proteins:
                if (protein['name'] == row[2]) and (protein[row[8]]) < num_annotations:
                    w.writerow(row)
                    protein[row[8]]+=1

# w.writerow(['DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','Reference','Evidence_Code','With_Or_From','Aspect','DB_Object_Name','DB_Object_Synonym','DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension','Gene_Product_Form_ID'])




