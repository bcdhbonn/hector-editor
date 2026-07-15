# HECTOR 3D Documentation SKOS Vocabulary

This directory contains the compiled and integrated SKOS vocabulary: **`HECTOR_3D_Documentation.ttl`**.

---

## 🌐 Namespace & URI Scheme

* **Base Namespace:** `http://vocabs.bcdh.uni-bonn.de/hector_3d_documentation/`
* **Namespace Prefix:** `hector_3d_documentation` (default empty prefix `:` in the serialization)
* **URIs:** To ensure URI stability, all concepts use identifiers of the format:
  `http://vocabs.bcdh.uni-bonn.de/hector_3d_documentation/concept_<id>`
  * The `<id>` represents a unique, stable, 8-character hexadecimal identifier.

---

## 📂 Vocabulary Facets

The vocabulary contains a hierarchical classification of technical documentation and processing metadata for 3D modeling, photogrammetry, and scanning:

1. **3D Model Preparation:** Operations for editing geometry (geometry operations like Meshmixer, MeshLab) and processing textures (PBR textures, normal maps, ambient occlusion).
2. **Dateiformat (File Formats):** Categorization of 3D data formats (e.g., PLY, OBJ) and image file formats (e.g., JPEG, PNG).
3. **Georeferenzierung (Georeferencing):** Methods for relative and absolute spatial referencing, measurement methods (GPS, Tachymeter, scale bars), and registration (target-based registration).
4. **Recording Devices:** Physical capture hardware, including laserscanners (e.g., Faro Focus series), structured light scanners (e.g., Artec Eva/Leo/Spider), and camera models (e.g., Nikon DSLR and mirrorless series).
5. **Software Systems:** Software tools used for digital content creation (DCC), photogrammetry processing (e.g., 3DF Zephyr, RealityScan, Meshroom), laserscanning (e.g., FARO SCENE, Z+F LaserControl), and structured light scanning (Artec Studio).

---

## 🔗 Authority File Alignments

Core concepts are enriched with definitions and mappings (`skos:exactMatch`) to global authority files:
* **Wikidata URIs** (e.g., `http://www.wikidata.org/entity/Q...`)
* **Gemeinsame Normdaten (GND) URIs** (e.g., `https://d-nb.info/gnd/...`)
* **Getty Art & Architecture Thesaurus (AAT) URIs** (e.g., `http://vocab.getty.edu/aat/...`)
