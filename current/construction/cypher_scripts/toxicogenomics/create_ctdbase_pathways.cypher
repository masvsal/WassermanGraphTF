LOAD CSV WITH HEADERS
	FROM '$CDTBASE_PATHWAY_URI' as line

MATCH (g:Gene)
WHERE g.primary_seq_flag = TRUE and line.GeneSymbol IN g.aliases

SET g.ctdbase_id = line.GeneID

MERGE (p:Pathway {name:line.PathwayName, id:line.PathwayID, from:split(line.PathwayName,':')[0]})

WITH g,p,line

CREATE (a:Annot)

MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(p)

RETURN count(DISTINCT a) as count

;