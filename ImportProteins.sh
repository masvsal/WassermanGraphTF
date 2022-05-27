#!/bin/bash

cat import/importStringProteins1Way.cypher | sed s/ANNOT_FILE/$1/g | sed s/INTERACT_FILE/$2/g | sed s/DATABASE_NAME/$3/g | bin/cypher-shell -u neo4j -p 123

Echo Cypher Complete!