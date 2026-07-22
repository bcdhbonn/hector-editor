# Rhineland Archaeological Vocabulary (SKOS)

This directory contains the SKOS vocabulary for describing archaeological finds, features (contexts), and chronological dating in the German-Dutch border region (Rhineland).

## 📄 Overview

* **File:** `arch_vocab_rhineland.ttl`
* **Format:** Turtle (RDF/SKOS)
* **Namespace:** `http://vocabs.bcdh.uni-bonn.de/LVR_Fundansprachen/`
* **Languages:** German (`de`), English (`en`), Dutch (`nl`)

## 💡 Description

The **Rhineland Archaeological Vocabulary** (`arch_vocab_rhineland.ttl`) provides a standardized, multilingual semantic hierarchy for categorizing and describing:
* **Archaeological Finds & Artifacts (Fundansprachen):** Tools, ceramics, coins, ornaments, sacral objects, organic remains, metalwork, and functional object types.
* **Archaeological Features & Contexts (Befundansprachen):** Structural remains, pits, postholes, graves, walls, ditches, hearths, and settlement structures.
* **Chronological Dating (Datierungen):** Archaeological epochs, millennia, centuries, and regional cultural periods.

It is specifically tailored for cross-border research and data integration in the German-Dutch border region, featuring trilingual labeling (`de`, `en`, `nl`) as well as explicit exact matches (`skos:exactMatch`) to global authority standards including **Wikidata**, **Getty Art & Architecture Thesaurus (AAT)**, and **Gemeinsame Normdaten (GND)**.

## 🔗 Linked Data & Authorities

Concepts in this vocabulary are mapped to external authority systems:
* **Wikidata Entities** (`http://www.wikidata.org/entity/Q...`)
* **Getty AAT Concepts** (`http://vocab.getty.edu/aat/...`)
* **GND Authority Records** (`https://d-nb.info/gnd/...`)

## 🛠 Usage & Editing

This vocabulary is saved in standard Turtle (`.ttl`) format and can be loaded into any RDF triple store, web browser for SKOS vocabularies, or managed using the [HECTOR-Editor](../../README.md).
