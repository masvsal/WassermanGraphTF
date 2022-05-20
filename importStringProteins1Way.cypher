//create indexes and constraints

//import CSV files

:begin

CREATE CONSTRAINT ON (p:Protein) ASSERT p.identifier IS UNIQUE;
CREATE INDEX ON :Protein(name);

:commit

:begin

LOAD CSV WITH HEADERS
	FROM "file:///" + $PROTEIN_ANNOT + ".csv" AS line
MERGE (p:Protein {identifier: line.identifier})
SET p.name = line.node
SET p.summary = line.domain_summary_url
SET p.annotation = line.annotation
SET p.alternate_names = split(coalesce(line.other_names_and_aliases), ",")
;

LOAD CSV WITH HEADERS
	FROM "file:///" + $PROTEIN_INTERACTIONS + ".csv" AS line
MERGE (p1:Protein {identifier: line.node1_string_id})
MERGE (p2:Protein {identifier: line.node2_string_id})


MERGE (p1)-[:IS_A_NEIGHBOR_OF {confidence: line.neighborhood_on_chromosome}]->(p2)
MERGE (p1)-[:FUSES_WITH {confidence: line.gene_fusion}]->(p2)
MERGE (p1)-[:IS_HOMOLOGOUS_TO{confidence: line.homology}]->(p2)
MERGE (p1)-[:COOCURS_WITH {confidence: line.phylogenetic_cooccurrence}]->(p2)
MERGE (p1)-[:EXPERIMENTALLY_INTERACTS_WITH {confidence: line.experimentally_determined_interaction}]->(p2)
MERGE (p1)-[:COEXPRESSED_WITH {confidence: line.coexpression}]->(p2)
MERGE (p1)-[:FOUND_IN_LITERATURE_WITH {confidence: line.automated_textmining}]->(p2)
MERGE (p1)-[:FOUND_IN_CURATED_DATABASES_WITH {confidence: line.database_annotated}]->(p2)
MERGE (p1)-[:IS_RELATED_TO {confidence: line.combined_score}]->(p2)
;

//refactoring

MATCH ()-[r]->()
SET r.confidence = toFloat(r.confidence) //this messes up 
WITH r
CALL apoc.do.when(r.confidence = 0.0 AND type(r) <> "IS_RELATED_TO",
    'DELETE r',
    '',
    {r:r})
    YIELD value
RETURN value
;



:commit