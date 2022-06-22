//this method of importing assigns a new is_annotated_to relationship to every line in fike. Very dense graph will be produced.
//database-specific identifiers are taken from GAF and assigned to protein (ID must have previously existed in alternate_names)
//TODO: fix my horrendous way of checking if an identical relationship exists

//file must be GAF-formatted
:param GAF_FILE_NAME=>'FILE_NAME_HERE'

:begin

LOAD CSV WITH HEADERS FROM "file:///" + $GAF_FILE_NAME as line

MATCH (prot:Protein) 
WHERE line.DB_Object_ID IN prot.alternate_names

MERGE (GO:GO_Concept {class:line.GO_ID, aspect:line.Aspect})
MERGE (prot)-[r:IS_ANNOTATED_TO {
db:line.DB, evidence_code:line.Evidence_Code, assigned_by:line.Assigned_By, date:line.Date,
 references:split(coalesce(line.Reference), "|"), qualifiers:split(coalesce(line.Qualifier), "|"),
 with_or_from:line.With_Or_From, taxon:line.Taxon
}]->(GO)
//optional parameters
SET r.annotation_extensions=line.Annotation_Extension
SET r.gene_product_form_id=line.Gene_Product_Form_ID

WITH prot, line

CALL {
	WITH prot, line
	RETURN apoc.coll.toSet(prot.database_ID + (line.DB + ':' + line.DB_Object_ID)) as DB_IDs
}

WITH prot, DB_IDs

SET prot.database_ID=DB_IDs
;

:commit
