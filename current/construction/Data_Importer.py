import logging
from neo4j.exceptions import Neo4jError
from core import config as cfg

#Generic Importer class for executing cypher scripts. Constructor accepts driver reference. 
class Data_Importer:
    def __init__(self, driver):
        self.driver = driver

"""#ignore this stuff
class go_importer(Data_Importer):
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
                print("({count}) GO annotations added".format(count=record['count']))
    
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
#ignore this stuff
    def initialize_graph(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._initialize_graph
            )
        for record in result:
            print(record["quality"])

    @staticmethod
    def _initialize_graph(tx):
        cypher_script = open("current/Analysis/Cypher_Scripts/Initialize_Graph.cypher", "r")
        query = cypher_script.read()
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"quality":record["quality"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def refactor(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._refactor
            )
        for record in result:
            print(record["quality"])

    @staticmethod
    def _refactor(tx):
        cypher_script = open("current/Analysis/Cypher_Scripts/Refactor_Graph.cypher", "r")
        query = cypher_script.read()
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"quality":record["quality"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def project(self,projection_name):
        # Read in the file
        with open('current/Analysis/Cypher_Scripts/Project_Graph.cypher', 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('$PROJECTION_NAME', projection_name)

        # Write the file out again
        with open('current/Analysis/Cypher_Scripts/Project_Graph.cypher', 'w') as file:
            file.write(filedata)

        with self.driver.session() as session:
            result = session.write_transaction(
                self._project
            )
        for record in result:
            print(record["quality"])

    @staticmethod
    def _project(tx):
        cypher_script = open("current/Analysis/Cypher_Scripts/Project_Graph.cypher", "r")
        query = cypher_script.read()
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"quality":record["quality"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def stream_similarity(self,projection_name,metric):
        # Read in the file
        with open('current/Analysis/Cypher_Scripts/Stream_Gene_Similarity.cypher', 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('$PROJECTION_NAME', projection_name)
        filedata = filedata.replace('$SIMILARITY_METRIC', metric)

        # Write the file out again
        with open('current/Analysis/Cypher_Scripts/Project_Graph.cypher', 'w') as file:
            file.write(filedata)
            
        with self.driver.session() as session:
            result = session.write_transaction(
                self._stream_similarity
            )
            return result

    @staticmethod
    def _stream_similarity(tx):
        cypher_script = open("current/Analysis/Cypher_Scripts/Stream_Gene_Similarity.cypher", "r")
        query = cypher_script.read()
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"name1":record["name1"],"name2":record["name2"],"similarity":record["similarity"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise """

