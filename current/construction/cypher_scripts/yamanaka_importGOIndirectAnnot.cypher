
//this method of importing assigns a new is_annotated_to relationship every time any GAF field changes. 
//database-specific identifiers are taken from GAF and assigned to protein (ID must have previously existed in alternate_names)
//TODO: fix my horrendous way of checking if a relationship exists

//file must be GAF-formatted
//:param GAF_FILE_NAME=>'GO_Pruned.csv'

//load CSV
//------------------
LOAD CSV WITH HEADERS FROM '$GAF_PRUNED_URI' as line
//find protein
match (prot:Protein)<-[:ENCODES]-(t:Transcript)<-[:ENCODES]-(g:Gene)
where t.ensembl_canonical_flag = TRUE AND g.primary_seq_flag = TRUE AND line.DB_Object_ID IN prot.uniprot_swissprot_id

//add nodes:
//-----------------
//GO class:
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
//possible null values:
//SET ann.with_or_from=line.With_Or_From
//optional parameters
//SET ann.annotation_extensions=line.Annotation_Extension
//SET ann.gene_product_form_id=line.Gene_Product_Form_ID

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

WITH "task_finished" as statement

//begin refactoring
//-------------------
//make sure optional fields are not null
// MATCH (nullExtension:Annot) WHERE nullExtension.annotation_extensions IS NULL
// MATCH (nullProductForm:Annot) WHERE nullProductForm.gene_product_form_id IS NULL
// MATCH (nullWithOrFrom:Annot) WHERE nu.with_or_from IS NULL

// SET nullExtension.annotation_extensions=[]
// SET nullProductForm.gene_product_form_id=[]
// SET nullWithOrFrom.with_or_from=[]

//WITH "task_finished" as statement

//setup namespace labels
MATCH (f:load {namespace:'F'})
MATCH (p:load {namespace:'P'})
MATCH (c:load {namespace:'C'})

SET f:Mol_Function
REMOVE f:load
REMOVE f.namespace

SET p:Biol_Process
REMOVE p:load
REMOVE p.namespace

SET c:Cell_Component
REMOVE c:load
REMOVE c.namespace

WITH "task_finished" as statement

MATCH (a)
WHERE 'Mol_Function' IN labels(a) OR 'Cell_Component' IN labels(a) OR 'Biol_Process' IN labels(a)
WITH a
MERGE (o:Ontology {name:'Gene Ontology (GO)'})
MERGE (a)-[:IN_ONTOLOGY]->(o)

WITH "task_finished" as statement

//make PMID primary reference ID in references
MATCH (r:Resource)
WHERE ANY (id IN r.alt_ids WHERE id STARTS WITH 'PMID:')
With apoc.coll.indexOf(r.alt_ids, 'PMID*') as n, r
SET r.PMID = r.alt_ids[n]

WITH "task_finished" as statement

//identifying negated annotations
MATCH (n:Annot)
WHERE size(n.qualifiers) = 2
//identifying positive annotations
MATCH (p:Annot)
WHERE size(p.qualifiers) = 1

SET n.not_flag = TRUE
SET n.qualifier = n.qualifiers[1]

SET p.not_flag = FALSE
SET p.qualifier = p.qualifiers[0]

WITH "task_finished" as statement

MATCH (f)
WHERE 'Mol_Function' IN labels(f)
MATCH (c)
WHERE 'Cell_Component' IN labels(c)
MATCH (p)
WHERE 'Biol_Process' IN labels(p)
RETURN count(f) as function, count(c) as component, count(p) as process
;

//SET r.db=line.DB, r.reference=line.Reference, r.evidence_code=line.Evidence_Code, r.assigned_by=line.Assigned_By,r.gene_product_form_id=line.Gene_Product_Form_ID, r.date=line.Date
//SET r.references=split(coalesce(line.Reference), "|")
//SET r.qualifiers=split(coalesce(line.Qualifier), "|") //NOT in position 0
//SET r.with_or_from=line.With_Or_From //pipes and commas mean specific things
//SET r.taxon=line.Taxon //order of elements in list are important
//Annotation extension, Gene product Form ID, taxon, with/from: pipes and commas mean specific things
