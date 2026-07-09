# 🛠️ Data Quality & Integrity Checks

HECTOR-Editor provides automatic and manual diagnostic tools to audit, clean, and synchronize graphs, ensuring high data quality and schema compliance.

---

## 🔄 Reciprocal Relationship Synchronization

### What are Reciprocal Relations?
In SKOS, relationships should be symmetrical between parents and children:
* If Concept A has Oberbegriff (`skos:broader`) Concept B.
* Then Concept B must have Unterbegriff (`skos:narrower`) Concept A.

If only one side of the relationship exists, the hierarchy is broken and may fail to load correctly in third-party semantic tools or repositories.

### Running Symmetrical Sync:
HECTOR-Editor does this dynamically when saving concepts. However, if you import files created by external tools that lack these relations:
1. Go to the **Data Quality / Integrity Checks** panel on the left.
2. Click the **🔄 Sync Broader/Narrower** button.
3. The editor scans the graph, identifies all unidirectional links, inserts the missing reciprocal triples, and serializes the updated vocabulary to disk.
4. The output log will report how many reciprocal connections were generated.

---

## 🔧 Repair Missing URI Labels

### The Problem:
Sometimes concepts in imported vocabularies contain valid URIs but lack readable `skos:prefLabel` records. This causes them to show up as blank or raw URIs in the navigation tree.

### Running Label Repair:
1. Click the **🔧 Repair Missing URI Labels** button.
2. The editor identifies all concepts missing a preferred label.
3. It parses the local part of the concept URI (the segment following the `#` or final `/`) and generates an English preferred label from it.
4. The updated graph is saved, and the treeview is refreshed.

---

## 🔍 Orphan & Scheme Integrity Health Check

### The Problem:
An "orphan" concept is a concept that is disconnected from the main scheme:
* It has no parent concept (`skos:broader`).
* It is not declared as a top concept of the scheme (`skos:topConceptOf` or `skos:hasTopConcept`).

Orphans exist in the database but are invisible in hierarchical tree navigators.

### Running the Health Check:
1. Click **🔍 Run Health Check**.
2. The editor runs a diagnostic check on the graph.
3. If orphans are found, their URIs and labels are printed in red/warning colors in the **Log Console**.
4. You can search for these URIs, load them in the editor, and assign them a parent or mark them as top concepts to reconnect them.
