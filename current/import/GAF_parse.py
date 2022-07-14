#ARGUMENTS: (1) from_file, (2) to_file, (3) num_annotations
#MODIFIES: to_file
#EFFECTS: parses from_file for core protein annotations. Writes maximum=*num_annotations* of 
#each GO Annotation namespace to to_file.

import sys
from textwrap import wrap
import csv
from core import config as cfg

from requests import head

#from_file = sys.argv[1]
#to_file = sys.argv[2]
 #int(sys.argv[3])

class gaf_parser():
    def __init__(self, num_annot, read_path, write_path, proteins):
        self.num_annotations = num_annot
        self.read_path = read_path
        self.write_path = write_path
        self.proteins = proteins

    def set_num_annot(self, num_annot):
        self.num_annotations = num_annot

    def write_annot(self,is_write_all):

        annot_per_protein = []
        for protein in self.proteins:
            annot_per_protein = annot_per_protein + [{'name':protein, 'P':0, 'F':0, 'C':0}]
        
        header = ['DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','Reference','Evidence_Code','With_Or_From','Aspect','DB_Object_Name','DB_Object_Synonym','DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension','Gene_Product_Form_ID']
        with open(self.read_path) as from_csv:
            r = csv.reader(from_csv)
            with open(self.write_path, mode='w+') as to_csv:
                w = csv.writer(to_csv)
                w.writerow(header)
                next(r) # skip header
                for row in r:
                    for protein in annot_per_protein:
                        if (protein['name'] == row[2]) and (is_write_all or (protein[row[8]]) < self.num_annotations):
                            w.writerow(row)
                            protein[row[8]]+=1

#main
num_annotations = 0
read_path = 'current/data/gene_annotations/goa_human_full.csv'
write_path = 'current/data/gene_annotations/namayura_GAF_Pruned.csv'
proteins = cfg.GENE_NAMES
writer = gaf_parser(num_annot=num_annotations,read_path=read_path,write_path=write_path,proteins=proteins)
writer.write_annot(True) #write all annotations
""" num_annotations = 4

proteins = [
    {'name':"KLF4",'P':0, 'F':0, 'C':0},
    {'name':"MYC",'P':0, 'F':0, 'C':0},
    {'name':"SOX17",'P':0, 'F':0, 'C':0},
    {'name':"SOX2",'P':0, 'F':0, 'C':0},
    {'name':"POU5F1",'P':0, 'F':0, 'C':0}]

header = ['DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','Reference','Evidence_Code','With_Or_From','Aspect','DB_Object_Name','DB_Object_Synonym','DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension','Gene_Product_Form_ID']

with open('current/data/gene_annotations/namayura_GAF.csv') as from_csv:
    r = csv.reader(from_csv)
    with open('current/data/gene_annotations/namayura_GAF_Pruned.csv', mode='w') as to_csv:
        w = csv.writer(to_csv)
        w.writerow(header)
        next(r) # skip header
        for row in r:
            for protein in proteins:
                if (protein['name'] == row[2]): #and (protein[row[8]]) < num_annotations:
                    w.writerow(row)
                    protein[row[8]]+=1

# w.writerow(['DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','Reference','Evidence_Code','With_Or_From','Aspect','DB_Object_Name','DB_Object_Synonym','DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension','Gene_Product_Form_ID'])

 """


