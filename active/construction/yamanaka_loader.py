import logging

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from sqlalchemy import null

from core import config as cfg

class Yamanaka_Loader:
    def __init__(self):
        self.driver = GraphDatabase.driver(cfg.AURADB_URI, 
        auth=(cfg.AURADB_USER, cfg.AURADB_PASSWORD))

    def close(self):
        self.driver.close()
    
    #Imports all information about gene, transcript, and protein relationships. 
    #Groups ensembl proteins by uniparc ID. 
    #Flags genes by primary sequence status in ensembl.
    def create_genes_and_proteins(self):
        with self.driver.session() as session:
            #returns counts of each type of entity added
            print("creating genes, proteins, and transcripts...")
            result = session.write_transaction(
                self._create_gene_to_uniparc_mapping
            )
            for record in result:
                print("{gene} genes with unique Ensembl IDs added. {transcript} transcripts with Unique Ensembl IDs added. {protein} proteins with unique Uniparc IDs added").format(
                    gene=record["genes"],transcript=record["trancripts"],protein=record["uniparc"])

            print("setting uniprot accession ids...")
            result = session.write_transaction(
                self._set_uniprot_accession_labels
            )
            for record in result:
                print("{isoform} uniparc IDs associated with a unique Isoform. {manual} uniparc IDs associated with at least one manually curated uniprotKB entry (swissprot ID). {automatic} proteins associated with at least one automatically curated uniprotKB entry (trembl ID)").format(
                    isoform=record["isoforms"],manual=record["manual_entry"],automatic=record["automatic_entry"])
            
            print("setting primary/alternate sequence flags")
            result = session.write_transaction(
                self._set_ensembl_primary_sequence_flags
            )
            for record in result:
                print("{primary} primary sequences set. {alternate} alternate sequences set").format(primary=record["primary"], alternate=record["alternate"]) 
    def testing(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self.test
            )
        for record in result:
            print(record["t"])

    @staticmethod
    def _create_gene_to_uniparc_mapping(tx):
        query = open("active/construction/cypher_scripts/import_genes_transcripts_proteins.cypher", "r")
        result = tx.run(query.read().replace("$GENE2UNIPARC",cfg.GENE2UNIPARC_URI))
        try:
            query.close()
            return [{"genes":record["genes"],"transcripts":record["transcripts"],"uniparc":record["uniparc"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _set_uniprot_accession_labels(tx):
        query = open("active/construction/cypher_scripts/import_uniprot_accession_ids.cypher", "r")
        result = tx.run(query.read().replace("$GENE2UNIPROT",cfg.GENE2UNIPROT_URI))
        try:
            query.close()
            return [{"isoforms":record["isoforms"],"manual_entry":record["manual_entry"],"automatic_entry":record["automatic_entry"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _set_ensembl_primary_sequence_flags(tx):
        query = open("active/construction/cypher_scripts/import_alt_seq_mapping.cypher", "r")
        result = tx.run(query.read().replace("$ALT_SEQ",cfg.ALTSEQ_URI))
        try:
            query.close()
            return [{"primary":record["primary"],"alternate":record["alternate"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def test(tx):
        cypher_script = open("active/construction/cypher_scripts/test.cypher", "r")
        query = cypher_script.read()
        print(query)
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"t":record["counts"] for record in result}]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

if __name__ == "__main__":
    loader = Yamanaka_Loader()
    loader.create_genes_and_proteins()
    loader.close()
    
    
