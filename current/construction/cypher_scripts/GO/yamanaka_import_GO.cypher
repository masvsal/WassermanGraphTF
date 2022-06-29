//load CSV
//------------------
LOAD CSV WITH HEADERS FROM '$GAF_PRUNED_URI' as line
//find protein
match (prot:Protein)<-[:ENCODES]-(t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = TRUE AND g.primary_seq_flag = TRUE AND line.DB_Object_ID IN prot.uniprot_swissprot_id

//add nodes:
//-----------------
//GO class:
WITH g, line
MERGE (GO:load {id:line.GO_ID, namespace:line.Aspect})

//Annotation: (use create because each new line needs separate annotation node)
CREATE (ann:Annot {
	qualifiers:split(coalesce(line.Qualifier), "|"),
	evidence_code:line.Evidence_Code,
	assigned_by:line.Assigned_By, date:line.Date,
	taxon:line.Taxon, not_flag:FALSE,
	with_or_from:coalesce(line.With_Or_From, []),
	annotation_extensions:coalesce(line.Annotation_Extension,[]),
	gene_product_form_id:coalesce(line.Gene_Product_Form_ID,[])})

//Resource:
MERGE (r:Publication {PMID:'', alt_ids:split(coalesce(line.Reference), "|")})

//add relationships:
//-----------------
MERGE (g)-[:HAS_ANNOTATION]->(ann)-[:ANNOTATED_TO]->(GO)
MERGE (ann)-[:BECAUSE]->(r)

WITH g, split(coalesce(line.DB_Object_Synonym), "|") as synonyms

//enrich protein database name
CALL {
	WITH g, synonyms
	RETURN apoc.coll.toSet(g.aliases + synonyms) as alt_names
}

WITH g, alt_names
SET g.aliases = alt_names
;