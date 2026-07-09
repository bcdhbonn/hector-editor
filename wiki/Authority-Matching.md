# 🔗 Authority Matching & Semantic Web Alignment

Aligning local SKOS concepts with authoritative global identifiers (such as Wikidata, Getty AAT, or GND) is essential for Linked Open Data (LOD) and semantic web workflows. HECTOR-Editor features asynchronous API integrations to query and apply these mappings.

---

## 🌐 Wikidata Alignment

Wikidata is a collaborative, multilingual knowledge base.

### Aligning a Concept with Wikidata:
1. Enter the concept's labels in the editor.
2. Click **🔍 Query Wikidata API** next to the Wikidata Match field.
3. HECTOR-Editor queries the Wikidata search API using the current active tree language.
4. An entity disambiguation popup window appears, listing the top 15 results (Entity ID, label, and description).
5. Click **Select Entity** next to the correct entry.
6. The Wikidata URI (e.g. `http://www.wikidata.org/entity/Q2277`) is inserted into the **Wikidata Match** input field.
7. Click **💾 Save Concept** to commit. The link is serialized as a `skos:exactMatch` statement.

---

## 🏛️ Getty AAT Alignment

The Getty Art & Architecture Thesaurus (AAT) is a structured vocabulary for art and heritage terms.

### Aligning a Concept with Getty AAT:
1. Click **🔍 Query Getty AAT** next to the Getty AAT Match field.
2. The editor queries the Getty AAT web service based on the label.
3. Select the matching concept from the disambiguation popup.
4. The exact match URI is added to the form and saved.

---

## 🗃️ GND Alignment

The Gemeinsame Normdatei (GND) is the German authority file for persons, corporate bodies, subject headings, and places, managed by the German National Library.

### Aligning a Concept with GND:
1. Click **🔍 Query GND API** next to the GND Match field.
2. Select the matching entry from the library authority search records.
3. The GND URI (e.g. `http://d-nb.info/gnd/...`) is populated in the form.
