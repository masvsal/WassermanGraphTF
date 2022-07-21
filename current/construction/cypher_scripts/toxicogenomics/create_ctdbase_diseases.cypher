LOAD CSV WITH HEADERS
	FROM '$CDTBASE_GENE_DISEASE_URI' as line

MERGE (d:Disease {mesh_id: line.DiseaseID, name: line.DiseaseName, omim_id: coalesce(split(line.OmimIDs, '|'), 'NOT FOUND')})

WITH d,split(line.DiseaseCategories, '|') as category_list, line

UNWIND category_list as disease_category

MERGE (dc:Disease_Category {name:disease_category})

WITH d,dc, line

MERGE (d)-[:IN_CATEGORY]->(dc)

RETURN count(d) as count
;