# WassermanGraphTF
Scripts and general code for GraphTF project. Used to integrate TF Annotation data and construct Neo4j graph database.
*Summer 2022*

*folder directories*

*graph schema*

*plan for future*

script for importing 1 way is ran from neo4j terminal. Arguments are passed into ImportProteins.sh. 

In order to succesfully import 1 way:
1. Download separate csv files containing protein annotations and interactions from from https://string-db.org/
2. Place files + importStringProteins1Way.cypher + ImportProteins.sh into import folder of appropriate neo4j database
3. from home folder of neo4j database, run the following command:
   ./import/ImportProteins.sh STRING_ANNOTATIONS.csv STRING_INTERACTIONS.csv DATABASE_NAME
where where the appropriate names replace capitalized names.

TODO: 
1. allow user to choose to run 1way or 2way import. 
2. specify schema, add visualization
3. script for GO annotation import?
