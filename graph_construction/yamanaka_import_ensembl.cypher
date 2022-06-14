//set variables
:param GENETOPROTEIN=>'ensembl_gene_to_uniparc.csv'
:param ENRICHUNIPARC=>'ensembl_gene_to_uniprot_accessions.csv'
:param ALTSEQMAPPING=>'yamanaka_alt_seq_mapping.csv'

//set database
:use isoformschemajune10
//'DATABASE_NAME' replaced by passed parameter

//GENE~~~~~~~
//Aliases: set
//
//TRANSCRIPT~~~~~~~
//Encodes: set
//
//~~~~~~~~~~~~~

//:begin

//create indexes and constraints
//CREATE CONSTRAINT ON (t:Transcript) ASSERT t.ensembl_id IS UNIQUE;
//CREATE CONSTRAINT ON (g:Gene) ASSERT g.ensembl_id IS UNIQUE;
//CREATE CONSTRAINT ON (p:Protein) ASSERT p.UniParc_id IS UNIQUE;

//:commit

:begin

//load genes
LOAD CSV WITH HEADERS
	FROM "file:///" + $GENETOPROTEIN as line
MERGE (g:Gene {ensembl_id:line.Gene_Stable_ID, ensembl_description:line.Gene_Description})
MERGE (t:Transcript {ensembl_id:line.Transcript_Stable_ID, ensembl_canonical_flag:toBoolean(coalesce(line.Ensembl_Canonical,0))})
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

WITH collect(g) as genes
RETURN "Ensembl to UniParc added"
;

LOAD CSV WITH HEADERS
	FROM "file:///" + $ENRICHUNIPARC as line
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

WITH collect(p) as proteins
RETURN "Uniprot IDs added to UniParc"
;

LOAD CSV WITH HEADERS
	FROM "file:///" + $ALTSEQMAPPING as line
MATCH (g:Gene {ensembl_id:line.Gene_Stable_ID})
SET g.primary_seq_flag=toBoolean(line.Primary_Seq)
;



:commit 