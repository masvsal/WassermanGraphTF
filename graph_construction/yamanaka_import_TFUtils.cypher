:param TFUtils_CSV => 'graph_data/gene_annotations/TFClass.csv'

LOAD CSV WITH HEADERS FROM "file:///" + $TFUtils_CSV as line
match (t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = '1' AND g.primary_seq = TRUE AND line.Transcription_factor IN g.aliases
SET g.aliases = g.aliases + [line.Uniprot_ID]
with g
CREATE (a:Annot {from:'TFUtils',quality:line.Quality, model:line.model, hgnc:line.HGNC, model_length:line.Model_Length})
with g,a
MERGE (f:Family {id:line.TFClass, name:line.TF_family, aliases:[line.TF_Family]})
MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(f)