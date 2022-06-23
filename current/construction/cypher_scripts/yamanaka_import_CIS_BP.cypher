:param PROTSEQ => ''

:begin
LOAD CSV WITH HEADERS FROM "file:///" + $PFM_CSV as line
match (p:Protein)<-[:ENCODES]-(t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = '1' AND g.primary_seq = TRUE AND line.TF_Name IN g.aliases
SET p.cis_bp_id = line.TF_ID
with g,line
UNWIND split(line.Pfam_DBDs, ",") as dbd
merge (f:DBD {name:dbd, seq:line.DBD_seqs})
with g,f,line
UNWIND split(line.Pfam_froms, ",") as from_
UNWIND split(line.Pfam_tos, ",") as to_
create (a:Annot {tax_group:line.Species, gene:line.Gene_ID, protein:line.Protein_ID, sequence: line.Protein_seq})
merge (g)-[:HAS_ANNOTATION]->(a)->[:ANNOTATED_TO]->(f)
:commit