LOAD CSV WITH HEADERS
	FROM '$CDTBASE_GENE_DISEASE_URI' as line

MATCH (g:Gene)
WHERE g.primary_seq_flag = TRUE AND line.GeneSymbol IN g.aliases
MATCH (d:Disease)
WHERE d.mesh_id = line.DiseaseID

SET g.ctdbase_id = line.GeneID

WITH g,d,line

CREATE (a:Annot {from:'CTDbase', evidence:split(line.DirectEvidence,'|')})

MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(d)

WITH a,line,split(line.PubMedIDs, '|') as pubmed_list

UNWIND pubmed_list as pubmed_id

MERGE (p:Publication {PMID:pubmed_id})

MERGE (a)-[:BECAUSE]->(p)

RETURN count(a) as count

;

