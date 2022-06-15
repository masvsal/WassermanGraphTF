# WassermanGraphTF - Graphically Representing Transcription Factor Annotation

Scripts and general code for GraphTF database

Directories: <br/>
```bash
├── data_import:       #scripts for ingesting remote data into local csv files
│   ├── __pycache__ 
│   ├── biogrid_example_scripts #scripts from biogrid repository for interacting w REST API
│   ├── config #URL and passkeys needed to interact w various biological databases
│   └── core: #code to parse config YML file
│       └── __pycache__ 
├── graph_construction #scripts for constructing and populating new neo4j database instance
├── graph_data #files written to and parsed by graph import scripts
│   ├── entities #gene, transcript, protein data
│   ├── gene_annotations #transcription factor annotation data
│   │   └── cis-bp 
│   └── protein_interactions #protein interaction data
└── obsolete #old data files and scripts, not used in current graph model
    └── exampleDataset
 ```

Schema:
<img width="1247" alt="image" src="https://user-images.githubusercontent.com/95512439/173684845-3edaaa17-94b5-42c9-af90-bdc8f888b6e1.png">

Mapping genes to proteins:
![image](https://user-images.githubusercontent.com/95512439/173697408-51a8931b-a399-4c4d-a9af-e05f41411552.png)

Annotations:
- Canonical Gene->Protein Relationships are chosen by canonical transcript status and primary sequence status in ensembl. These criteria yield a single gene->transcript->protein pathway for every protein in yamanaka graph.
