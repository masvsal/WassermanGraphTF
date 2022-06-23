LOAD CSV WITH HEADERS
	FROM '$GENE2UNIPARC' as line

MATCH (g:Gene)-[:ENCODES]->(t:Transcript)-[:ENCODES]->(pA:Protein)
WHERE g.primary_seq_flag = TRUE AND t.ensembl_canonical_flag = TRUE AND line.OFFICIAL_SYMBOL_A IN g.aliases

MATCH (g:Gene)-[:ENCODES]->(t:Transcript)-[:ENCODES]->(pB:Protein)
WHERE g.primary_seq_flag = TRUE AND t.ensembl_canonical_flag = TRUE AND line.OFFICIAL_SYMBOL_B IN g.aliases

WITH pA, pB
SET pA.biogrid_id = [line.BIOGRID_ID_A,line.SYSTEMATIC_NAME_A]
SET pB.biogrid_id = [line.BIOGRID_ID_B,line.SYSTEMATIC_NAME_B]

MERGE (a:Annot {
	from:line.SOURCEDB, 
	experimental_system = line.EXPERIMENTAL_SYSTEM + ":" + line.EXPERIMENTAL_SYSTEM_TYPE, 
	id:line.BIOGRID_INTERACTION_ID, 
	throughput:line.THROUGHPUT, 
	quantitation:coalesce(line.QUANTITATION, ""), 
	modification:coalesce(line.MODIFICATION, ""),
	qualification:coalesce(line.QUALIFICATIONS, ""), 
	tags:coalesce(line.tags, "")})
MERGE (p:Publication {PMID:line.PUBMED_ID, author:line.PUBMED_AUTHOR})
MERGE (pA)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(pB)
MERGE (a)-[:BECAUSE]->(p)

