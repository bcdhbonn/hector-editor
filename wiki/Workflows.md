# 📖 Core Workflows

This page details standard workflows for managing concepts and schemas using HECTOR-Editor.

---

## 📂 File Management

### Loading an Existing Vocabulary
1. Click **Open Main Vocabulary (.ttl)**.
2. Select your SKOS Turtle file (e.g., `HECTOR_Epoch.ttl`).
3. The hierarchy tree will render on the left, and the root concept scheme URI will be detected.

### Creating a New Vocabulary
1. Click **Create New Vocabulary**.
2. Enter the base URI namespace in the popup dialog (e.g., `https://example.org/vocab/`).
3. The editor initializes a fresh graph containing a `skos:ConceptScheme`.

---

## 🏛️ Managing Concepts

### Adding a New Concept
1. Click **Clear / New Concept** in the lower right of the Editor panel.
2. The form clears, and a new unique concept URI (UUID-based) is generated.
3. Fill in the **Preferred Label (`prefLabel`)** under the corresponding language tabs (e.g. `de` and `en`).
4. (Optional) Provide **Alternative Labels (`altLabel`)** or a **Definition**.
5. Select the concept's position in the hierarchy:
   * **Root level:** Check **Is Top Concept of Scheme**.
   * **Sub-concept:** Select one or more parents in the **Broader Parents** listbox.
6. Click **💾 Save Concept**. The concept is added to the graph and tree.

### Editing a Concept
1. Search or navigate to the concept in the hierarchy tree on the left.
2. Click the concept. Its metadata will load into the form on the right.
3. Modify the labels, definitions, mappings, or parent associations.
4. Click **💾 Save Concept**.

### Deleting a Concept
1. Select the concept in the tree.
2. Click **❌ Delete Concept** in the bottom right.
3. Confirm the deletion. The editor will remove the concept, clean up any incoming/outgoing hierarchical links, and update the graph.

---

## 🌳 Hierarchies & Polyhierarchies

### Establishing Parents
* Select a concept in the **Broader Parents** list on the right. The editor automatically translates this selection into a `skos:broader` statement.
* Simultaneously, the editor handles the inverse `skos:narrower` connection on the parent concept, keeping the graph synchronized.

### Working with Polyhierarchies
* SKOS allows concepts to have multiple parents.
* To select multiple parents in the list box, hold down `Ctrl` (Windows/Linux) or `Command` (macOS) and click the desired parents.
* Click **💾 Save Concept**. The concept will appear under all parent branches in the tree.
