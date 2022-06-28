LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/masvsal/WassermanGraphTF/main/current/data/gene_annotations/namayura_GAF_Pruned.csv' AS line
RETURN collect(line.DB_Object_ID) as t