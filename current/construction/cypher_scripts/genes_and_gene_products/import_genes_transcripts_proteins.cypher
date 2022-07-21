//:param GENETOPROTEIN=>'ensembl_gene_to_uniparc.csv'


//load genes
LOAD CSV WITH HEADERS
	FROM '$GENE2UNIPARC' as line
MERGE (g:Gene {ensembl_id:line.Gene_Stable_ID, ensembl_description:line.Gene_Description})
MERGE (t:Transcript {ensembl_id:line.Transcript_Stable_ID, ensembl_canonical_flag:toBoolean(toInteger(line.Ensembl_Canonical))})
MERGE (p:Protein {UniParc_id: line.UniParc_ID})
CREATE (m:Metadata {from:'Ensembl', gene_source:line.Gene_Source, transcript_source:line.Transcript_Source, gene_version:line.Gene_Version, transcript_version:line.Transcript_Version})

MERGE (g)-[:ENCODES]->(t)-[:ENCODES]->(p)
MERGE (g)-[:HAS_METADATA]->(m)<-[:HAS_METADATA]-(t)

SET t.aliases = coalesce(t.aliases,[]) + [line.Transcript_Name]
SET g.aliases = coalesce(g.aliases,[]) + [line.Gene_Name]
SET p.ensembl_ids = coalesce(p.ensembl_ids,[]) + [line.Protein_Stable_ID]

WITH g, t, p
CALL {
	WITH g, t, p
	RETURN apoc.coll.toSet(g.aliases) as aliases_G, apoc.coll.toSet(t.aliases) as aliases_T, apoc.coll.toSet(p.ensembl_ids) as ensembl_ids
}
WITH g,t,p,aliases_G, aliases_T, ensembl_ids

SET g.aliases = aliases_G
SET t.aliases = aliases_T
SET p.ensembl_ids = ensembl_ids

WITH count(DISTINCT g) as genes, count(DISTINCT t) as transcripts, count(DISTINCT p) as uniparc
RETURN genes, transcripts, uniparc
;