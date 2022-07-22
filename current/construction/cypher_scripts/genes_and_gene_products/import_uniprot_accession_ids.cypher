//:param PROTEINTOUNIPARC=>'ensembl_gene_to_uniprot_accessions.csv'
LOAD CSV WITH HEADERS
	FROM '$GENE2UNIPARC' as line
MATCH (p:Protein)
WHERE line.Protein_Stable_ID IN p.ensembl_ids

SET p.isoform_id = p.isoform_id + [coalesce(line.UniProtKB_Isoform_ID,'NONE ASSOCIATED') ]
SET p.uniprot_swissprot_id = p.uniprot_swissprot_id + [coalesce(line.UniProtKB_Swiss_Prot_ID,'NONE ASSOCIATED') ]
SET p.uniprot_trembl_id = p.uniprot_trembl_id + [coalesce(line.UniProtKB_TrEMBL_ID,'NONE ASSOCIATED')]

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
CALL {
    WITH p
    WITH p
    WHERE (p.isoform_id <> ['NONE ASSOCIATED'])
    SET p.isoform_id = [x IN p.isoform_id WHERE x <> "NONE ASSOCIATED"]
    WITH count(p) as count
    RETURN count as isoforms
}
CALL {
    WITH p
    WITH p
    WHERE (p.uniprot_swissprot_id <> ['NONE ASSOCIATED'])
    SET p.uniprot_swissprot_id = [x IN p.uniprot_swissprot_id WHERE x <> "NONE ASSOCIATED"]
    WITH count(p) as count
    RETURN count as manual_entry
}
CALL {
    WITH p
    WITH p
    WHERE (p.uniprot_trembl_id <> ['NONE ASSOCIATED'])
    SET p.uniprot_trembl_id = [x IN p.uniprot_trembl_id WHERE x <> "NONE ASSOCIATED"]
    WITH count(p) as count
    RETURN count as automatic_entry
}

RETURN count(isoforms) as isoforms, count(manual_entry) as manual_entry, count(automatic_entry) as automatic_entry
;