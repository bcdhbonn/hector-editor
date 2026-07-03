# HECTOR Epoch SKOS Vocabulary

This directory contains the compiled and integrated SKOS vocabulary: **`HECTOR_Epoch.ttl`**.

---

## 🌐 Namespace & URI Scheme

* **Base Namespace:** `http://vocabs.bcdh.uni-bonn.de/hector_epochs/`
* **Namespace Prefix:** `hector_epochs`
* **Abstract URIs:** To ensure URI stability and decoupling from human-readable labels, all concepts use abstract, opaque URIs of the format:
  `http://vocabs.bcdh.uni-bonn.de/hector_epochs/c_<hash>`
  * The `c_<hash>` represents a stable, 8-character SHA-256 hash computed from the concept's original semantic identifier.

---

## 📂 Vocabulary Facets

The vocabulary integrates five main semantic facets:

1. **Core baseline epochs:** The fundamental archaeological epochs (Stone Age, Copper Age, Bronze Age, Iron Age, Classical Antiquity, Middle Ages, Modern Period) based on the original OWL baseline ontology.
2. **Chronological grid:** A fine-grained temporal grid consisting of Millennia, Centuries, and their respective Halves and Quarters spanning from 3000 BC to the present.
3. **Roman Imperial period:** 106 Roman emperors, chronologically classified into the *Early*, *Middle*, and *Late* Imperial periods based on their date of reign/death.
4. **Medieval dynasties:** A detailed regional and dynastic categorization of 86 medieval rulers across five European realms:
   * **Holy Roman Empire:** Ottonian, Salian, Hohenstaufen, Luxembourg, and Habsburg dynasties.
   * **England:** Norman, Plantagenet, Lancaster, and York dynasties.
   * **France:** Capetian and Valois dynasties.
   * **Spain:** House of Burgundy and House of Trastámara.
   * **Italy:** House of Hauteville and House of Anjou.
5. **Ancient Egypt:** A comprehensive hierarchical classification of Ancient Egypt comprising:
   * **Kingdoms & Intermediate Periods:** Old Kingdom, New Kingdom, etc.
   * **Dynasties:** Dynasties 1 to 31 and the Ptolemaic period.
   * **Rulers:** 524 Pharaohs nested under their respective dynasties.

---

## 🔗 Authority File Alignments

All rulers and core epochs are enriched with descriptions and exact matches (`skos:exactMatch`) to global authority files:
* **Wikidata URIs** (e.g., `http://www.wikidata.org/entity/Q...`)
* **Gemeinsame Normdaten (GND) URIs** (e.g., `http://d-nb.info/gnd/...`)
* **Getty Art & Architecture Thesaurus (AAT) URIs** (e.g., `http://vocab.getty.edu/aat/...`)
