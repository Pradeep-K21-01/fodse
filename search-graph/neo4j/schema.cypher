// search-graph/neo4j/schema.cypher
// Legal Knowledge Graph Schema
// Run this in Neo4j Browser or via cypher-shell
//
// Start Neo4j:
//   docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none neo4j
// Open browser: http://localhost:7474
// Run this file: cypher-shell -f schema.cypher

// ── Clear existing data ────────────────────────────────────────────────────
MATCH (n) DETACH DELETE n;

// ── Constraints (unique keys) ──────────────────────────────────────────────
CREATE CONSTRAINT law_name_unique IF NOT EXISTS
FOR (l:Law) REQUIRE l.name IS UNIQUE;

CREATE CONSTRAINT section_id_unique IF NOT EXISTS
FOR (s:Section) REQUIRE s.section_id IS UNIQUE;

CREATE CONSTRAINT crime_name_unique IF NOT EXISTS
FOR (c:Crime) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT punishment_id_unique IF NOT EXISTS
FOR (p:Punishment) REQUIRE p.id IS UNIQUE;

// ── Node: Laws ─────────────────────────────────────────────────────────────
CREATE (:Law {name: "Information Technology Act, 2000",     short: "IT Act",    year: 2000});
CREATE (:Law {name: "Indian Penal Code, 1860",              short: "IPC",       year: 1860});
CREATE (:Law {name: "Negotiable Instruments Act, 1881",     short: "NI Act",    year: 1881});
CREATE (:Law {name: "Consumer Protection Act, 2019",        short: "CPA",       year: 2019});
CREATE (:Law {name: "Motor Vehicles Act, 1988",             short: "MVA",       year: 1988});
CREATE (:Law {name: "Hindu Marriage Act, 1955",             short: "HMA",       year: 1955});
CREATE (:Law {name: "Indian Contract Act, 1872",            short: "ICA",       year: 1872});
CREATE (:Law {name: "Bharatiya Nyaya Sanhita, 2023",        short: "BNS",       year: 2023});

// ── Node: Sections ─────────────────────────────────────────────────────────
CREATE (:Section {section_id: "IT-66",   number: "66",   title: "Computer related offences",          law: "IT Act"});
CREATE (:Section {section_id: "IT-66A",  number: "66A",  title: "Offensive messages online",          law: "IT Act"});
CREATE (:Section {section_id: "IT-66B",  number: "66B",  title: "Stolen computer resource",           law: "IT Act"});
CREATE (:Section {section_id: "IT-66C",  number: "66C",  title: "Identity theft",                     law: "IT Act"});
CREATE (:Section {section_id: "IT-66D",  number: "66D",  title: "Cheating by impersonation online",   law: "IT Act"});
CREATE (:Section {section_id: "IT-67",   number: "67",   title: "Obscene material online",            law: "IT Act"});
CREATE (:Section {section_id: "NI-138",  number: "138",  title: "Cheque dishonour offence",           law: "NI Act"});
CREATE (:Section {section_id: "NI-139",  number: "139",  title: "Presumption in favour of holder",   law: "NI Act"});
CREATE (:Section {section_id: "NI-142",  number: "142",  title: "Cognisance of offences",             law: "NI Act"});
CREATE (:Section {section_id: "MV-184",  number: "184",  title: "Dangerous driving",                  law: "MVA"});
CREATE (:Section {section_id: "MV-185",  number: "185",  title: "Driving under influence",            law: "MVA"});
CREATE (:Section {section_id: "HM-13",   number: "13",   title: "Grounds for divorce",                law: "HMA"});
CREATE (:Section {section_id: "HM-24",   number: "24",   title: "Maintenance pendente lite",          law: "HMA"});
CREATE (:Section {section_id: "CP-35",   number: "35",   title: "Consumer complaint filing",          law: "CPA"});

// ── Node: Crimes ───────────────────────────────────────────────────────────
CREATE (:Crime {name: "Online fraud",       category: "cybercrime"});
CREATE (:Crime {name: "Identity theft",     category: "cybercrime"});
CREATE (:Crime {name: "Cheque bounce",      category: "financial"});
CREATE (:Crime {name: "Consumer fraud",     category: "consumer"});
CREATE (:Crime {name: "Drunk driving",      category: "traffic"});
CREATE (:Crime {name: "Divorce",            category: "family"});
CREATE (:Crime {name: "Contract breach",    category: "civil"});
CREATE (:Crime {name: "Data theft",         category: "cybercrime"});

