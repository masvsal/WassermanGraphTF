// LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/masvsal/WassermanGraphTF/main/current/data/gene_annotations/TFClass.csv' as line
// RETURN line.Quality as quality, line.Model as model, line.HGNC, line.Model_length, line.TFclass, line.TF_familys

match (n) detach delete n;