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
        self.annotation_loader.create_go_annotations() #works!
        self.annotation_loader.create_tfclass_annotations()
        self.annotation_loader.create_cis_bp_annotations() #works
        self.annotation_loader.create_jaspar_pfm_annotations() #works! :)
        self.annotation_loader.create_biogrid_interaction_annotations()
        self.annotation_loader.create_string_interaction_annotations()

    def test_connection(self):
        self.entity_loader.testing()
    
    