// ── Node: Punishments ─────────────────────────────────────────────────────
CREATE (:Punishment {id: "P-IT66D",  description: "Up to 3 years imprisonment or fine up to Rs.1 lakh or both"});
CREATE (:Punishment {id: "P-IT66C",  description: "Up to 3 years imprisonment and fine up to Rs.1 lakh"});
CREATE (:Punishment {id: "P-NI138",  description: "Up to 2 years imprisonment or twice the cheque amount or both"});
CREATE (:Punishment {id: "P-MV185",  description: "First offence: Rs.10,000 fine or 6 months imprisonment"});
CREATE (:Punishment {id: "P-MV184",  description: "Up to 1 year imprisonment or Rs.5,000 fine"});

// ── Relationships ──────────────────────────────────────────────────────────

// Law → Section
MATCH (l:Law {short:"IT Act"}),  (s:Section {section_id:"IT-66"})  CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"IT Act"}),  (s:Section {section_id:"IT-66C"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"IT Act"}),  (s:Section {section_id:"IT-66D"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"IT Act"}),  (s:Section {section_id:"IT-67"})  CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"NI Act"}),  (s:Section {section_id:"NI-138"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"NI Act"}),  (s:Section {section_id:"NI-139"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"NI Act"}),  (s:Section {section_id:"NI-142"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"MVA"}),     (s:Section {section_id:"MV-184"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"MVA"}),     (s:Section {section_id:"MV-185"}) CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"HMA"}),     (s:Section {section_id:"HM-13"})  CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"HMA"}),     (s:Section {section_id:"HM-24"})  CREATE (l)-[:HAS_SECTION]->(s);
MATCH (l:Law {short:"CPA"}),     (s:Section {section_id:"CP-35"})  CREATE (l)-[:HAS_SECTION]->(s);

// Crime → Section
MATCH (c:Crime {name:"Online fraud"}),   (s:Section {section_id:"IT-66D"}) CREATE (c)-[:COVERED_UNDER]->(s);
MATCH (c:Crime {name:"Identity theft"}), (s:Section {section_id:"IT-66C"}) CREATE (c)-[:COVERED_UNDER]->(s);
MATCH (c:Crime {name:"Data theft"}),     (s:Section {section_id:"IT-66"})  CREATE (c)-[:COVERED_UNDER]->(s);
MATCH (c:Crime {name:"Cheque bounce"}),  (s:Section {section_id:"NI-138"}) CREATE (c)-[:COVERED_UNDER]->(s);
MATCH (c:Crime {name:"Drunk driving"}),  (s:Section {section_id:"MV-185"}) CREATE (c)-[:COVERED_UNDER]->(s);
MATCH (c:Crime {name:"Divorce"}),        (s:Section {section_id:"HM-13"})  CREATE (c)-[:COVERED_UNDER]->(s);
MATCH (c:Crime {name:"Consumer fraud"}), (s:Section {section_id:"CP-35"})  CREATE (c)-[:COVERED_UNDER]->(s);

// Section → Punishment
MATCH (s:Section {section_id:"IT-66D"}), (p:Punishment {id:"P-IT66D"}) CREATE (s)-[:CARRIES_PUNISHMENT]->(p);
MATCH (s:Section {section_id:"IT-66C"}), (p:Punishment {id:"P-IT66C"}) CREATE (s)-[:CARRIES_PUNISHMENT]->(p);
MATCH (s:Section {section_id:"NI-138"}), (p:Punishment {id:"P-NI138"}) CREATE (s)-[:CARRIES_PUNISHMENT]->(p);
MATCH (s:Section {section_id:"MV-185"}), (p:Punishment {id:"P-MV185"}) CREATE (s)-[:CARRIES_PUNISHMENT]->(p);
MATCH (s:Section {section_id:"MV-184"}), (p:Punishment {id:"P-MV184"}) CREATE (s)-[:CARRIES_PUNISHMENT]->(p);

// Superseded laws
MATCH (old:Law {short:"IPC"}), (new:Law {short:"BNS"})
CREATE (old)-[:SUPERSEDED_BY {year: 2023}]->(new);