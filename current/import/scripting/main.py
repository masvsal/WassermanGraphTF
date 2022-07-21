import ensembl_request as er
import string_request as sr
import biogrid_request as br
import GAF_parse as gp
import jaspar_request as jp
import tfclass_parse as tp
import ctdbase_request as cr
from core import config as cfg
import time
import pandas as pd

gene_names = cfg.GENE_NAMES

ensembl_timing = []
jaspar_timing = []
other_timing = []

def benchmark(gene_names_added):
    for i in range(1,len(gene_names_added) - 1):
        #import and save information associated with gene names
        gene_names = gene_names_added[:i]
        start = time.time()
        er.request_ensembl(gene_names=gene_names)
        end = time.time()
        ensembl_timing += [end - start]
        #import and save information annotations with gene names from each of the following databases
        start = time.time()
        jp.request_jaspar(gene_names=gene_names)
        end = time.time()
        jaspar_timing += [end - start]
        start = time.time()
        gp.parse_go_annotations(gene_names=gene_names)
        tp.parse_tfclass(gene_names=gene_names)
        sr.request_string(gene_names=gene_names)
        br.request_biogrid(gene_names=gene_names)
        cr.request_CTDbase(gene_names=gene_names)
        end = time.time()
        other_timing += [end - start]

    df = pd.DataFrame(data={'ensembl':ensembl_timing, 'jaspar':jaspar_timing, 'other':other_timing})
    df.to_csv('current/analysis/similarity_data/similarity_data.csv')

er.request_ensembl(gene_names=gene_names)
jp.request_jaspar(gene_names=gene_names)
gp.parse_go_annotations(gene_names=gene_names)
tp.parse_tfclass(gene_names=gene_names)
sr.request_string(gene_names=gene_names)
br.request_biogrid(gene_names=gene_names)
cr.request_CTDbase(gene_names=gene_names)