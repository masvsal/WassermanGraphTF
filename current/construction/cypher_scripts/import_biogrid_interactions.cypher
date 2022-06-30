LOAD CSV WITH HEADERS
	FROM '$BIOGRID_URI' as line

MATCH (gA:Gene)-[:ENCODES]->(tA:Transcript)-[:ENCODES]->(pA:Protein)
WHERE gA.primary_seq_flag = TRUE AND tA.ensembl_canonical_flag = TRUE AND line.OFFICIAL_SYMBOL_A IN gA.aliases

MATCH (gB:Gene)-[:ENCODES]->(tB:Transcript)-[:ENCODES]->(pB:Protein)
WHERE gB.primary_seq_flag = TRUE AND tB.ensembl_canonical_flag = TRUE AND line.OFFICIAL_SYMBOL_B IN gB.aliases

WITH pA, pB, line
SET pA.biogrid_id = [line.BIOGRID_ID_A,line.SYSTEMATIC_NAME_A]
SET pB.biogrid_id = [line.BIOGRID_ID_B,line.SYSTEMATIC_NAME_B]

MERGE (a:Annot {
	from:line.SOURCEDB, 
	experimental_system:line.EXPERIMENTAL_SYSTEM + ":" + line.EXPERIMENTAL_SYSTEM_TYPE, 
	id:line.BIOGRID_INTERACTION_ID, 
	throughput:line.THROUGHPUT, 
	quantitation:coalesce(line.QUANTITATION, ""), 
	modification:coalesce(line.MODIFICATION, ""),
	qualification:coalesce(line.QUALIFICATIONS, ""), 
	tags:coalesce(line.tags, "")})
MERGE (p:Publication {PMID:line.PUBMED_ID, author:line.PUBMED_AUTHOR})
MERGE (pA)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(pB)
MERGE (a)-[:BECAUSE]->(p)
RETURN count(a) as count
;

