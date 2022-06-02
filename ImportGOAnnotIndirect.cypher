
//this method of importing assigns a new is_annotated_to relationship every time any GAF field changes. 
//database-specific identifiers are taken from GAF and assigned to protein (ID must have previously existed in alternate_names)
//TODO: fix my horrendous way of checking if a relationship exists

//file must be GAF-formatted
:param GAF_FILE_NAME=>'first_5_lines_SOX17_GAF.csv'

:begin
//load CSV
//------------------
LOAD CSV WITH HEADERS FROM "file:///" + $GAF_FILE_NAME as line
//find protein
MATCH (prot) WHERE line.DB_Object_ID IN prot.alternate_names

//add nodes:
//-----------------
//GO class:
MERGE (GO:load {id:line.GO_ID, namespace:line.Aspect})

//Annotation:
MERGE (ann:Annot {qualifiers:split(coalesce(line.Qualifier), "|"), evidence_code:line.Evidence_Code, assigned_by:line.Assigned_By, date:line.Date, with_or_from:line.With_Or_From, taxon:line.Taxon, not_flag:FALSE})
//optional parameters
SET ann.annotation_extensions=line.Annotation_Extension
SET ann.gene_product_form_id=line.Gene_Product_Form_ID

//Resource:
MERGE (r:Resource {PMID:'', alt_ids:split(coalesce(line.Reference), "|")})


//add relationships:
//-----------------
MERGE (prot)-[:HAS_ANNOTATION]->(ann)-[:ANNOTATED_TO]->(GO)
MERGE (ann)-[:BECAUSE]->(r)

WITH prot, line

//enrich protein database name
CALL {
	WITH prot, line
	RETURN apoc.coll.toSet(prot.database_ID + (line.DB + ':' + line.DB_Object_ID)) as DB_IDs
}

WITH prot, DB_IDs

SET prot.database_ID=DB_IDs
;

//begin refactoring
//-------------------
//make sure optional fields are not null
MATCH (ann:Annot) WHERE ann.annotation_extensions IS NULL
SET ann.annotation_extensions=[]
;
MATCH (ann:Annot) WHERE ann.gene_product_form_id IS NULL
SET ann.gene_product_form_id=[]
;

//setup namespace labels
MATCH (f:load {namespace:'F'})
SET f:Mol_Function
REMOVE f:load
REMOVE f.namespace
;
MATCH (p:load {namespace:'P'})
SET p:Biol_Process
REMOVE p:load
REMOVE p.namespace
;
MATCH (c:load {namespace:'C'})
SET c:Cell_Component
REMOVE c:load
REMOVE c.namespace
;
MATCH (a)
WHERE 'Mol_Function' IN labels(a) OR 'Cell_Component' IN labels(a) OR 'Biol_Process' IN labels(a)
WITH a
MERGE (o:Ontology {name:'Gene Ontology (GO)'})
MERGE (a)-[:IN_ONTOLOGY]->(o)
;

//make PMID primary reference ID in references
MATCH (r:Resource)
WHERE ANY (id IN r.alt_ids WHERE id STARTS WITH 'PMID:')
With apoc.coll.indexOf(r.alt_ids, 'PMID*') as n, r
SET r.PMID = r.alt_ids[n]
;

//identifying negated annotations
MATCH (r:Annot)
WHERE size(r.qualifiers) = 2
SET r.not_flag = TRUE
SET r.qualifier = r.qualifiers[1]
;

//identifying positive annotations
MATCH (r:Annot)
WHERE size(r.qualifiers) = 1
SET r.not_flag = FALSE
SET r.qualifier = r.qualifiers[0]
;


:commit


//SET r.db=line.DB, r.reference=line.Reference, r.evidence_code=line.Evidence_Code, r.assigned_by=line.Assigned_By, r.gene_product_form_id=line.Gene_Product_Form_ID, r.date=line.Date
//SET r.references=split(coalesce(line.Reference), "|")
//SET r.qualifiers=split(coalesce(line.Qualifier), "|") //NOT in position 0
//SET r.with_or_from=line.With_Or_From //pipes and commas mean specific things
//SET r.taxon=line.Taxon //order of elements in list are important
//Annotation extension, Gene product Form ID, taxon, with/from: pipes and commas mean specific things
