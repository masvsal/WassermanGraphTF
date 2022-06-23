//:param PROTEINTOUNIPARC=>'ensembl_gene_to_uniprot_accessions.csv'

LOAD CSV WITH HEADERS
	FROM '$GENE2UNIPROT' as line
MATCH (p:Protein)
WHERE line.Protein_Stable_ID IN p.ensembl_ids
SET p.isoform_id = coalesce(p.isoform_id,[]) + [coalesce(line.UniProtKB_Isoform_ID,"")] 
SET p.uniprot_swissprot_id = coalesce(p.uniprot_swissprot_id,[]) + [coalesce(line.UniProtKB_Swiss_Prot_ID,"")] 
SET p.uniprot_trembl_id = coalesce(p.uniprot_trembl_id,[]) + [coalesce(line.UniProtKB_TrEMBL_ID,"")]

WITH p
CALL {
	WITH p
	RETURN apoc.coll.toSet(p.isoform_id) as isoform, apoc.coll.toSet(p.uniprot_swissprot_id) as swissprot, apoc.coll.toSet(p.uniprot_trembl_id) as trembl
}

WITH p,isoform,swissprot,trembl

SET p.isoform_id = isoform
SET p.uniprot_swissprot_id = swissprot
SET p.uniprot_trembl_id = trembl

WITH p

MATCH (isoforms:Protein)
WHERE (isoforms.isoform_id <> [""])

MATCH (manual_entry:Protein)
WHERE (manual_entry.uniprot_swissprot_id <> [""])

MATCH (automatic_entry:Protein)
WHERE (automatic_entry.uniprot_trembl_id <> [""])

RETURN count(isoforms) AS isoforms, count(manual_entry) as manual_entry, count(automatic_entry) as automatic_entry
;