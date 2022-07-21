LOAD CSV WITH HEADERS
	FROM '$CDTBASE_DISEASE_CHEMICAL_URI' as line

MATCH (d:Disease)
WHERE d.mesh_id = line.DiseaseID

MATCH (ch:Chemical)
WHERE ch.ctdbase_id = line.ChemicalID

CREATE (a1:Annot {from:'CTDBase'})
CREATE (ass:Association {bidirectional_flag:TRUE})

MERGE (d)-[:HAS_ANNOTATION]->(a1)
MERGE (ch)-[:HAS_ANNOTATION]->(a1)
MERGE (a1)-[:ANNOTATED_TO]->(ass)

WITH a1, split(line.PubMedIDs, '|') as pubmed_list

UNWIND pubmed_list as pubmed_id

MERGE (p:Publication {PMID:pubmed_id})

MERGE (a)-[:BECAUSE]->(p)

RETURN count(a) as count

;