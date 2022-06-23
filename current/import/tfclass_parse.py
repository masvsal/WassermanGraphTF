#!/usr/bin/env python3

#PARAMETERS:
#MODIFIES: csv file for storing TFClass info about yamanaka transcription factors
#EFFECTS: searches master csv document for familial annotation related to yamanaka TFs

import pandas as pd
import sys

gene_names = ["KLF4", "MYC", "SOX17", "SOX2", "POU5F1"]

#csv in
df = pd.read_csv('data/gene_annotations/tf2TFClass.csv')

#extract relevant rows
loc_col = df.loc[df['Transcription factor'].isin(gene_names)]

#refactor rows
s = loc_col['TF family'].astype(str)
loc_col['TF family'] = s.str.replace("\{.*\}",'')

#out csv
loc_col.to_csv('data/gene_annotations/TFClass.csv')