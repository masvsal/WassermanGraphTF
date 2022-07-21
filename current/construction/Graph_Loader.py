from neo4j import GraphDatabase
from core import config as cfg      
import Data_Importer

#opens connection to AuraDB and initializes database
class Graph_Loader:
    def __init__(self):
        self.driver = GraphDatabase.driver(cfg.AURADB_URI, 
        auth=(cfg.AURADB_USER, cfg.AURADB_PASSWORD))
        self.entity_loader = Data_Importer.Entity_Importer(self.driver)
        self.annotation_loader = Data_Importer.Annotation_Importer(self.driver)
    
    def close(self):
        self.driver.close()
    
    def load_entities(self):
        self.entity_loader.create_genes_and_proteins()

    def load_annotations(self):
        """ self.annotation_loader.create_go_annotations() #works!
        self.annotation_loader.create_tfclass_annotations()
        self.annotation_loader.create_cis_bp_annotations() #works
        self.annotation_loader.create_jaspar_pfm_annotations() #works! :)
        self.annotation_loader.create_biogrid_interaction_annotations()
        self.annotation_loader.create_string_interaction_annotations()
        self.annotation_loader.create_gene_disease_associations()
        self.annotation_loader.create_gene_chemical_annotations()
        self.annotation_loader.create_gene_pathway_annotations() """
        self.annotation_loader.create_disease_chem_annotations()
    
    def test_connection(self):
        self.entity_loader.testing()

#used for some analysis I was doing
class go_loader:
    def __init__(self):
        self.driver = GraphDatabase.driver(cfg.AURADB_URI, 
        auth=(cfg.AURADB_USER, cfg.AURADB_PASSWORD))
        self.go_loader = Data_Importer.go_importer(self.driver)
    def load_go(self):
        self.go_loader.initialize_graph()
        self.go_loader.create_go_annotations()
        self.go_loader.refactor()
    def project_and_stream_similarity(self,projection_name):
        self.go_loader.project(projection_name=projection_name)
        results_o = self.go_loader.stream_similarity(projection_name,'Overlap')
        results_j = self.go_loader.stream_similarity(projection_name,'Jaccard')
        return results_o,results_j
    
