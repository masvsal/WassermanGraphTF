from typing import Dict
import fetch_endpoint as fe
import pandas as pd
from core import config as cfg
import utility_functions as uf
import io

gene_names = cfg.GENE_NAMES

def use_genes_to_request_report_as_csv(report_name, gene_names, extra_params = {}):
    params = {
        'inputType':'gene',
        'inputTerms':uf.list_to_pipe_del(gene_names), #pipe delimited term list
        'report':report_name,
        'format':'csv',
    }
    for param in extra_params:
        params[param] = extra_params[param]
    r = fe.fetch_endpoint(cfg.CTDBASE_BASE_URL,"",params=params)
    r = r.content
    df = pd.read_csv(io.StringIO(r.decode('utf-8')))
    return df

def get_chemical_gene_interactions(gene_names):
    df = use_genes_to_request_report_as_csv('cgixns', gene_names, {'actionTypes':'Any'})
    df = df[df.Organism == 'Homo sapiens']
    df.to_csv('current/data/gene_annotations/ctdbase/automated_chem_gene_interactions.csv', index=False)
    return df
def get_chemical_associations(gene_names):
    df = use_genes_to_request_report_as_csv('chems_curated',gene_names)
    df = df[df.Organism == 'Homo sapiens']
    df.to_csv('current/data/gene_annotations/ctdbase/automated_curated_chem_associations.csv', index=False)
    return df
def get_gene_associations(gene_names):
    df = use_genes_to_request_report_as_csv('genes_curated',gene_names)
    df = df[(df['SrcOrganism'] == 'Homo sapiens') & (df['TgtOrganism'] == 'Homo sapiens')]
    df.to_csv('current/data/gene_annotations/ctdbase/automated_curated_gene_associations.csv', index=False)
    return df
def get_disease_associations(gene_names):
    df = use_genes_to_request_report_as_csv('diseases_curated',gene_names)
    #df = df[df.Organism == 'Homo sapiens']
    df.to_csv('current/data/gene_annotations/ctdbase/automated_curated_disease_associations.csv')
    return df
def get_pathway_associations(gene_names):
    df = use_genes_to_request_report_as_csv('pathways_curated',gene_names)
    df.to_csv('current/data/gene_annotations/ctdbase/automated_curated_pathway_associations.csv')
    return df
def get_go_annotations(gene_names):
    df_bp = use_genes_to_request_report_as_csv('go',gene_names,{'ontology':'go_bp'})
    df_cc = use_genes_to_request_report_as_csv('go',gene_names,{'ontology':'go_cc'})
    df_mf = use_genes_to_request_report_as_csv('go',gene_names,{'ontology':'go_mf'})
    df = pd.concat([df_bp, df_cc, df_mf])
    df.to_csv('current/data/gene_annotations/ctdbase/automated_go_annotations.csv')
    return df

#main
hmn_chemixns=get_chemical_gene_interactions(gene_names=gene_names)
hmn_chems_curated=get_chemical_associations(gene_names=gene_names)
hmn_gene_assc_curated=get_gene_associations(gene_names=gene_names)
hmn_disease_assc_curated=get_disease_associations(gene_names = gene_names)
hmn_pathway_assc_curated = get_pathway_associations(gene_names=gene_names)
hmn_go_annots = get_go_annotations(gene_names=gene_names)

print("human chemical-gene interaction # \n", hmn_chemixns['GeneSymbol'].value_counts())
print("human chemical association # \n",hmn_chems_curated['GeneSymbol'].value_counts())
print("human gene association # \n",hmn_gene_assc_curated['SrcGeneSymbol'].value_counts())
print("human dis association # \n",hmn_disease_assc_curated['GeneSymbol'].value_counts())
print("pathway association # \n",hmn_pathway_assc_curated['GeneSymbol'].value_counts())
print("GO annot # \n",hmn_go_annots['GeneSymbol'].value_counts())