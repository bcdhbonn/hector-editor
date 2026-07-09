# 🏛️ HECTOR-Editor – Wiki & Benutzerhandbuch

Willkommen im Wiki des **HECTOR-Editors**. Dieses Handbuch bietet eine detaillierte und umfassende Anleitung zur Installation, Bedienung und den erweiterten Funktionen des HECTOR-Editors für die Verwaltung von semantischen SKOS-Vokabularen in den Digital Humanities und der Archäologie.

---

## Inhaltsverzeichnis
1. [Einführung](#1-einführung)
2. [Installation & Start](#2-installation--start)
3. [Die Benutzeroberfläche](#3-die-benutzeroberfläche)
4. [Grundlegende Workflows (Konzepte verwalten)](#4-grundlegende-workflows-konzepte-verwalten)
5. [Hierarchie & Polyhierarchie](#5-hierarchie--polyhierarchie)
6. [Schnittstellen & Autoritätsdaten (Wikidata, AAT, GND)](#6-schnittstellen--autoritätsdaten-wikidata-aat-gnd)
7. [Datenqualität & Integritätswerkzeuge](#7-datenqualität--integritätswerkzeuge)
8. [Datenhaltung & Export](#8-datenhaltung--export)

---

## 1. Einführung

Der **HECTOR-Editor** ist eine leichtgewichtige, responsive Desktop-Anwendung, die in Python mit der GUI-Bibliothek **CustomTkinter** entwickelt wurde. Das Tool wurde speziell für die Verwaltung, Strukturierung und Qualitätsprüfung von kontrollierten Vokabularen nach dem **SKOS-Standard (Simple Knowledge Organization System)** konzipiert.

### Hauptmerkmale:
* **Hierarchische Modellierung:** Einfache Zuordnung von Oberbegriffen (`skos:broader`) und Unterbegriffen (`skos:narrower`).
* **Mehrsprachigkeit:** Unterstützung von Bezeichnungen (`skos:prefLabel` und `skos:altLabel`) in mehreren Sprachen (z. B. Deutsch und Englisch).
* **Polyhierarchie:** Ein Konzept kann mehreren Oberbegriffen gleichzeitig zugeordnet sein.
* **Normdaten-Anbindung:** Integrierte Abfrage-Schnittstellen für Wikidata, Getty AAT und die Gemeinsame Normdatei (GND) zur Verknüpfung von Konzepten mit externen URIs (`skos:exactMatch`).
* **Qualitätssicherung:** Automatische Konsistenzprüfungen und reziproke Verknüpfungen.

---

## 2. Installation & Start

### Systemvoraussetzungen
* **Python 3.8 oder neuer**
* Pip (Python Package Installer)

### Installation
1. Klonen Sie das Repository oder laden Sie die Projektdateien herunter:
   ```bash
   git clone https://github.com/bcdhbonn/hector-editor-skos.git
   cd hector-editor-skos
   ```
2. Installieren Sie die erforderlichen Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

### Anwendung starten
Starten Sie den Editor über die Befehlszeile:
```bash
python hector_editor.py
```

---

## 3. Die Benutzeroberfläche

Die Oberfläche des HECTOR-Editors ist in zwei Hauptbereiche unterteilt:

```
+------------------------------------------+------------------------------------------+
|  LINKS: NAVIGATION & WERKZEUGE           |  RECHTS: EDITIERBEREICH (FORMULAR)       |
|  - Anwendungs-Header & Theme-Umschalter  |  - Konzept-URI (ID-Generierung)          |
|  - Datei-Aktionen (Laden, Erstellen)     |  - Bezeichnungen (prefLabel / altLabel)  |
|  - Hierarchie-Baum (Treeview)            |  - Definitionen (mehrsprachig)           |
|  - Datenqualitäts-Panel (Integrität)     |  - Externe Mappings (Wikidata, AAT, GND) |
|  - Log-Konsole (Betriebs-Logs)           |  - Elternbeziehungen (Polyhierarchie)   |
|                                          |  - Speichern & Löschen Aktionen          |
+------------------------------------------+------------------------------------------+
```

### Linker Bereich (Workspace Panel)
* **Dateiverwaltung:** Laden und Erstellen von `.ttl`-Vokabularen, sowie das Importieren von Unter-Vokabularen/Facetten.
* **Hierarchie-Baum (Treeview):** Zeigt die hierarchische Struktur des geladenen Vokabulars. Unterstützt die chronologische Sortierung (z. B. nach Epochen, Jahrhunderten, Quartalen).
* **Datenqualität:** Werkzeuge zur Integritätsprüfung und automatischen Korrektur von Fehlern im Vokabular.
* **Log-Konsole:** Echtzeit-Ausgabe aller ausgeführten Prozesse (z. B. API-Anfragen, Lade- und Speichervorgänge).

### Rechter Bereich (Concept Editor)
* **Metadaten-Formular:** Editieren aller SKOS-Felder für das aktuell im Baum ausgewählte Konzept.
* **Schaltflächen:** Speichern der Änderungen ins geladene Vokabular sowie das Löschen von Konzepten.

---

## 4. Grundlegende Workflows (Konzepte verwalten)

### Vokabular laden oder erstellen
* **Laden:** Klicken Sie auf **Open Main Vocabulary (.ttl)** und wählen Sie eine SKOS-Turtle-Datei (z. B. [vocabularies/hector_epochs/HECTOR_Epoch.ttl](file:///e:/Vocab/hector-editor-skos/vocabularies/hector_epochs/HECTOR_Epoch.ttl)).
* **Erstellen:** Nutzen Sie **Create New Vocabulary**, um ein neues leeres Konzeptschema mit einer eigenen Basis-URI zu initialisieren.

### Neues Konzept erstellen
1. Klicken Sie im rechten Editorbereich auf **Clear / New Concept**. Dadurch werden alle Formularfelder geleert und eine eindeutige UUID für die neue Konzept-URI generiert.
2. Tragen Sie die Bezeichnungen (`prefLabel` und optional `altLabel`) für die gewünschten Sprachen ein.
3. Wählen Sie im Feld **Broader Parents** (rechte Spalte) einen oder mehrere Oberbegriffe aus. Wenn das Konzept ein Haupteinstiegspunkt sein soll, aktivieren Sie die Option **Is Top Concept of Scheme**.
4. Klicken Sie auf **💾 Save Concept**, um das Konzept im Vokabular zu speichern und in die Baumstruktur einzutragen.

### Konzept bearbeiten
1. Wählen Sie das Konzept im linken Hierarchie-Baum aus. Die Daten werden automatisch in das rechte Formular geladen.
2. Nehmen Sie die Änderungen vor (z. B. Text anpassen, alternative Labels hinzufügen oder Mappings ändern).
3. Klicken Sie auf **💾 Save Concept**, um die Änderungen zu sichern.

### Konzept löschen
1. Wählen Sie das gewünschte Konzept im Hierarchie-Baum aus.
2. Klicken Sie unten rechts auf **❌ Delete Concept**.
3. Bestätigen Sie die Sicherheitsabfrage. Das Konzept sowie alle seine Verknüpfungen werden aus dem Vokabular entfernt.

---

## 5. Hierarchie & Polyhierarchie

### Hierarchische Beziehungen (`skos:broader` & `skos:narrower`)
* Wenn Sie ein Konzept als Unterbegriff deklarieren, fügt der Editor eine `skos:broader`-Beziehung zum Elternkonzept hinzu.
* Gleichzeitig generiert die Anwendung die reziproke `skos:narrower`-Beziehung am Elternkonzept. Beim Speichern oder Ändern von Elternbeziehungen bereinigt der Editor veraltete Gegenbeziehungen automatisch, um die Konsistenz des Graphen zu wahren.

### Polyhierarchische Zuordnung
* Der Editor unterstützt vollumfänglich Polyhierarchien. Ein Konzept kann mehreren Oberbegriffen gleichzeitig zugeordnet werden.
* Halten Sie im Bereich **Broader Parents** die `Strg`-Taste (bzw. `Ctrl`) gedrückt, um mehrere Oberbegriffe in der Liste zu markieren.
* Beim Speichern wird das Konzept im Hierarchie-Baum unter allen ausgewählten Elternknoten gleichzeitig angezeigt.

### Chronologische Sortierung
* Die Sortierung der Baumstruktur erfolgt nach einem intelligenten chronologischen Schlüssel auf Basis der deutschen Bezeichnungen (`prefLabel`).
* Zeitangaben (z. B. „3. Jahrtausend v. Chr.“, „1. Hälfte 19. Jh. v. Chr.“, „2. Viertel 8. Jh. n. Chr.“) werden automatisch erkannt und chronologisch sortiert, statt rein alphabetisch geordnet zu werden.

---

## 6. Externe Autoritätsdaten & Mappings

Zur Vernetzung Ihrer Vokabulare mit dem Semantic Web (Linked Open Data) können Konzepte mit normierten IDs verknüpft werden. Der HECTOR-Editor bietet dafür eine asynchrone API-Integration.

### Wikidata-Verknüpfung
1. Geben Sie die Labels des Konzepts ein.
2. Klicken Sie auf **🔍 Query Wikidata API**.
3. Ein Auswahlfenster öffnet sich und listet die 15 besten Treffer auf Wikidata (inkl. ID, Label und Beschreibung).
4. Wählen Sie den passenden Eintrag aus. Die Wikidata-URI wird automatisch in das Feld **Wikidata Match** eingetragen und beim Speichern als `skos:exactMatch` serialisiert.

### Getty AAT & GND Integration
* Über die Schaltflächen **🔍 Query Getty AAT** und **🔍 Query GND API** können die jeweiligen Repositorien nach passenden Datensätzen durchsucht und die Mappings direkt übernommen werden.

---

## 7. Datenqualität & Integritätswerkzeuge

Im linken Bereich unter **Data Quality / Integrity Checks** stehen drei mächtige Reparaturwerkzeuge bereit:

### 1. 🔄 Sync Broader/Narrower
* **Problem:** Manchmal fehlen in importierten RDF-Daten die reziproken Gegenbeziehungen (z. B. es gibt `skos:broader`, aber kein Gegenstück `skos:narrower`).
* **Lösung:** Dieses Tool scannt das gesamte Vokabular, findet alle einseitigen Beziehungen, ergänzt die fehlenden Gegenstücke und speichert die Datei neu ab.

### 2. 🔧 Repair Missing URI Labels
* **Problem:** Konzepte besitzen zwar eine URI, haben jedoch kein lesbares `skos:prefLabel` zugewiesen bekommen.
* **Lösung:** Generiert automatisch ein englisches Standardlabel, das auf dem lokalen Teil (Local Name) der Konzept-URI basiert (z. B. aus `c_12345` wird `c_12345`).

### 3. 🔍 Run Health Check
* **Problem:** Verwaiste Konzepte (Orphans), die weder einen Oberbegriff (`skos:broader`) besitzen, noch als Einstiegspunkt (`skos:hasTopConcept` / `skos:topConceptOf`) deklariert sind.
* **Lösung:** Listet alle verwaisten URIs in der Log-Konsole auf, damit diese im Editor gesucht und korrekt verknüpft werden können.

---

## 8. Datenhaltung & Export

### Turtle-Dateiformat (.ttl)
* Alle Vokabulare werden im bewährten W3C-Standard-Format **Turtle** gespeichert.
* Dies ermöglicht eine einfache Versionsverwaltung mit Git, da Änderungen zeilenbasiert und lesbar in Diff-Views nachvollzogen werden können.

### Facetten- und Teilexport
* Wenn Sie nur einen bestimmten Ast eines Vokabulars exportieren möchten, wählen Sie das gewünschte Konzept im Baum aus und klicken Sie auf **📥 Export Sub-Tree (Facet)**.
* Der Editor extrahiert dieses Konzept und alle darunterliegenden Unterkonzepte rekursiv in eine neue eigenständige Turtle-Datei.
