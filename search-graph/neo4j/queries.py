"""
search-graph/neo4j/queries.py
Reusable Neo4j query functions used by the AI engine
to enrich answers with graph-based legal relationships.

Install: pip install neo4j
"""

import os
from neo4j import GraphDatabase

NEO4J_URI  = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "")

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        auth   = (NEO4J_USER, NEO4J_PASS) if NEO4J_PASS else ("neo4j", "")
        _driver = GraphDatabase.driver(NEO4J_URI, auth=auth)
    return _driver


# ── Query 1: Get sections for a crime keyword ──────────────────────────────

def get_sections_for_crime(keyword: str) -> list[dict]:
    """
    Find all law sections related to a crime keyword.

    Example:
        get_sections_for_crime("cheque bounce")
        → [{"crime": "Cheque bounce", "section": "138", "law": "NI Act",
            "title": "Cheque dishonour offence", "punishment": "..."}]
    """
    query = """
    MATCH (c:Crime)-[:COVERED_UNDER]->(s:Section)<-[:HAS_SECTION]-(l:Law)
    WHERE toLower(c.name) CONTAINS toLower($keyword)
       OR toLower(s.title) CONTAINS toLower($keyword)
    OPTIONAL MATCH (s)-[:CARRIES_PUNISHMENT]->(p:Punishment)
    RETURN c.name AS crime, s.number AS section,
           l.name AS law, s.title AS title,
           p.description AS punishment
    LIMIT 5
    """
    with get_driver().session() as session:
        result = session.run(query, keyword=keyword)
        return [dict(r) for r in result]


# ── Query 2: Get all sections for a law ────────────────────────────────────

def get_law_sections(law_short: str) -> list[dict]:
    """
    Get all sections of a law by short name.

    Example:
        get_law_sections("NI Act")
        → [{"section": "138", "title": "Cheque dishonour", ...}]
    """
    query = """
    MATCH (l:Law {short: $short})-[:HAS_SECTION]->(s:Section)
    OPTIONAL MATCH (s)-[:CARRIES_PUNISHMENT]->(p:Punishment)
    RETURN s.number AS section, s.title AS title,
           p.description AS punishment
    ORDER BY s.number
    """
    with get_driver().session() as session:
        result = session.run(query, short=law_short)
        return [dict(r) for r in result]


# ── Query 3: Check if a law was superseded ─────────────────────────────────

def get_superseded_law(law_short: str) -> dict | None:
    """
    Check if a law has been replaced by a newer one.

    Example:
        get_superseded_law("IPC")
        → {"old": "IPC", "new": "BNS", "year": 2023}
    """
    query = """
    MATCH (old:Law {short: $short})-[r:SUPERSEDED_BY]->(new:Law)
    RETURN old.short AS old, new.short AS new,
           new.name AS new_full, r.year AS year
    """
    with get_driver().session() as session:
        result = session.run(query, short=law_short)
        row    = result.single()
        return dict(row) if row else None


# ── Query 4: Graph-enriched context for RAG ────────────────────────────────

def enrich_query_with_graph(query: str) -> str:
    """
    Given a user query, find related law sections from the graph
    and return them as a text string to append to the RAG context.

    Used by legal_agent.py to add structured legal references.
    """
    # Extract keywords for graph lookup
    keywords = [w for w in query.lower().split() if len(w) > 4]

    enrichment_parts = []
    for kw in keywords[:3]:   # check top 3 keywords
        sections = get_sections_for_crime(kw)
        for s in sections:
            if s.get("section") and s.get("law"):
                line = (
                    f"[Graph] {s['law']} Section {s['section']}: {s['title']}"
                )
                if s.get("punishment"):
                    line += f" — Punishment: {s['punishment']}"
                enrichment_parts.append(line)

    return "\n".join(enrichment_parts) if enrichment_parts else ""