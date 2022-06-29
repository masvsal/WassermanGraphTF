LOAD CSV WITH HEADERS FROM '$CIS_BP_URI' as line FIELDTERMINATOR '\t'
//get specific protein
MATCH (p:Protein)
WHERE line.Protein_ID in p.ensembl_ids
//only get primary sequence if protein is canonical
MATCH (g:Gene)-[:ENCODES]->(t:Transcript)-[:ENCODES]->(p)
WHERE t.ensembl_canonical_flag = TRUE AND g.primary_seq_flag = TRUE

//enrich protein with cis_bp id
SET p.cis_bp_id = line.TF_ID

//iterate thru the DNA binding domain and bp coordinate fields. Use it to create DBD and Annotation nodes
WITH g,line, split(line.Pfam_DBDs, ",") as dbd, split(line.Pfam_froms, ",") as from_, split(line.Pfam_tos, ",") as to_

WHERE size(dbd) = size(from_) AND size(dbd) = size(to_)

WITH g,line,dbd,from_,to_,range(0,size(dbd)-1,1) AS coll_size

UNWIND coll_size as idx
MERGE (d:DBD {name:dbd[idx]})
MERGE (a:Annot {from:'CIS_BP', tax_group:line.Species, gene:line.Gene_ID, sequence: line.Protein_seq, dbd_seq:line.DBD_seqs, bp:from_[idx] + ":" + to_[idx]})
merge (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(d)
;