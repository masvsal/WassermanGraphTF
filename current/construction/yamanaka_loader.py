import logging

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

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
                print("{gene} genes with unique Ensembl IDs added. {transcript} transcripts with Unique Ensembl IDs added. {protein} proteins with unique Uniparc IDs added".format(gene=record["genes"],transcript=record["transcripts"],protein=record["uniparc"]))
                #print("{id} {canonical}".format(id=record["id"],canonical=record['canonical']))

            print("setting uniprot accession ids...")
            result = session.write_transaction(
                self._set_uniprot_accession_labels
            )
            for record in result:
                print("{isoform} uniparc IDs associated with a unique Isoform. {manual} uniparc IDs associated with at least one manually curated uniprotKB entry (swissprot ID). {automatic} proteins associated with at least one automatically curated uniprotKB entry (trembl ID)".format(
                    isoform=record["isoforms"],manual=record["manual_entry"],automatic=record["automatic_entry"]))
            
            print("setting primary/alternate sequence flags")
            result = session.write_transaction(
                self._set_ensembl_primary_sequence_flags
            )
            for record in result:
                print("{primary} primary sequences set. {alternate} alternate sequences set".format(primary=record["primary"], alternate=record["alternate"]))
    
    def create_go_annotations(self):
        with self.driver.session() as session:
            print("creating go annotations...")
            result = session.write_transaction(
                self._create_go_annotations
            )
            print ("formatting go annotations...")
            result = session.write_transaction(
                self._format_go_annotations
            )
            for record in result:
                print("({count}) GO nodes added".format(count=record['count']))

    def create_tfclass_annotations(self):
        with self.driver.session() as session:
            print("creating tfclass...")
            result = session.write_transaction(
                self._create_tfclass_annotations
            )
            for record in result:
                print("({families}) tfclass nodes added".format(families=record['families']))
    
    def create_cis_bp_annotations(self):
        with self.driver.session() as session:
            print("creating dna binding domain (cis bp)...")
            result = session.write_transaction(
                self._create_cis_bp_annotations
            )
            for record in result:
                print("({dbds}) dna binding domain nodes added".format(dbds=record['dbds']))
    
    def create_jaspar_pfm_annotations(self):
        with self.driver.session() as session:
            print("creating jaspar PFM...")
            result = session.write_transaction(
                self._create_jaspar_pfm_annotations
            )
            for record in result:
                print("({pfms}) PFM nodes added".format(pfms=record['pfms']))
    
    def create_biogrid_interaction_annotations(self):
        with self.driver.session() as session:
            print("creating biogrid interactions...")
            result = session.write_transaction(
                self._create_biogrid_interaction_annotations
            )
            for record in result:
                print("({count}) biogrid interactions added".format(count=record['count']))
    
    def create_string_interaction_annotations(self):
        with self.driver.session() as session:
            print("setting string annotations...")
            result = session.write_transaction(
                self._create_string_annotations
            )
            print("creating string interactions...")
            result = session.write_transaction(
                self._create_string_interactions
            )
            for record in result:
                print("({count}) bidirectional string interactions added".format(count=record['count']))

    @staticmethod
    def _create_gene_to_uniparc_mapping(tx):
        query = open("current/construction/cypher_scripts/import_genes_transcripts_proteins.cypher", "r")
        #query = print(query.read().replace("$GENE2UNIPARC",cfg.GENE2UNIPARC_URI))
        result = tx.run(query.read().replace("$GENE2UNIPARC",cfg.GENE2UNIPARC_URI))
        query.close()
        try:    
            return [{"genes":record["genes"],"transcripts":record["transcripts"],"uniparc":record["uniparc"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _set_uniprot_accession_labels(tx):
        query = open("current/construction/cypher_scripts/import_uniprot_accession_ids.cypher", "r")
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
        query = open("current/construction/cypher_scripts/import_alt_seq_mapping.cypher", "r")
        result = tx.run(query.read().replace("$ALT_SEQ",cfg.ALTSEQ_URI))
        try:
            query.close()
            return [{"primary":record["primary"],"alternate":record["alternate"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_go_annotations(tx):
        query = open("current/construction/cypher_scripts/GO/yamanaka_import_GO.cypher", "r")
        result = tx.run(query.read().replace("$GAF_PRUNED_URI",cfg.GAF_PRUNED))
        query.close()
        try:
            return "done" #[{"component":record["component"], "process":record["process"], "function":record['function']} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _format_go_annotations(tx):
        query = open("current/construction/cypher_scripts/GO/yamanaka_format_GO.cypher", "r")
        result = tx.run(query.read())
        query.close()
        try:
            return [{"count":record['count']} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @staticmethod
    def _create_cis_bp_annotations(tx):
        query = open("current/construction/cypher_scripts/yamanaka_import_CIS_BP.cypher", "r")
        result = tx.run(query.read().replace("$CIS_BP_URI",cfg.PROT_SEQ))
        try:
            query.close()
            return [{"dbds":record['count']} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_tfclass_annotations(tx):
        query = open("current/construction/cypher_scripts/yamanaka_import_TFUtils.cypher", "r")
        result = tx.run(query.read().replace("$TFCLASS_URI",cfg.TFCLASS))
        try:
            query.close()
            return [{"families":record["families"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_jaspar_pfm_annotations(tx):
        query = open("current/construction/cypher_scripts/yamanaka_import_jaspar.cypher", "r")
        result = tx.run(query.read().replace("$JASPAR_PFM_URI",cfg.JASPAR_PFM))
        try:
            query.close()
            return [{"pfms":record["pfms"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_biogrid_interaction_annotations(tx):
        query = open("current/construction/cypher_scripts/import_biogrid_interactions.cypher", "r")
        result = tx.run(query.read().replace("$BIOGRID_URI",cfg.BIOGRID))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_string_annotations(tx):
        query = open("current/construction/cypher_scripts/import_string_annotation.cypher", "r")
        result = tx.run(query.read().replace("$STRING_ANNOTATION_URI",cfg.STRING_ANNOTATION))
        try:
            query.close()
            return 'done' #[{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_string_interactions(tx):
        query = open("current/construction/cypher_scripts/import_string_interactions.cypher", "r")
        result = tx.run(query.read().replace("$STRING_INTERACTIONS_URI",cfg.STRING_INTERACTIONS))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def testing(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self.test
            )
        for record in result:
            print(record["quality"],record["model"])

    @staticmethod
    def test(tx):
        cypher_script = open("current/construction/cypher_scripts/test.cypher", "r")
        query = cypher_script.read()
        print(query)
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"quality":record["quality"], "model":record["model"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

#main method
if __name__ == "__main__":
    loader = Yamanaka_Loader()
    loader.testing()
    loader.create_genes_and_proteins()
    loader.create_go_annotations() #works!
    loader.create_tfclass_annotations()
    loader.create_cis_bp_annotations() #works
    loader.create_jaspar_pfm_annotations() #works! :)
    loader.create_biogrid_interaction_annotations()
    loader.create_string_interaction_annotations()
    loader.close()
    
    
