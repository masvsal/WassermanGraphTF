LOAD CSV WITH HEADERS FROM '$CIS_BP_URI' as line FIELDTERMINATOR '\t'
match (p:Protein)<-[:ENCODES]-(t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = TRUE AND g.primary_seq_flag = TRUE AND line.TF_Name IN g.aliases
SET p.cis_bp_id = line.TF_ID
with g,line
UNWIND split(line.Pfam_DBDs, ",") as dbd
merge (f:DBD {name:dbd, seq:line.DBD_seqs})
with g,f,line
UNWIND split(line.Pfam_froms, ",") as from_
UNWIND split(line.Pfam_tos, ",") as to_
create (a:Annot {tax_group:line.Species, gene:line.Gene_ID, protein:line.Protein_ID, sequence: line.Protein_seq, from:from_, to:to_})
merge (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(f)
RETURN count(f) as dbds
;