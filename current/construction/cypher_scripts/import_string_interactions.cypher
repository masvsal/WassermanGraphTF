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
    coexpression:line.coexpression,
    automated_textmining:toFloat(line.automated_textmining),
    database_annotated:toFloat(line.database_annotated)})

MERGE (p1)-[:HAS_ANNOTATION]->(a)<-[:HAS_ANNOTATION]-(p2)
RETURN count(a) as count
;