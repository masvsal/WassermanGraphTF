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
MATCH (r:Publication)
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

WITH "task finished" as statement

MATCH (:Ontology {name:'Gene Ontology (GO)'})<-[:IN_ONTOLOGY]-(go)
RETURN count(go) as count

;