LOAD CSV WITH HEADERS FROM "$JASPAR_PFM_URI" as line
match (prot:Protein)<-[:ENCODES]-(t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = TRUE AND g.primary_seq_flag = TRUE AND split(line.uniprot_ids, "|")[0] IN prot.uniprot_swissprot_id
WITH g, line
CREATE (a:Annot {from:'Jaspar:' + line.collection, entry_url:line.url, id:line.jaspar_id, data_type:line.data_type, data_source:line.data_source, species:line.tax_group})
WITH g,a, line
UNWIND split(line.pubmed_ids,",") as pmid
MERGE (r:Publication {PMID:pmid})
MERGE (pfm:PFM {id:line.jaspar_id,a:line.A, c:line.C, g:line.G, T:line.T})
MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(pfm)
MERGE (a)-[:BECAUSE]->(r)
RETURN count(pfm) as pfms
;

// LOAD CSV WITH HEADERS FROM "file:///" + $Family_Domain_CSV as line
// match (prot:Protein)<-[:ENCODES]-(t:Transcript)<-[:ENCODES]-(g:Gene)
// where t.ensembl_canonical_flag = '1' AND g.primary_seq = TRUE AND split(line.uniprot_ids, "|") IN prot.uniprot_swissprot_id
// with g
// CREATE (a:Annot {from:'Jaspar:' + line.collection, entry_url:line.url, id:line.jaspar_id, species:line.tax_group})
// with g,a
// UNWIND split(line.pubmed_ids,",") as pmid
// MERGE (r:Resource {PMID:pmid})
// //i only account for 1 family and 1 class
// MERGE (f:Family {name:line.family})
// MERGE (c:Class {name:line.class})
// MERGE (g)-[:HAS_ANNOTATION]->(a)-[:ANNOTATED_TO]->(f)-[:IS_A]->(c)
// MERGE (a)-[:BECAUSE]->(r)


