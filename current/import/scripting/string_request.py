import fetch_endpoint as fe
from core import config as cfg
import pandas as pd
import io

get_interactions_ext = 'tsv/network'
get_annotations_ext = 'tsv/get_string_ids'

def get_network(gene_names):
    if len(gene_names) == 1:
        print('STRING: One gene selected. 10 closest neighbors returned.')
    params = {
        'identifiers':"%0d".join(gene_names),
        'species':9606,
        'required_score':900,
        'network_type':'functional', #physical
        'show_query_node_labels':1
    }
    r = fe.fetch_endpoint(cfg.STRING_BASE_URL,get_interactions_ext,params=params)
    r = r.content
    df = pd.read_csv(io.StringIO(r.decode('utf-8')), delimiter='\t')
    df.drop_duplicates(inplace=True)
    df = df.rename(columns={'stringId_A':'node1_string_id','stringId_B':'node2_string_id','preferredName_A':'node1','preferredName_B':'node2', 'nscore':'neighborhood_on_chromosome','fscore':'gene_fusion','pscore':'phylogenetic_cooccurrence','ascore':'coexpression','escore':'experimentally_determined_interaction','dscore':'database_annotated','tscore':'automated_textmining','score':'combined_score'},errors='raise')
    return df
def get_annotations(gene_names):
    params = {
        'identifiers':"%0d".join(gene_names),
        'species':9606
    }
    r = fe.fetch_endpoint(cfg.STRING_BASE_URL,get_annotations_ext,params=params)
    r = r.content
    df = pd.read_csv(io.StringIO(r.decode('utf-8')),delimiter='\t')
    df.drop_duplicates(inplace=True)
    df.drop(columns=['queryIndex'],inplace=True)
    df = df.rename(columns={'stringId':'identifier','preferredName':'node'},errors='raise')
    return df

def request_string(gene_names):
    print('STRING: getting network...', end="")
    network_df = get_network(gene_names)
    network_df.to_csv('current/data/protein_interactions/automated_string_interactions.csv',index=False)
    print("done")

    print('STRING: getting annotations...', end="")
    annotation_df = get_annotations(gene_names)
    annotation_df.to_csv('current/data/protein_interactions/automated_string_annotations.csv',index=False)
    print("done")


