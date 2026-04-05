from neo4j import GraphDatabase

URI      = "bolt://localhost:7687"
USER     = "neo4j"
PASSWORD = "pharma123"    # ← change this if your password is different

DATA = {
    "drugs": [
        {"id":"D001","name":"Metformin",    "type":"SmallMolecule","snomed_code":"372501008"},
        {"id":"D002","name":"Imatinib",     "type":"SmallMolecule","snomed_code":"414460008"},
        {"id":"D003","name":"Adalimumab",   "type":"Biologic",     "snomed_code":"407317001"},
        {"id":"D004","name":"Atorvastatin", "type":"SmallMolecule","snomed_code":"372912004"},
        {"id":"D005","name":"Pembrolizumab","type":"Biologic",     "snomed_code":"716123008"},
    ],
    "diseases": [
        {"id":"DIS001","name":"Type 2 Diabetes",         "category":"ChronicDisease","icd10":"E11"},
        {"id":"DIS002","name":"Chronic Myeloid Leukemia","category":"Cancer",        "icd10":"C92.1"},
        {"id":"DIS003","name":"Rheumatoid Arthritis",    "category":"ChronicDisease","icd10":"M06"},
        {"id":"DIS004","name":"Hypercholesterolemia",    "category":"ChronicDisease","icd10":"E78.0"},
        {"id":"DIS005","name":"Melanoma",                "category":"Cancer",        "icd10":"C43"},
    ],
    "genes": [
        {"id":"G001","name":"AMPK",   "full_name":"AMP-activated protein kinase"},
        {"id":"G002","name":"BCR-ABL","full_name":"Breakpoint cluster region-Abelson"},
        {"id":"G003","name":"TNF",    "full_name":"Tumor Necrosis Factor"},
        {"id":"G004","name":"HMGCR",  "full_name":"HMG-CoA Reductase"},
        {"id":"G005","name":"PD-1",   "full_name":"Programmed Death-1"},
    ],
    "drug_treats_disease": [
        ("D001","DIS001"),("D002","DIS002"),
        ("D003","DIS003"),("D004","DIS004"),("D005","DIS005"),
    ],
    "drug_targets_gene": [
        ("D001","G001"),("D002","G002"),
        ("D003","G003"),("D004","G004"),("D005","G005"),
    ],
    "gene_associated_with_disease": [
        ("G001","DIS001"),("G002","DIS002"),
        ("G003","DIS003"),("G004","DIS004"),("G005","DIS005"),
    ],
}

def load_data():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:

        print("Clearing old data...")
        session.run("MATCH (n) DETACH DELETE n")

        for drug in DATA["drugs"]:
            session.run("""
                CREATE (d:Drug {
                    id:$id, name:$name,
                    type:$type, snomed_code:$snomed_code
                })
            """, **drug)
        print(f"Loaded {len(DATA['drugs'])} drugs")

        for disease in DATA["diseases"]:
            session.run("""
                CREATE (d:Disease {
                    id:$id, name:$name,
                    category:$category, icd10:$icd10
                })
            """, **disease)
        print(f"Loaded {len(DATA['diseases'])} diseases")

        for gene in DATA["genes"]:
            session.run("""
                CREATE (g:Gene {
                    id:$id, name:$name, full_name:$full_name
                })
            """, **gene)
        print(f"Loaded {len(DATA['genes'])} genes")

        for drug_id, disease_id in DATA["drug_treats_disease"]:
            session.run("""
                MATCH (d:Drug {id:$drug_id})
                MATCH (dis:Disease {id:$disease_id})
                CREATE (d)-[:TREATS]->(dis)
            """, drug_id=drug_id, disease_id=disease_id)

        for drug_id, gene_id in DATA["drug_targets_gene"]:
            session.run("""
                MATCH (d:Drug {id:$drug_id})
                MATCH (g:Gene {id:$gene_id})
                CREATE (d)-[:TARGETS]->(g)
            """, drug_id=drug_id, gene_id=gene_id)

        for gene_id, disease_id in DATA["gene_associated_with_disease"]:
            session.run("""
                MATCH (g:Gene {id:$gene_id})
                MATCH (d:Disease {id:$disease_id})
                CREATE (g)-[:ASSOCIATED_WITH]->(d)
            """, gene_id=gene_id, disease_id=disease_id)

        print("All relationships created!")
        print("\nSuccess! Your pharma knowledge graph is loaded.")
        print("Go to Neo4j Query tab and run:  MATCH (n) RETURN n LIMIT 50")

    driver.close()

if __name__ == "__main__":
    load_data()