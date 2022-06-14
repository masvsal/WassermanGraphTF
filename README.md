# WassermanGraphTF
Scripts and general code for GraphTF project. Used to integrate TF Annotation data and construct Neo4j graph database.
*Summer 2022*

*folder directories*

*graph schema*

*plan for future*

script for importing 1 way is ran from neo4j terminal. Arguments are passed into ImportProteins.sh. 

To import 1 way:
1. Download separate csv files containing protein annotations and interactions from from https://string-db.org/
2. Place files + importStringProteins1Way.cypher + ImportProteins.sh into import folder of appropriate neo4j database
3. In Neo4j terminal (from your databases home directory): run:
```
   ./import/ImportProteins.sh STRING_ANNOTATIONS.csv STRING_INTERACTIONS.csv DATABASE_NAME
```
where appropriate file names replace capitalized parameters.

To import GO annotations:
1. download appropriate .gaf from GO. 
2. Convert to .csv.
3. Insert the following headers from left to right:
A|DB	DB_Object_ID	B|DB_Object_Symbol	C|Qualifier	D|GO_ID	E|Reference	F|Evidence_Code	G|With_Or_From	H|Aspect	I|DB_Object_Name	J|DB_Object_Synonym	K|DB_Object_Type	L|Taxon	M|Date	N|Assigned_By	O|Annotation_Extension	P|Gene_Product_Form_ID![image](https://user-images.githubusercontent.com/95512439/170846823-e6f76b50-99d2-4389-a825-354e23702ea8.png)
3. in neo4j terminal, open cypher shell
4. run: 
```
:source import/importGOAnnot.cypher
```



TODO: 
1. allow user to choose to run 1way or 2way import. 
2. specify schema, add visualization
3. script for GO annotation import?
