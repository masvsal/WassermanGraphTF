
- always use create clause rather than merge when introducing new annotaiton node. This way, more annotations to a piece of informations is reflected int the graph rather than being merged into the same relationship. Also, for necessary for self-referential associations when we only use 1 annotation node to represent associations.


# CTDBase:

papers:
- CTDBase 2021 release summary
- https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0155811

CTDbase structure:
- manually curated associations: chemical disease, gene disease, gene chemical
- imported monthly from GO: gene-GO
- predicted interactions: chemical-GO, disease-GO

## Batch query - API:
link: http://ctdbase.org/help/linking.jsp#batchqueries


## Batch querying - Browser
Accepted Data types:
- Chemicals: MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. To limit your search to official names, use the “name:” prefix.
- Diseases: MeSH or OMIM name, synonym, or accession ID (“MESH:…” or “OMIM:…”). To limit your search to official names, use the “name:” prefix.
- Genes: NCBI (Entrez Gene) symbols (“name:…”) or accession IDs (“GENE:…”).
- Gene Ontology terms: name, synonym, or ID (e.g., “GO:0008219” or “8219”).
- Pathways: KEGG or REACTOME name or accession ID (“KEGG:…” or “REACT:…”).
- References: PubMed® IDs or DOIs.
- Phenotypes: phenotypic GO terms by name, synonym, or ID (e.g., “GO:0008219” or “8219”).

Filters: Select whether or not to return associations for all hierachical descendants of input data. 

Downloading chemical gene interactions:
- Filtering:
  - Degree: Increases, decreases, affect
  - Type: Type of gene function affected. Many different types.

Downloading gene associations:
- Inputs:
  - Gene: chamicals involved in curated interaction w genes
  - Disease: curated from literature or inferred using chemical-gene-disease interactions. 
  - Reference: retrieve chemicals-gene or chemical-disease associated with specific curated references
  - Phenotype: curated.
  - - GO: annotated to gene.

Downloading disease associations:
- Inputs:
  - Gene: diases involved in curated association w genes from literature or OMIM or inferred by 
  - Chemical: curated from literature or inferred using chemical-gene-disease interactions. 
  - Reference: retrieve chemicals-disease or gene-disease associated with specific curated references
  - Phenotype: curated.
  - GO: inferred to input GO term.

Downloading phenotype associations:
- Inputs:
  - Chemical: curated from literature
  -  Disease: inferred using gene-based inference networks
  - Reference: retrieve curated chemical and gene-phenotypes associations

Downloading pathway associations:
- Inputs:
  - Chemical: retrieves pathways containing curated gene associations with chemical. Can choose to further filter pathways to those only enriched significantly among genes associated with chemical.
  - Gene: Pathways containing genes based on annotation from KEGG and REACTOME
  - Disease: retrieves pathways containing curated gene associations based on KEGG and REACTOME curation

Downloading GO associations:
must select ontology
- Inputs:
  - Chemical: uses curated chem-gene interactions to retrieve annotations to any encoded gene products
  - Gene: Pathways containing genes based on annotation from KEGG and REACTOME
  - Disease: retrieves pathways containing curated gene associations based on KEGG and REACTOME curation

CTDbase only keeps record of GO annotations that are significantly enriched compared to baseline # of annotations. Further explanation:

CTD contains curated interactions between chemicals and genes/proteins. Many of these genes/proteins have Gene Ontology (GO) annotations that provide information about their associated biological processes, molecular functions, and cellular components. To provide insight into the biological properties that may be affected by a chemical, this report provides a list of GO terms that are statistically enriched among the genes/proteins that interact with the chemical or one of its descendants. GO terms are displayed in order of significance.

The significance of enrichment was calculated by the hypergeometric distribution and adjusted for multiple testing using the Bonferroni method.[1] The hypergeometric distribution is used to calculate the probability that the fraction of interacting genes annotated to the GO term or its descendants is significantly higher than the fraction of all human genes annotated to that GO term or its descendants in the genome.

For each enriched GO term with a Bonferroni p-value less than 0.01, the following information is displayed:

The ontology to which the GO term belongs (BP = Biological Process; CC = Cellular Component; MF = Molecular Function).
The highest level to which the GO term is assigned within the GO hierarchical ontology. Many GO terms are located at multiple levels within the ontology; only the highest level is displayed. Level 1 constitutes “children” of the most general Biological Process, Cellular Component, and Molecular Function terms.
The name of the enriched GO term associated with interacting genes. Each term is linked to additional information about the term.
The number of interacting genes with the associated GO term annotation or its descendants. Each number is linked to a list of the specific genes/proteins with this GO annotation.
The raw p-value.
The corrected p-value calculated using the Bonferroni multiple testing adjustment (see above).
The genome frequency: the fraction of genes in the genome annotated to the GO term or its descendants.
Sorting

Sort these data differently by clicking a column heading.

Download

Save these data into a comma-separated values (CSV), Excel, XML, or tab-separated values (TSV) file by clicking a Download link at the bottom of the table.

Top ↑ Footnotes
[1]
Boyle EI, Weng S, Gollub J, Jin H, Botstein D, Cherry JM, Sherlock G. GO::TermFinder—open source software for accessing Gene Ontology information and finding significantly enriched Gene Ontology terms associated with a list of genes. Bioinformatics. 2004 Dec 12;20(18):3710-5. PMID:15297299
Top ↑



- API = http://ctdbase.org/help/linking.jsp#batchqueries
- 
