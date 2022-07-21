LOAD CSV WITH HEADERS
	FROM '$BIOGRID_URI' as line

MATCH (gA:Gene)-[:ENCODES]->(tA:Transcript)-[:ENCODES]->(pA:Protein)
WHERE gA.primary_seq_flag = TRUE AND tA.ensembl_canonical_flag = TRUE AND line.OFFICIAL_SYMBOL_A IN gA.aliases

MATCH (gB:Gene)-[:ENCODES]->(tB:Transcript)-[:ENCODES]->(pB:Protein)
WHERE gB.primary_seq_flag = TRUE AND tB.ensembl_canonical_flag = TRUE AND line.OFFICIAL_SYMBOL_B IN gB.aliases

WITH pA, pB, line, gA, gB
SET pA.biogrid_id = [line.BIOGRID_ID_A,line.SYSTEMATIC_NAME_A]
SET pB.biogrid_id = [line.BIOGRID_ID_B,line.SYSTEMATIC_NAME_B]

MERGE (assoc:Association {
	from:line.SOURCEDB,
	bidirectional_flag:False,
	id:line.BIOGRID_INTERACTION_ID})

CREATE (a1:Annot {
	bait:pA.uniprot_swissprot_id,
	target:pB.uniprot_swissprot_id,
	experimental_system:line.EXPERIMENTAL_SYSTEM + ":" + line.EXPERIMENTAL_SYSTEM_TYPE,
	throughput:line.THROUGHPUT, 
	quantitation:coalesce(line.QUANTITATION, ""), 
	modification:coalesce(line.MODIFICATION, ""),
	qualification:coalesce(line.QUALIFICATIONS, ""), 
	tags:coalesce(line.tags, "")})

MERGE (p:Publication {PMID:line.PUBMED_ID, author:line.PUBMED_AUTHOR})

CREATE (pA)-[:HAS_ANNOTATION]->(a1)
CREATE (pB)-[:HAS_ANNOTATION]->(a1)
MERGE (a1)-[:ANNOTATED_TO]->(assoc)
MERGE (a1)-[:BECAUSE]->(p)

RETURN count(a1) as count
;

