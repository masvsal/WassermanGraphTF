MATCH (l:load)

CALL {
    WITH l
    WITH l
    WHERE l.namespace = 'F'
    SET l:Mol_Function
    REMOVE l:load
    REMOVE l.namespace
    WITH count(l) as count
    RETURN count = 1 as isF
}

CALL {
    WITH l
    WITH l
    WHERE l.namespace = 'P'
    SET l:Biol_Process
    REMOVE l:load
    REMOVE l.namespace
    WITH count(l) as count
    RETURN count = 1 as isP
}

CALL {
    WITH l
    WITH l
    WHERE l.namespace = 'C'
    SET l:Cell_Component
    REMOVE l:load
    REMOVE l.namespace
    WITH count(l) as count
    RETURN count = 1 as isC
}

MERGE (o:Ontology {name:'Gene Ontology (GO)'})
MERGE (l)-[:IN_ONTOLOGY]->(o)

WITH l

MATCH (l)<-[:ANNOTATED_TO]-(a:Annot)

CALL {
    WITH a
    WITH a
    WHERE size(a.qualifiers) = 2
    SET a.not_flag = TRUE
    SET a.qualifier = a.qualifiers[1]
    WITH count(a) as count
    RETURN count = 1 as isTrue
}

CALL {
    WITH a
    WITH a
    WHERE size(a.qualifiers) = 1
    SET a.not_flag = FALSE
    SET a.qualifier = a.qualifiers[0]
    WITH count(a) as count
    RETURN count = 1 as isFalse
}


// WHERE size(n.qualifiers) = 2
// //identifying positive annotations
// MATCH (p:Annot)
// WHERE size(p.qualifiers) = 1

// SET n.not_flag = TRUE
// SET n.qualifier = n.qualifiers[1]

// SET p.not_flag = FALSE
// SET p.qualifier = p.qualifiers[0]

WITH a

//make PMID primary reference ID in references
// MATCH (r:Publication)
MATCH (a)-[:BECAUSE]->(p:Publication)
WHERE ANY (id IN p.alt_ids WHERE id STARTS WITH 'PMID:')

WITH apoc.coll.indexOf(p.alt_ids, 'PMID*') as n, p, a
SET p.PMID = p.alt_ids[n]

WITH collect(a) as annots

RETURN count(annots) as count
;