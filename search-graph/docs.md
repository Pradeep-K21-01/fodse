# Search + Knowledge Graph — Member 5 Guide

## What you own
- `elasticsearch/` — keyword search index for legal documents
- `neo4j/` — legal knowledge graph (laws → sections → crimes → punishments)

## Setup order

### Step 1 — Start services
```bash
# Elasticsearch
docker run -d -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.13.0

# Neo4j
docker run -d -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=none neo4j
```

### Step 2 — Install dependencies
```bash
pip install elasticsearch neo4j
```

### Step 3 — Run Elasticsearch setup
```bash
python elasticsearch/setup_index.py
```
This reads all JSON files from `data-engineering/structured_json/` and indexes them.

### Step 4 — Run Neo4j schema
```bash
python neo4j/import_data.py
```
This builds the legal knowledge graph with 8 laws, 15+ sections, crimes, and punishments.

### Step 5 — Verify
- Elasticsearch: http://localhost:9200/legal_docs/_count
- Neo4j Browser: http://localhost:7474
  - Run: `MATCH (n) RETURN n LIMIT 50`

## How it connects to the AI engine

The `elastic_client.py` in `ai/retrieval/` queries Elasticsearch for keyword matches.
The `queries.py` in `neo4j/` enriches answers with structured legal relationships.

Both results are merged by `reranker.py` using Reciprocal Rank Fusion before going to the LLM.

## Graph structure

```
Law ──HAS_SECTION──► Section ──CARRIES_PUNISHMENT──► Punishment
                        ▲
Crime ──COVERED_UNDER───┘

Law ──SUPERSEDED_BY──► Law
```

## Example queries in Neo4j Browser

```cypher
-- Find all sections for cheque bounce
MATCH (c:Crime {name:"Cheque bounce"})-[:COVERED_UNDER]->(s:Section)
RETURN c, s

-- Find punishment for IT Act 66D
MATCH (s:Section {section_id:"IT-66D"})-[:CARRIES_PUNISHMENT]->(p)
RETURN s.title, p.description

-- Check superseded laws
MATCH (old:Law)-[:SUPERSEDED_BY]->(new:Law)
RETURN old.name, new.name
```