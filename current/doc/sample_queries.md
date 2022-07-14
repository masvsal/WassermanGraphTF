
# Sample Queries:
last updated: july 14th 2022
by: Samuel Salitra

## Computing Similarity Scores Using Neo4j...

Requirements: Database with GDS library installed.
More information: https://neo4j.com/docs/graph-data-science/current/algorithms/similarity/

- Computing similarity between two genes. This only uses annotations attached to the gene encoding a TF.

1. First we must create bi-partite graph:
```cypher
MATCH (g:Gene)-[:HAS_ANNOTATION]->(a:Annot)-[:ANNOTATED_TO]->(e) //get all information annotated to a gene
//create a bi-partite graph of gene and annoated information
SET e:Contextual_Data //node set 1 -- information
SET g:Primary_Gene    //node set 2 -- gene
WITH g,e, count(a) as num_annot
MERGE (g)-[:DIRECT_ANNOTATION {num_annot:num_annot}]->(e) //mapping from gene -> information using relationship weight to denote # of intermediate annotation nodes.
```
2. Project bipartite graph
```cypher
CALL gds.graph.project(
    'GeneToInformationProjection',
    ['Primary_Gene', 'Contextual_Data'],
    {
        DIRECT_ANNOTATION: {
            type: 'DIRECT_ANNOTATION',
            properties: {
                num_annot: {
                    property: 'num_annot'
                }
            }
        }
    }
) YIELD nodeCount as nc, relationshipCount as rc
RETURN nc, rc
;
```
3. Print All Pairwise Similarity Values.
```cypher
call gds.nodeSimilarity.stream('GeneToInformationProjection', {similarityMetric:'OVERLAP'}) //leave replace 'OVERLAP' with 'JACCARD' to compute jaccard similarity instead.
YIELD node1, node2, similarity
WITH head(gds.util.asNode(node1).aliases) as gene_1, head(gds.util.asNode(node2).aliases) as gene_2, pairwise_similarity_score
RETURN gene_1, gene_2, pairwise_similarity_score ORDER BY pairwise_similarity_score DESC
```
- Computing similarity between two proteins. This only uses annotations attached to a protein isoform. 
1. First we must create bi-partite graph:
```cypher
MATCH (p:Protein)-[:HAS_ANNOTATION]->(a:Annot)-[:ANNOTATED_TO]->(e) //get all information annotated to a protein
//create a bi-partite graph of protein and annoated information
SET e:Contextual_Data     //node set 1 -- information
SET gp:Primary_Protein    //node set 2 -- protein
WITH g,e, count(a) as num_annot
MERGE (g)-[:DIRECT_ANNOTATION {num_annot:num_annot}]->(e) //mapping from protein -> information using relationship weight to denote # of intermediate annotation nodes.
```
2. Project bipartite graph
```cypher
CALL gds.graph.project(
    'ProteinToInformationProjection',
    ['Primary_Protein', 'Contextual_Data'],
    {
        DIRECT_ANNOTATION: {
            type: 'DIRECT_ANNOTATION',
            properties: {
                num_annot: {
                    property: 'num_annot'
                }
            }
        }
    }
) YIELD nodeCount as nc, relationshipCount as rc
RETURN nc, rc
;
```
3. Print All Pairwise Similarity Values.
```cypher
call gds.nodeSimilarity.stream('ProteinToInformationProjection', {similarityMetric:'OVERLAP'}) //leave replace 'OVERLAP' with 'JACCARD' to compute jaccard similarity instead.
YIELD node1, node2, similarity
WITH head(gds.util.asNode(node1).uniprot_swissprot_id) as protein_1, head(gds.util.asNode(node2).uniprot_swissprot_id) as protein_2, pairwise_similarity_score
RETURN protein_1, protein_2, pairwise_similarity_score ORDER BY pairwise_similarity_score DESC
```
- Computing similarity using both gene and protein annotations.

1. First we must create bi-partite graph:
```cypher
MATCH (g:Gene)-[:HAS_ANNOTATION]->(a:Annot)-[:ANNOTATED_TO]->(e)
SET g:Primary_TF //node set 1 - gene
SET e:Contextual_Data //node set 2 - protein and gene contextual information
WITH g,e,count(a) as num_annot
MERGE (g)-[:DIRECT_ANNOTATION {num_annot:num_annot}]->(e) //directly connect gene and all of its contextual info
WITH g
MATCH (g)-[:ENCODES]->(t:Transcript)-[:ENCODES]->(p:Protein) //find canonical isoform encoded by gene
WHERE t.ensembl_canonical_flag = TRUE
MATCH (p)-[:HAS_ANNOTATION]->(a:Annot)-[:ANNOTATED_TO]->(e) //find contextual information attached to canonical isoform.
SET e:Contextual_Data
WITH g,e,count(a) as num_annot
MERGE (g)-[:DIRECT_ANNOTATION {num_annot:num_annot}]->(e) //directly connect gene and protein contextual information.
```
2. Project bipartite graph
```cypher
CALL gds.graph.project(
    'GeneAndProteinToInformationProjection',
    ['Primary_TF', 'Contextual_Data'],
    {
        DIRECT_ANNOTATION: {
            type: 'DIRECT_ANNOTATION',
            properties: {
                num_annot: {
                    property: 'num_annot'
                }
            }
        }
    }
) YIELD nodeCount as nc, relationshipCount as rc
RETURN nc, rc
;
```
3. Print All Pairwise Similarity Values.
```cypher
call gds.nodeSimilarity.stream('GeneAndProteinToInformationProjection', {similarityMetric:'OVERLAP'}) //leave replace 'OVERLAP' with 'JACCARD' to compute jaccard similarity instead.
YIELD node1, node2, similarity
WITH head(gds.util.asNode(node1).aliases) as TF_1, head(gds.util.asNode(node2).aliases) as TF_2, pairwise_similarity_score
RETURN TF_1, TF_2, pairwise_similarity_score ORDER BY pairwise_similarity_score DESC
```
