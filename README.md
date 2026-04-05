# Pharma Knowledge Graph

A healthcare knowledge graph built with Neo4j, RDF/OWL Ontology, SNOMED CT, and ICD-10 codes — with a Streamlit search interface.

## What this project demonstrates
- RDF/OWL ontology engineering (Drug, Disease, Gene classes with formal properties)
- Property graph modeling in Neo4j (15 nodes, 15 relationships)
- Healthcare terminology alignment (SNOMED CT + ICD-10)
- Semantic search across drugs, diseases, and genes
- Stakeholder-facing web app built with Streamlit

## Tech stack
- Python 3.9
- Neo4j 2025 (graph database)
- RDFLib (ontology / RDF triples)
- Streamlit (web app)
- Cypher (graph queries)

## Files
- `ontology.py` — builds the RDF/OWL ontology and saves as Turtle (.ttl)
- `load_graph.py` — loads drugs, diseases, genes into Neo4j
- `app.py` — Streamlit web app with search and query interface
- `pharma_ontology.ttl` — the generated RDF ontology file

## How to run

### 1. Install dependencies
pip install neo4j rdflib streamlit pandas

### 2. Start Neo4j Desktop and create an instance called pharma-graph

### 3. Build the ontology
python ontology.py

### 4. Load the graph data
python load_graph.py

### 5. Run the app
streamlit run app.py

## Knowledge graph structure

Nodes: Drug, Disease, Gene

Relationships:
- Drug -[TREATS]-> Disease
- Drug -[TARGETS]-> Gene  
- Gene -[ASSOCIATED_WITH]-> Disease

## Sample drugs and diseases

| Drug | Disease | ICD-10 |
|------|---------|--------|
| Metformin | Type 2 Diabetes | E11 |
| Imatinib | Chronic Myeloid Leukemia | C92.1 |
| Adalimumab | Rheumatoid Arthritis | M06 |
| Atorvastatin | Hypercholesterolemia | E78.0 |
| Pembrolizumab | Melanoma | C43 |

## Built for
Novartis Senior Semantic Engineer interview demonstration