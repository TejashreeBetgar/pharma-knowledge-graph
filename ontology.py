from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef

# Think of a Namespace like a prefix for all your concept names
PHARMA = Namespace("http://novartis-kg.org/pharma#")
SNOMED = Namespace("http://snomed.info/id/")

def build_ontology():
    g = Graph()
    g.bind("pharma", PHARMA)
    g.bind("snomed", SNOMED)
    g.bind("owl", OWL)

    # === DEFINE CLASSES (like categories in your dictionary) ===
    # "Drug is a Thing"
    g.add((PHARMA.Drug,         RDF.type,        OWL.Class))
    g.add((PHARMA.Drug,         RDFS.label,      Literal("Drug")))
    g.add((PHARMA.Drug,         RDFS.comment,    Literal("A pharmaceutical compound used in treatment")))

    # "Disease is a Thing"
    g.add((PHARMA.Disease,      RDF.type,        OWL.Class))
    g.add((PHARMA.Disease,      RDFS.label,      Literal("Disease")))

    # "Gene is a Thing"
    g.add((PHARMA.Gene,         RDF.type,        OWL.Class))
    g.add((PHARMA.Gene,         RDFS.label,      Literal("Gene")))

    # "ChronicDisease IS-A Disease" (subclass relationship)
    g.add((PHARMA.ChronicDisease, RDF.type,      OWL.Class))
    g.add((PHARMA.ChronicDisease, RDFS.subClassOf, PHARMA.Disease))
    g.add((PHARMA.ChronicDisease, RDFS.label,    Literal("Chronic Disease")))

    # === DEFINE PROPERTIES (the relationships between classes) ===
    # "treats" connects Drug → Disease
    g.add((PHARMA.treats,       RDF.type,        OWL.ObjectProperty))
    g.add((PHARMA.treats,       RDFS.domain,     PHARMA.Drug))
    g.add((PHARMA.treats,       RDFS.range,      PHARMA.Disease))
    g.add((PHARMA.treats,       RDFS.label,      Literal("treats")))

    # "targets" connects Drug → Gene
    g.add((PHARMA.targets,      RDF.type,        OWL.ObjectProperty))
    g.add((PHARMA.targets,      RDFS.domain,     PHARMA.Drug))
    g.add((PHARMA.targets,      RDFS.range,      PHARMA.Gene))
    g.add((PHARMA.targets,      RDFS.label,      Literal("targets")))

    # "associatedWith" connects Gene → Disease
    g.add((PHARMA.associatedWith, RDF.type,      OWL.ObjectProperty))
    g.add((PHARMA.associatedWith, RDFS.domain,   PHARMA.Gene))
    g.add((PHARMA.associatedWith, RDFS.range,    PHARMA.Disease))

    # Save the ontology as a file (Turtle format — human readable RDF)
    g.serialize("pharma_ontology.ttl", format="turtle")
    print("Ontology built and saved to pharma_ontology.ttl")
    return g

if __name__ == "__main__":
    build_ontology()