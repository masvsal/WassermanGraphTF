import fetch_endpoint as fe
from core import config as cfg
import pandas as pd
import numpy as np

#request extensions
test_ext = 'info/ping'
symbol_lookup_ext = 'lookup/symbol/human/'
id_lookup_ext = 'lookup/id/'
homology_lookup_ext = 'homology/symbol/human/'
xref_lookup_ext = 'xrefs/id/'
#identifiers primary alleles by gene stable id

def test_connection():
    params = {
        'content-type':'application/json'
    }
    r = fe.fetch_endpoint(cfg.ENSEMBL_BASE_URL, test_ext, params)
    response = r.json()['ping']
    if (response == 1):
        print('connection to biomart established')

#fetch homology of given gene. Saves alt_seq mapping to alt_seq mapping file.
def get_all_alleles(gene_names):
    alt_allele_mapping = {}
    params = {
        'content-type':'application/json',
        'type':'projections',
        'target_species':'human',
        'format':'condensed'
    }

    for name in gene_names:
        r = fe.fetch_endpoint(cfg.ENSEMBL_BASE_URL,homology_lookup_ext + name, params=params)
        response = r.json()
        data = response['data'][0]
        alt_allele_mapping[data['id']] = True #set primary allele to true
        for homology in data['homologies']:
            alt_allele_mapping[homology['id']] = False  #all alternate alleles are false
    df = pd.Series(alt_allele_mapping,name='Primary_Seq')
    df.index.name = 'Gene_Stable_ID'
    df.reset_index()
    df.to_csv('current/data/entities/automated_alt_seq_mapping.csv',index='false')
    print('alt alleles mapped')
    return alt_allele_mapping

#fetch information about multiple genes:
def lookup_all_alleles(alt_allele_mapping):
    header = {'content-type':'application/json','accept':'applications/json'}
    params = {'expand':1,'species':'human'}
    #create id list string for searching by gene ids in ensembl
    data_string = '{"ids":['
    for id in alt_allele_mapping:
        data_string+='"' + id + '",'
    data_string = data_string[:-1] #removes last comma in list
    data_string += ']}'
    #query ensembl using gene id list
    r = fe.fetch_endpoint_POST(cfg.ENSEMBL_BASE_URL,id_lookup_ext,params=params, header=header, data=data_string)
    response = r.json()
    #flatten all useful protein information in response. Also collect each gene's dataframe together
    gene_dfs = []
    for id in alt_allele_mapping:
        gene = response[id]
        for t in gene['Transcript']:
            if t['biotype'] == 'protein_coding':
                t['protein_id'] = t['Translation']['id']
        gene_dfs += [pd.json_normalize(data=gene,record_path ='Transcript',meta=['display_name','id','description','source','version'],meta_prefix='Gene_')]
    #combine and prune gene dataframes
    df = pd.concat(gene_dfs)
    columns_to_remove = [
        'Exon','Translation','start','Parent',"assembly_name","db_type","end",
        'species','biotype','seq_region_name','object_type','logic_name','strand',
        ]
    rows_to_keep = ['protein_coding'] #only keep protein_coding transcripts
    df = df.loc[df['biotype'].isin(rows_to_keep)]
    for col in columns_to_remove:
        col_mask = df.columns.str.startswith(col)
        df = df.loc[:,~col_mask]
    df.rename(columns = {'id':'Transcript_Stable_ID','source':'Transcript_Source','display_name':'Transcript_Name','version':'Transcript_Version','is_canonical':'Ensembl_Canonical','protein_id':'Protein_Stable_ID','Gene_display_name':'Gene_Name','Gene_id':'Gene_Stable_ID'}, inplace = True)
    print('lookup by allele performed')
    return df

#get xrefs
def lookup_all_protein_xrefs(df:pd.DataFrame, protein_ids):
    params = {
        'species':'human',
        'content-type':'application/json',
        'all-levels':1
    }

    xref_dbs = ['UniParc','Uniprot/SWISSPROT','Uniprot_isoform', 'Uniprot/SPTREMBL']
    xref_dbs_mapping = {'UniParc':'UniParc_ID','Uniprot/SWISSPROT':'UniProtKB_Swiss_Prot_ID','Uniprot_isoform':'UniProtKB_Isoform_ID', 'Uniprot/SPTREMBL':'UniProtKB_TrEMBL_ID'}
    
    map = {}
    for protein_id in protein_ids:
        map[protein_id] = {}
        for xref_db in xref_dbs:
            map[protein_id][xref_db] = ''
    for protein_id in protein_ids:
        r = fe.fetch_endpoint(cfg.ENSEMBL_BASE_URL,xref_lookup_ext + protein_id,params=params)
        response = r.json()
        single_gene_xref_df = pd.json_normalize(response)
        single_gene_xref_df = single_gene_xref_df.loc[single_gene_xref_df['dbname'].isin(xref_dbs)]
        for a,b in zip(single_gene_xref_df.dbname, single_gene_xref_df.primary_id):
            map[protein_id][a] = b
    genes_xref_df = pd.DataFrame(map).T
    genes_xref_df.rename(columns=xref_dbs_mapping, inplace=True)
    merged = pd.merge(genes_xref_df,df, left_index=True, right_on='Protein_Stable_ID')
    merged.to_csv('current/data/entities/automated_gene_to_uniparc.csv',index=False)
    
    print('cross-references found')
    return merged

gene_names = cfg.GENE_NAMES

# main
test_connection()
alt_allele_mapping = get_all_alleles(gene_names=gene_names)
gene_information_df = lookup_all_alleles(alt_allele_mapping)
protein_ids = gene_information_df['Protein_Stable_ID'].values
gene_information_df = lookup_all_protein_xrefs(df=gene_information_df,protein_ids=set(protein_ids))