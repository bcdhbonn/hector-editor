# BCDH Heritage Assets SKOS Vocabulary

This directory contains the compiled and integrated SKOS vocabulary: **`heritage_assets.ttl`**.

---

## 🌐 Namespace & URI Scheme

* **Base Namespace:** `http://vocabs.bcdh.uni-bonn.de/heritage_assets/`
* **Namespace Prefix:** `th`
* **URIs:** To ensure URI stability and decoupling from human-readable labels, all concepts use identifiers of the format:
  `http://vocabs.bcdh.uni-bonn.de/heritage_assets/<concept_id>`
  * The `<concept_id>` represents a unique, stable, and human-readable identifier (e.g., `amphora`, `koilon`, `red-figure`).

---

## 📂 Vocabulary Facets & Focus

The vocabulary contains a hierarchical classification of cultural heritage assets, architecture, ceramic wares, historical peoples, and artistic/mythological representation subjects. **The current focus of this vocabulary is on the classical archaeology of the Mediterranean region (Mittelmeerraum).**

It integrates the following core facets:

1. **Behälter (Container):** 
   * A comprehensive classification of ancient vessel forms, focusing particularly on ancient Greek, Etruscan, and Roman pottery shapes (e.g., amphorae, lekythoi, kraters, hydriai, pyxides, cups, and bowls).
2. **Töpferware (Ceramics Wares & Styles):**
   * Regional and stylistic divisions of ancient Mediterranean pottery (e.g., Corinthian ceramics, Attic black-figure and red-figure styles, Apulian, Campanian, Messapian, Daunian, and Peucetian wares, as well as Etruscan Bucchero).
3. **Vasenmaler (Vase Painters):**
   * Hierarchical listings of ancient Greek and Roman vase painters and potter groups (e.g., Achilles Painter, Athena Painter, Theseus Painter, Berlin Painter).
4. **Plastik (Sculptures & Decors):**
   * Classical sculptural categories (statuettes/figurines, statues, portraiture, reliefs) and architectural-sculptural elements (e.g., acroteria, peplophoroi).
5. **Architektur und Urbanistik (Architecture & Urbanism):**
   * Ancient building typologies (temples, theaters, catacombs, curias, fortifications) and specific structural components (columns, capitals, bases, cornices, roofing systems).
6. **Kulturen (Cultures & Peoples):**
   * Ancient Mediterranean tribes, peoples, and civilizational categories (e.g., Sicani/Sikaner, Siculi/Sikuler, Romans, Greeks, Minoans, Carthaginians, Iberians, Ligurians, and Germanic tribes).
7. **Bildthema (Subject & Iconography):**
   * Mythological and narrative iconographies depicted on ancient artifacts (e.g., the Giant Fight/Gigantomachy, individual Giants like Agrios and Alcyoneus, Theseus with Minos, and Cadmus).
8. **Schuhwerk (Footwear):**
   * Typological classification of ancient footwear, divided into:
     * **Griechischer Schuh (Greek footwear):** e.g., arbyle, embas, iphikratides.
     * **Römischer Schuh (Roman footwear):** e.g., caliga, crepida, gallica, pero, soccus.
9. **Stoff (Material):**
   * Raw materials used in the production of heritage assets, including metals, glass, ores, and organic materials (e.g., bone, ivory, wood, leather).
10. **Ornament:**
    * Decorative patterns, friezes, and motifs (geometric, floral, and figurative) used on ancient architecture and pottery.

---

## 🔗 Authority File Alignments

Core concepts are enriched with labels, scope notes (definitions), and exact matches (`skos:exactMatch`) to global authority files:
* **Wikidata URIs** (e.g., `http://www.wikidata.org/entity/Q...`)
* **Gemeinsame Normdaten (GND) URIs** (e.g., `https://d-nb.info/gnd/...`)
* **Getty Art & Architecture Thesaurus (AAT) URIs** (e.g., `http://vocab.getty.edu/aat/...`)
