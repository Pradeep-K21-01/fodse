"""
search-graph/neo4j/import_data.py
Connects to Neo4j and runs schema.cypher to build the legal knowledge graph.

Install: pip install neo4j
Run:     python neo4j/import_data.py

Requires: Neo4j running
  docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none neo4j
"""

import os
from pathlib import Path
from neo4j import GraphDatabase

NEO4J_URI  = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "")

SCHEMA_FILE = Path(__file__).parent / "schema.cypher"


def run_schema(driver):
    """Execute each Cypher statement from schema.cypher."""
    cypher = SCHEMA_FILE.read_text(encoding="utf-8")

    # Split on semicolons, skip comments and blanks
    statements = [
        s.strip() for s in cypher.split(";")
        if s.strip() and not s.strip().startswith("//")
    ]

    with driver.session() as session:
        for i, stmt in enumerate(statements, 1):
            try:
                session.run(stmt)
                print(f"  [{i}/{len(statements)}] ✅  {stmt[:60]}...")
            except Exception as e:
                print(f"  [{i}/{len(statements)}] ❌  {e} — stmt: {stmt[:60]}")


def verify(driver):
    """Print node and relationship counts."""
    with driver.session() as session:
        laws    = session.run("MATCH (l:Law) RETURN count(l) AS c").single()["c"]
        sects   = session.run("MATCH (s:Section) RETURN count(s) AS c").single()["c"]
        crimes  = session.run("MATCH (c:Crime) RETURN count(c) AS c").single()["c"]
        rels    = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]

    print(f"\n[Neo4j] Graph summary:")
    print(f"  Laws        : {laws}")
    print(f"  Sections    : {sects}")
    print(f"  Crimes      : {crimes}")
    print(f"  Relationships: {rels}")
    print("\n[Neo4j] Knowledge graph ready ✅\n")


def main():
    print(f"[Neo4j] Connecting to {NEO4J_URI} ...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS) if NEO4J_PASS else ("neo4j", ""))

    try:
        driver.verify_connectivity()
        print("[Neo4j] Connected ✅\n")
        print("[Neo4j] Running schema.cypher ...")
        run_schema(driver)
        verify(driver)
    finally:
        driver.close()


if __name__ == "__main__":
    main()