//STRING INTERACTION~~~~~~
//type: bi-directional
//~~~~~~~~~~~~~~~~~~~~~~~~
//load interactions separate relationships
LOAD CSV WITH HEADERS FROM '$STRING_INTERACTIONS_URI' AS line FIELDTERMINATOR '\t'

MATCH (p1:Protein)
WHERE p1.string_id = line.node1_string_id
MATCH (p2:Protein)
WHERE p2.string_id = line.node2_string_id

MERGE (a:Annot {
    from: 'STRING',
    confidence: toFloat(line.combined_score),
    neighborhood_on_chromosome:toFloat(line.neighborhood_on_chromosome),
    gene_fusion:toFloat(line.gene_fusion),
    homology:toFloat(line.homology),
    phylogenetic_cooccurrence:toFloat(line.phylogenetic_cooccurrence),
    experimentally_determined:toFloat(line.experimentally_determined_interaction),
    coexpression:toFloat(line.coexpression),
    automated_textmining:toFloat(line.automated_textmining),
    database_annotated:toFloat(line.database_annotated)})

MERGE (p1)-[:HAS_ANNOTATION {confidence: toFloat(line.combined_score)}]->(a)<-[:HAS_ANNOTATION {confidence: toFloat(line.combined_score)}]-(p2)

WITH "done" as done

LOAD CSV WITH HEADERS FROM '$STRING_PHYSICAL_INTERACTIONS_URI' AS line FIELDTERMINATOR '\t'

MATCH (p1:Protein)-[r1:HAS_ANNOTATION]->(a:Annot)<-[r2:HAS_ANNOTATION]-(p2:Protein)
WHERE a.from = 'STRING' AND p1.string_id = line.node1_string_id AND p2.string_id = line.node2_string_id

SET a.physical_confidence = toFloat(line.combined_score),
SET a.physical_experimentally_determined = toFloat(line.experimentally_determined_interaction)
SET r1.physical_confidence = toFloat(line.combined_score)
SET r2.physical_confidence = toFloat(line.combined_score)

RETURN count(a) as count
;