#executes cypher scripting which loads genes, gene products, their relationships, and associated metadata
class Entity_Importer(Data_Importer): 
    def testing(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._test
            )
        for record in result:
            print(record["quality"])

    @staticmethod
    def _test(tx):
        cypher_script = open("current/construction/cypher_scripts/test.cypher", "r")
        query = cypher_script.read()
        print(query)
        result = tx.run(query)
        cypher_script.close()
        try:
            return [{"quality":record["quality"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
 
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

    @staticmethod
    def _create_gene_to_uniparc_mapping(tx):
        query = open("current/construction/cypher_scripts/genes_and_gene_products/import_genes_transcripts_proteins.cypher", "r")
        #query = print(query.read().replace("$GENE2UNIPARC",cfg.GENE2UNIPARC_URI))
        result = tx.run(query.read().replace("$GENE2UNIPARC",cfg.GENE2UNIPARC_AUTOMATED_URI))
        query.close()
        try:    
            return [{"genes":record["genes"],"transcripts":record["transcripts"],"uniparc":record["uniparc"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _set_uniprot_accession_labels(tx):
        query = open("current/construction/cypher_scripts/genes_and_gene_products/import_uniprot_accession_ids.cypher", "r")
        result = tx.run(query.read().replace("$GENE2UNIPARC",cfg.GENE2UNIPARC_AUTOMATED_URI))
        try:
            query.close()
            return [{"isoforms":record["isoforms"],"manual_entry":record["manual_entry"],"automatic_entry":record["automatic_entry"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _set_ensembl_primary_sequence_flags(tx):
        query = open("current/construction/cypher_scripts/genes_and_gene_products/import_alt_seq_mapping.cypher", "r")
        result = tx.run(query.read().replace("$ALT_SEQ",cfg.ALTSEQ_AUTOMATED_URI))
        try:
            query.close()
            return [{"primary":record["primary"],"alternate":record["alternate"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

#executes cypher scriptiing which loads gene/protein annotations. Annotations include: structure, function, & interactions
class Annotation_Importer(Data_Importer):
    def create_go_annotations(self):
        """ with self.driver.session() as session:
            print ("creating go annotations...")
            result = session.write_transaction(
                self._create_ctdbase_go_annotations
            )
            for record in result:
                print("({count}) GO annotations added".format(count=record['count'])) """
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
                print("({count}) GO annotations added".format(count=record['count']))
    
    def create_gene_chemical_annotations(self):
        with self.driver.session() as session:
            print("creating gene chemical associations...")
            result = session.write_transaction(
                self._create_gene_chem_annotations
            )
            for record in result:
                print("({count}) gene-chemical annotations nodes added".format(count=record['count']))
    
    def create_gene_pathway_annotations(self):
        with self.driver.session() as session:
            print("creating pathway associations...")
            result = session.write_transaction(
                self._create_pathway_annotations
            )
            for record in result:
                print("({count}) pathway annotations nodes added".format(count=record['count']))
    
    def create_disease_chem_annotations(self):
        with self.driver.session() as session:
            print("creating d-c associations...")
            result = session.write_transaction(
                self._create_disease_chem_annotations
            )
            for record in result:
                print("({count}) disease-chem annotations nodes added".format(count=record['count']))

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
            for record in result:
                print("({count}) string annotations added".format(count=record['count']))
            print("creating string interactions...")
            result = session.write_transaction(
                self._create_string_interactions
            )
            for record in result:
                print("({count}) bidirectional string interactions added".format(count=record['count']))

    def create_gene_disease_associations(self):
        with self.driver.session() as session:
            print("creating diseases...")
            result = session.write_transaction(
                self._create_ctdbase_diseases
            )
            for record in result:
                print("({count}) diseases added".format(count=record['count']))
            print("creating gene-disease annotations...")
            result = session.write_transaction(
                self._create_ctdbase_gene_disease_associations
            )
            for record in result:
                print("({count}) annotations added".format(count=record['count']))
    
    @staticmethod
    def _create_go_annotations(tx):
        query = open("current/construction/cypher_scripts/GO/yamanaka_import_GO.cypher", "r")
        result = tx.run(query.read().replace("$GAF_PRUNED_URI",cfg.GOA_PRUNED))
        query.close()
        try:
            return "done" #[{"component":record["component"], "process":record["process"], "function":record['function']} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_ctdbase_go_annotations(tx):
        query = open("current/construction/cypher_scripts/GO/ctdbase_import_go.cypher", "r")
        result = tx.run(query.read().replace("$CDTBASE_GO_URI",cfg.CTDBASE_GO))
        query.close()
        try:
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_gene_chem_annotations(tx):
        query = open("current/construction/cypher_scripts/toxicogenomics/create_ctdbase_gene_chemical_associations.cypher", "r")
        result = tx.run(query.read().replace("$CDTBASE_GENE_CHEMICAL_URI",cfg.CTDBASE_GENE_CHEMICAL))
        query.close()
        try:
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_pathway_annotations(tx):
        query = open("current/construction/cypher_scripts/toxicogenomics/create_ctdbase_pathways.cypher", "r")
        result = tx.run(query.read().replace("$CDTBASE_PATHWAY_URI",cfg.CTDBASE_PATHWAY))
        query.close()
        try:
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_disease_chem_annotations(tx):
        query = open("current/construction/cypher_scripts/toxicogenomics/create_ctdbase_chemical_disease_associations.cypher", "r")
        result = tx.run(query.read().replace("$CDTBASE_DISEASE_CHEMICAL_URI",cfg.CTDBASE_DISEASE_CHEMICAL))
        query.close()
        try:
            return [{"count":record["count"]} for record in result]
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
        query = open("current/construction/cypher_scripts/DBD/yamanaka_import_CIS_BP.cypher", "r")
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
        query = open("current/construction/cypher_scripts/TFClass/yamanaka_import_TFUtils.cypher", "r")
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
        query = open("current/construction/cypher_scripts/PFM/yamanaka_import_jaspar.cypher", "r")
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
        query = open("current/construction/cypher_scripts/protein_associations/import_biogrid_interactions.cypher", "r")
        result = tx.run(query.read().replace("$BIOGRID_URI",cfg.BIOGRID))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_ctdbase_diseases(tx):
        query = open("current/construction/cypher_scripts/toxicogenomics/create_ctdbase_diseases.cypher", "r")
        result = tx.run(query.read().replace("$CDTBASE_GENE_DISEASE_URI",cfg.CTDBASE_GENE_DISEASE))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_ctdbase_gene_disease_associations(tx):
        query = open("current/construction/cypher_scripts/toxicogenomics/create_ctdbase_disease_gene_associations.cypher", "r")
        result = tx.run(query.read().replace("$CDTBASE_GENE_DISEASE_URI",cfg.CTDBASE_GENE_DISEASE))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_string_annotations(tx):
        query = open("current/construction/cypher_scripts/protein_associations/import_string_annotation.cypher", "r")
        result = tx.run(query.read().replace("$STRING_ANNOTATION_URI",cfg.STRING_ANNOTATION))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    @staticmethod
    def _create_string_interactions(tx):
        query = open("current/construction/cypher_scripts/protein_associations/import_string_interactions.cypher", "r")
        result = tx.run(query.read().replace("$STRING_INTERACTIONS_URI",cfg.STRING_INTERACTIONS))
        try:
            query.close()
            return [{"count":record["count"]} for record in result]
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise