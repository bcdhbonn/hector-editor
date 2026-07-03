# HECTOR-Editor & Epochen-Vokabular

HECTOR-Editor is a lightweight, responsive desktop application built with Python and CustomTkinter for managing semantic SKOS vocabularies. Tailored for workflows in the Digital Humanities and archaeological data management, it allows researchers to easily build, edit, and serialize structured hierarchical concept schemes.

---

## 📂 Vokabular-Struktur (`vocabularies/`)

Das fertige, integrierte SKOS-Vokabular befindet sich im Ordner `vocabularies/` und ist als **`HECTOR_Epoch.ttl`** serialisiert. Es ist im Namespace `http://vocabs.bcdh.uni-bonn.de/hector_epochs/` definiert und nutzt rein **abstrakte, opake URIs** (`c_<stable_hash>`) zur Gewährleistung der Stabilität.

Es besteht aus folgenden Teil-Facetten:
1. **Core-Epochen:** Die grundlegenden archäologischen Epochen (Steinzeit, Kupferzeit, Bronzezeit, Eisenzeit, Altertum, Mittelalter, Neuzeit) basierend auf der ursprünglichen Ontologiestruktur.
2. **Chronologisches Raster:** Ein feingliedriges, zeitliches Raster aus Jahrtausenden, Jahrhunderten sowie deren Hälften und Vierteln (von 3000 v. Chr. bis heute).
3. **Römische Kaiserzeit:** 106 römische Kaiser, chronologisch sortiert in die *Frühe*, *Mittlere* und *Späte Kaiserzeit*.
4. **Mittelalterliche Dynastien:** Gliederung der Herrscher nach Ländern (Heiliges Römisches Reich, England, Frankreich, Spanien, Italien) und deren Dynastien (Ottonen, Salier, Staufer, Normannen, Kapetinger, etc.) mit 86 detaillierten Herrscherprofilen.
5. **Altes Ägypten:** Eine hierarchische Gliederung des Alten Ägyptens in Epochen (Altes Reich, Neues Reich, etc.), Dynastien (1. bis 31. Dynastie, Ptolemäer) und 524 Pharaonen.

---

## ✨ Key Features (Editor)
* **SKOS Hierarchy Management:** Visually construct and manage `skos:Concept` hierarchies, broader/narrower relationships, and top concepts.
* **Multilingual Support:** Dynamic UI for managing `skos:prefLabel` and `skos:altLabel` across multiple language codes (DE/EN).
* **Polyhierarchical Support:** Concepts can be linked to multiple broader terms, allowing for an accurate representation of complex knowledge domains (e.g., Neuzeit centuries linked to both Neuzeit and the Chronological Grid).
* **Chronological Sorting:** The Treeview sorts all periods, millennia, centuries, halves, and quarters chronologically based on their German labels.
* **Authority File Integration:** Built-in asynchronous querying and exact matching (`skos:exactMatch`) for:
    * Wikidata API
    * Getty Art & Architecture Thesaurus (AAT)
    * Gemeinsame Normdaten (GND)
* **Turtle Serialization:** Native import and export of robust `.ttl` (Turtle) graphs using RDFLib.

---

## 🚀 Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/bcdhbonn/hector-editor.git
   cd hector-editor
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the editor:
   ```bash
   python hector_editor.py
   ```
