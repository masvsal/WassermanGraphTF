LOAD CSV WITH HEADERS
	FROM '$STRING_ANNOTATION_URI' as line FIELDTERMINATOR '\t'
MATCH (g:Gene)-[:ENCODES]->(t:Transcript)-[:ENCODES]->(p:Protein)
WHERE g.primary_seq_flag = TRUE AND t.ensembl_canonical_flag = TRUE AND line.node IN g.aliases

SET g.string_description = line.domain_summary_url
//SET g.aliases = g.aliases + split(coalesce(line.other_names_and_aliases), ",")

WITH p, line

SET p.string_id = line.identifier
SET p.string_domain_diagram = line.annotation
;