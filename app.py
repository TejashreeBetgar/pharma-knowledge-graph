import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

# ---------------- CONFIG ----------------
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "pharma123"

st.set_page_config(page_title="Pharma Knowledge Graph", page_icon="🧬", layout="wide")

st.title("Pharma Knowledge Graph Explorer")
st.caption("Built with Neo4j · RDF/OWL Ontology · SNOMED CT · ICD-10 | Demo")
st.success("Use case: Drug discovery, target identification, and clinical decision support")

# ---------------- DB CONNECTION ----------------
@st.cache_resource
def get_driver():
    return GraphDatabase.driver(URI, auth=(USER, PASSWORD))

driver = get_driver()

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["Search", "Graph Queries", "Ontology", "Ask AI"])

# =========================================================
# 🟢 TAB 1: SEARCH (UNCHANGED)
# =========================================================
with tab1:
    st.subheader("Semantic Search")

    query = st.text_input("Type anything:", placeholder="e.g. Metformin, Diabetes, TNF...")

    if query:
        with driver.session() as s:
            results = s.run("""
                MATCH (n)
                WHERE toLower(n.name) CONTAINS toLower($q)
                RETURN labels(n)[0] AS Type,
                       n.name AS Name,
                       coalesce(n.icd10, n.snomed_code, n.full_name, '') AS Detail
                LIMIT 20
            """, q=query).data()

        if results:
            st.success(f"Found {len(results)} result(s)")
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.warning("No results found.")

    st.divider()
    st.subheader("All nodes in the graph")

    col1, col2, col3 = st.columns(3)

    with driver.session() as s:
        drugs = s.run("MATCH (d:Drug) RETURN d.name AS name, d.type AS type, d.snomed_code AS snomed").data()
        diseases = s.run("MATCH (d:Disease) RETURN d.name AS name, d.category AS category, d.icd10 AS icd10").data()
        genes = s.run("MATCH (g:Gene) RETURN g.name AS name, g.full_name AS full_name").data()

    with col1:
        st.markdown("### Drugs")
        st.dataframe(pd.DataFrame(drugs), use_container_width=True)

    with col2:
        st.markdown("### Diseases")
        st.dataframe(pd.DataFrame(diseases), use_container_width=True)

    with col3:
        st.markdown("### Genes")
        st.dataframe(pd.DataFrame(genes), use_container_width=True)

# =========================================================
# 🟢 TAB 2: GRAPH QUERIES (UNCHANGED)
# =========================================================
with tab2:
    st.subheader("Knowledge Graph Queries")

    q_type = st.selectbox("Choose a query:", [
        "What diseases does a drug treat?",
        "What genes does a drug target?",
        "Which drugs treat chronic diseases?",
        "Which drugs treat cancer?",
        "Show full drug pathway"
    ])

    drug_list = ["Metformin", "Imatinib", "Adalimumab", "Atorvastatin", "Pembrolizumab"]

    with driver.session() as s:
        if q_type == "What diseases does a drug treat?":
            drug = st.selectbox("Select drug:", drug_list)
            rows = s.run("""
                MATCH (d:Drug {name:$name})-[:TREATS]->(dis:Disease)
                RETURN d.name AS Drug, dis.name AS Disease, dis.icd10 AS ICD10, dis.category AS Category
            """, name=drug).data()

        elif q_type == "What genes does a drug target?":
            drug = st.selectbox("Select drug:", drug_list)
            rows = s.run("""
                MATCH (d:Drug {name:$name})-[:TARGETS]->(g:Gene)
                RETURN d.name AS Drug, g.name AS Gene, g.full_name AS Full_Name
            """, name=drug).data()

        elif q_type == "Which drugs treat chronic diseases?":
            rows = s.run("""
                MATCH (d:Drug)-[:TREATS]->(dis:Disease {category:'ChronicDisease'})
                RETURN d.name AS Drug, d.type AS Type, dis.name AS Disease, dis.icd10 AS ICD10
            """).data()

        elif q_type == "Which drugs treat cancer?":
            rows = s.run("""
                MATCH (d:Drug)-[:TREATS]->(dis:Disease {category:'Cancer'})
                RETURN d.name AS Drug, d.type AS Type, dis.name AS Disease, dis.icd10 AS ICD10
            """).data()

        else:
            drug = st.selectbox("Select drug:", drug_list)
            rows = s.run("""
                MATCH (d:Drug {name:$name})-[:TARGETS]->(g:Gene)-[:ASSOCIATED_WITH]->(dis:Disease)
                RETURN d.name AS Drug, g.name AS Gene, dis.name AS Disease, dis.icd10 AS ICD10
            """, name=drug).data()

        if rows:
            st.success(f"{len(rows)} result(s) found")
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.warning("No results.")

# =========================================================
# 🟢 TAB 3: ONTOLOGY (UNCHANGED)
# =========================================================
with tab3:
    st.subheader("RDF/OWL Ontology")

    try:
        with open("pharma_ontology.ttl", "r", encoding="utf-8") as f:
            st.code(f.read(), language="turtle")
    except FileNotFoundError:
        st.error("pharma_ontology.ttl not found.")

# =========================================================
# 🟢 TAB 4: ASK AI (FIXED)
# =========================================================
with tab4:
    st.subheader("Ask AI about the graph")

    question = st.text_input("Ask a question")

    if st.button("Ask AI"):
        if not question.strip():
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                try:
                    import requests

                    with driver.session() as session:
                        result = session.run("""
                            MATCH (d:Drug)-[:TREATS]->(dis:Disease)
                            RETURN d.name AS drug, dis.name AS disease
                            LIMIT 30
                        """)
                        data = list(result)

                    context = "\n".join(
                        [f"{r['drug']} treats {r['disease']}" for r in data]
                    )

                    prompt = f"""
Use ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "phi3:latest",
                            "prompt": prompt,
                            "stream": False
                        },
                        timeout=60
                    )

                    response.raise_for_status()

                    answer = response.json().get("response", "No response")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error: {e}")
