:param TFUtils_CSV => 'TFClass.csv'

:begin

LOAD CSV WITH HEADERS FROM "file:///" + $TFUtils_CSV as line
match (t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = '1' AND g.primary_seq = TRUE AND line.Transcription_factor IN g.aliases
SET g.aliases = g.aliases + [line.UniProt_ID]
with g, line
CREATE (a:Annot {from:'TFUtils',quality:line.Quality, model:line.Model, hgnc:line.HGNC, model_length:line.Model_length})
with g,a, line
MERGE (f:Family {id:line.TFclass, name:line.TF_family, aliases:[line.TF_family]})
MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(f)
;

:commit