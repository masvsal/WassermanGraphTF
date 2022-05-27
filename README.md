# WassermanGraphTF
Scripts and general code for creating graph database of TF. Summer 2022

script for importing 1 way is ran from neo4j terminal. Arguments are passed into ImportProteins.sh. 

In order to succesfully import 1 way:
1. Download separate csv files containing protein annotations and interactions from place separate csv files containing annotations and interactions from https://string-db.org/
2. Place files + importStringProteins1Way.cypher + ImportProteins.sh into import folder of appropriate neo4j database
3. from home folder of neo4j database, run the following command:
   ./import/ImportProteins.sh STRING_ANNOTATIONS.csv STRING_INTERACTIONS.csv DATABASE_NAME
where where the appropriate names replace capitalized names.
