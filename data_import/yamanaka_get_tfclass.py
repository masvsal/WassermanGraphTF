#!/usr/bin/env python3

#PARAMETERS:
#MODIFIES: csv file for storing TFClass info about yamanaka transcription factors
#EFFECTS: searches master csv document for familial annotation related to yamanaka TFs

import pandas as pd
import sys

gene_names = ["KLF4", "MYC", "SOX17", "SOX2", "POU5F1"]
#from_file = sys.argv[1]
#to_file = sys.argv[2]

df = pd.read_csv('gene_annotations/tf2TFClass.csv')
loc_col = df.loc[df['Transcription factor'].isin(gene_names)]
loc_col.to_csv('gene_annotations/TFClass.csv')


print(df.head(1),"\n",loc_col)