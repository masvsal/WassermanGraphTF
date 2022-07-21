import fetch_endpoint as fe
import pandas as pd
from core import config as cfg
import utility_functions as uf
import io

def request_report_as_csv(report_name, gene_names,input_type, extra_params = {}):
    params = {
        'inputType':input_type,
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
    df = request_report_as_csv('cgixns', gene_names, 'gene', {'actionTypes':'ANY'})
    df = df[df.Organism == 'Homo sapiens']
    df.to_csv('current/data/gene_annotations/ctdbase/automated_chem_gene_interactions.csv', index=False)
    return df
def get_chemical_associations(gene_names):
    df = request_report_as_csv('chems_curated',gene_names, 'gene')
    df = df[df.Organism == 'Homo sapiens']
    return df
def get_gene_associations(gene_names):
    df = request_report_as_csv('genes_curated',gene_names, 'gene')
    df = df[(df['SrcOrganism'] == 'Homo sapiens') & (df['TgtOrganism'] == 'Homo sapiens')]
    df.to_csv('current/data/gene_annotations/ctdbase/automated_curated_gene_associations.csv', index=False)
    return df
def get_disease_associations(gene_names):
    df = request_report_as_csv('diseases_curated',gene_names, 'gene')
    #df = df[df.Organism == 'Homo sapiens']
    return df
def get_pathway_associations(gene_names):
    df = request_report_as_csv('pathways_curated',gene_names, 'gene')
    return df
def get_go_annotations(gene_names):
    df_bp = request_report_as_csv('go',gene_names,'gene',{'ontology':'go_bp'})
    df_cc = request_report_as_csv('go',gene_names,'gene',{'ontology':'go_cc'})
    df_mf = request_report_as_csv('go',gene_names,'gene',{'ontology':'go_mf'})
    df = pd.concat([df_bp, df_cc, df_mf])
    df.to_csv('current/data/gene_annotations/ctdbase/automated_go_annotations.csv')
    return df

def get_chem_disease_associations(disease_names, chemical_names):
    df =  request_report_as_csv('chems_curated',disease_names,'disease')
    df = df[~df['ChemicalID'].isin(chemical_names)]
    return df
#main

def request_CTDbase(gene_names):
    print('CTDBASE: using gene names to get gene-chemical associations...',end='')
    hmn_chemixns=get_chemical_associations(gene_names=gene_names)
    print('saving...', end='')
    hmn_chemixns.to_csv('current/data/gene_annotations/ctdbase/automated_curated_chem_associations.csv', index=False)
    print("done")
    print('CTDBASE: using gene names to get gene-disease associations...',end='')
    hmn_disease_assc_curated=get_disease_associations(gene_names = gene_names)
    print('saving...', end='')
    hmn_disease_assc_curated.to_csv('current/data/gene_annotations/ctdbase/automated_curated_disease_associations.csv')
    print('done')
    print('CTDBASE: using gene names to get gene-pathway associations...',end='')
    hmn_pathway_assc_curated = get_pathway_associations(gene_names=gene_names)
    print('saving...', end='')
    hmn_pathway_assc_curated.to_csv('current/data/gene_annotations/ctdbase/automated_curated_pathway_associations.csv')
    print('done')

    disease_ids = list(hmn_disease_assc_curated['DiseaseID'].unique())
    chemical_ids = list(hmn_chemixns['ChemicalId'].unique())

    print('CTDBASE: using disease ids to get disease-chemical associations...',end='')
    chem_disease = get_chem_disease_associations(disease_ids,chemical_ids)
    print('saving...', end='')
    chem_disease.to_csv('current/data/gene_annotations/ctdbase/automated_chem_disease_associations.csv')
    print('done')

""" 
chmixns = hmn_chemixns['GeneSymbol'].value_counts().to_frame().rename(columns={'GeneSymbol':'chem-gene associations(curated)'})
print(chmixns)
chems = hmn_chems_curated['GeneSymbol'].value_counts().to_frame().rename(columns={'GeneSymbol':'chem (curated)'})
gene_assc = hmn_gene_assc_curated['SrcGeneSymbol'].value_counts().to_frame().rename(columns={'GeneSymbol':'gene (curated)'})
disease_assc = hmn_disease_assc_curated['GeneSymbol'].value_counts().to_frame().rename(columns={'GeneSymbol':'disease (curated)'})
pathway_assc = hmn_pathway_assc_curated['GeneSymbol'].value_counts().to_frame().rename(columns={'GeneSymbol':'pathway'})
go_annots = hmn_go_annots['GeneSymbol'].value_counts().to_frame().rename(columns={'GeneSymbol':'gene ontology'})

merged = [chmixns, chems, disease_assc, pathway_assc, go_annots]
merged = pd.concat(merged, axis=1)

lol.to_csv('current/analysis/similarity_data/similarity_data.csv',index=True) """