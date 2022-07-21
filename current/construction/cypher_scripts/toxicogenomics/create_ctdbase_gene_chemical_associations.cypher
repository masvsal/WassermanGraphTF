LOAD CSV WITH HEADERS
	FROM '$CDTBASE_GENE_CHEMICAL_URI' as line

MATCH (g:Gene)
WHERE g.primary_seq_flag = TRUE and line.GeneSymbol IN g.aliases
SET g.ctdbase_id = line.GeneId
MERGE (ch:Chemical {cas_id:coalesce(line.CasRN,'NOT FOUND'), name:line.ChemicalName, ctdbase_id:line.ChemicalId })
CREATE (a:Annot {from:'CTDBase',tax_group:line.Organism+':'+toString(toInteger(line.OrganismId))})

MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(ch)

WITH a,split(line.PubMedIds,'|') as pubmed_list
UNWIND pubmed_list as p

MERGE (pub:Publication {PMID:p})

MERGE (a)-[:BECAUSE]->(pub)

RETURN count(DISTINCT a) as count

;
