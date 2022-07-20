LOAD CSV WITH HEADERS
	FROM '$CDTBASE_GO_URI' as line

MATCH (g:Gene)
WHERE g.primary_seq_flag = TRUE AND line.GeneSymbol IN g.aliases


MERGE (go:GO_entry {id:line.GoTermID, name:line.GoTermName, ontology:line.Ontology})
CREATE (g)-[r:DIRECT_ANNOTATION]->(go)

RETURN count(r) as count
;