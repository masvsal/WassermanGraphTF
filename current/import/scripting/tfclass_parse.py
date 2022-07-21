#!/usr/bin/env python3

#PARAMETERS:
#MODIFIES: csv file for storing TFClass info about yamanaka transcription factors
#EFFECTS: searches master csv document for familial annotation related to yamanaka TFs

import pandas as pd


def parse_tfclass(gene_names):
    df = pd.read_csv('current/data/gene_annotations/tf2TFClass.csv')

    #extract relevant rows
    loc_col = df.loc[df['Transcription_factor'].isin(gene_names)]

    #refactor rows
    s = loc_col['TF_family'].astype(str)
    loc_col['TF_family'] = s.str.replace("\{.*\}",'')

    #out csv
    loc_col.to_csv('current/data/gene_annotations/TFClass.csv', index=None)