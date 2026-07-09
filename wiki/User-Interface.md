# 🖥️ User Interface Guide

HECTOR-Editor features a responsive two-column interface designed to adapt cleanly to various screen sizes.

```
+------------------------------------------+------------------------------------------+
|  LEFT PANEL: NAVIGATION & TOOLS          |  RIGHT PANEL: CONCEPT EDITOR             |
|  - App Header & Theme Switcher           |  - Concept URI Input                     |
|  - File Actions (Load, Create)           |  - Pref Labels / Alt Labels              |
|  - Hierarchical Treeview                 |  - Multilingual Definitions              |
|  - Data Quality Panel (Integrity Checks) |  - Authority Mappings (Wikidata, AAT...) |
|  - Log Console (Runtime logs)            |  - Broader Parents Selection List        |
+------------------------------------------+------------------------------------------+
```

## Left Panel: Navigation & Tools

The Left Panel contains file system controls, the navigation tree, and data quality check utilities.

### 1. App Identity Header
* Displays the HECTOR-Editor logo.
* Contains the **Dark Mode** toggle switch to instantly shift between dark and light appearance modes.

### 2. File Action Buttons
* **Open Main Vocabulary (.ttl):** Load an existing RDF SKOS Turtle file.
* **Create New Vocabulary:** Initialize a brand new concept scheme with a custom namespace.
* **Import Facet / Sub-Vocabulary (.ttl):** Load a separate branch to merge into the active vocabulary.

### 3. Hierarchical Treeview
* Visualizes the concept scheme.
* Chronologically sorts chronological epochs, centuries, quarters, and halves according to their German labels.
* Selecting a concept loads its metadata immediately into the Right Panel.

### 4. Data Quality Checks
* Quick action tools to audit and maintain graph consistency (e.g. Sync relations, Repair labels, Orphan check).

### 5. Log Console
* A read-only console displaying terminal logs, execution updates, API requests, and warning messages in real-time.

---

## Right Panel: Concept Editor

The Right Panel is the editing form for the currently active concept.

### 1. Concept URI & ID
* Displays the URI of the concept. For new concepts, a unique UUID is generated.
* **Is Top Concept of Scheme:** Checkbox to declare the concept as a root-level concept (`skos:hasTopConcept`).

### 2. Labels & Language Tabs
* Multi-tab section to define **Preferred Labels (`skos:prefLabel`)** and **Alternative Labels (`skos:altLabel`)** for active language tags (e.g., German `de` and English `en`).

### 3. Definitions
* Multi-line input fields to provide semantic descriptions (`skos:definition`) in multiple languages.

### 4. Semantic Alignments (Exact Match Mappings)
* Input fields and query buttons to link the concept with external authority registries:
  * **Wikidata Match (`skos:exactMatch`):** Query Wikidata API.
  * **Getty AAT Match (`skos:exactMatch`):** Query Getty Art & Architecture Thesaurus.
  * **GND Match (`skos:exactMatch`):** Query Gemeinsame Normdatei.

### 5. Broader Parents
* A selection list displaying all loaded concepts. You can link a concept to one or more parents to support **polyhierarchies**.
