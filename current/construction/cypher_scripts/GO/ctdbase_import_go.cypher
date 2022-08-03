//used for testing purposes. Parses GO annotations formatted by the CTDbase database.

LOAD CSV WITH HEADERS
	FROM '$CDTBASE_GO_URI' as line

MATCH (g:Gene)
WHERE g.primary_seq_flag = TRUE AND line.GeneSymbol IN g.aliases


MERGE (go:GO_entry {id:line.GoTermID, name:line.GoTermName, ontology:line.Ontology})

CREATE (a:Annot {from:'CTDBASE'})
MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(go)

RETURN count(a) as count
;