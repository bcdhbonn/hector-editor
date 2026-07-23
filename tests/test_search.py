import unittest
import os
import shutil
import tkinter as tk
from rdflib import Graph, URIRef, RDF, SKOS, Literal
from hector_core import VocabularyManager
from hector_editor import HECTOREditor

class TestEditorSearch(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_search_temp"
        os.makedirs(self.test_dir, exist_ok=True)
        self.vocab_path = os.path.join(self.test_dir, "search_vocab.ttl")
        
        self.mgr = VocabularyManager()
        self.mgr.create_new_vocabulary(self.vocab_path, "http://example.org/test/", "Search Vocab")
        
        # Build hierarchy:
        # Root: Archäologische Objekte (c_root)
        #   └─ Keramik (c_parent)
        #        └─ Amphore (c_child)
        self.c_root = URIRef("http://example.org/test/root")
        self.c_parent = URIRef("http://example.org/test/parent")
        self.c_child = URIRef("http://example.org/test/child")
        
        self.mgr.g.add((self.c_root, RDF.type, SKOS.Concept))
        self.mgr.g.add((self.c_root, SKOS.prefLabel, Literal("Archäologische Objekte", lang="de")))
        
        self.mgr.g.add((self.c_parent, RDF.type, SKOS.Concept))
        self.mgr.g.add((self.c_parent, SKOS.prefLabel, Literal("Keramik", lang="de")))
        self.mgr.g.add((self.c_parent, SKOS.broader, self.c_root))
        
        self.mgr.g.add((self.c_child, RDF.type, SKOS.Concept))
        self.mgr.g.add((self.c_child, SKOS.prefLabel, Literal("Amphore", lang="de")))
        self.mgr.g.add((self.c_child, SKOS.altLabel, Literal("Speichergefäß", lang="de")))
        self.mgr.g.add((self.c_child, SKOS.broader, self.c_parent))
        
        self.mgr.serialize()
        
        # Create headless Tk app for testing HECTOREditor
        self.root = tk.Tk()
        self.root.withdraw()
        self.editor = HECTOREditor(self.root)
        self.editor.load_data(self.vocab_path)

    def tearDown(self):
        self.root.destroy()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_search_leaf_node_shows_full_path(self):
        # Type "amphore" into search field
        self.editor.txt_search.delete(0, "end")
        self.editor.txt_search.insert(0, "amphore")
        self.editor.update_tree_ui()
        
        # Verify tree contains root, parent, and child
        tree_items = self.editor.tree.get_children("")
        self.assertEqual(len(tree_items), 1)
        root_vals = self.editor.tree.item(tree_items[0])["values"]
        self.assertEqual(root_vals[0], str(self.c_root))
        
        # Check that root node is open (expanded)
        self.assertTrue(self.editor.tree.item(tree_items[0], "open"))
        
        # Check children of root node (Keramik)
        parent_items = self.editor.tree.get_children(tree_items[0])
        self.assertEqual(len(parent_items), 1)
        parent_vals = self.editor.tree.item(parent_items[0])["values"]
        self.assertEqual(parent_vals[0], str(self.c_parent))
        
        # Check children of parent node (Amphore)
        child_items = self.editor.tree.get_children(parent_items[0])
        self.assertEqual(len(child_items), 1)
        child_vals = self.editor.tree.item(child_items[0])["values"]
        self.assertEqual(child_vals[0], str(self.c_child))

    def test_search_alt_label(self):
        # Search by altLabel "Speichergefäß"
        self.editor.txt_search.delete(0, "end")
        self.editor.txt_search.insert(0, "speichergefäß")
        self.editor.update_tree_ui()
        
        tree_items = self.editor.tree.get_children("")
        self.assertEqual(len(tree_items), 1)

    def test_search_no_match(self):
        # Search for non-existent concept
        self.editor.txt_search.delete(0, "end")
        self.editor.txt_search.insert(0, "xyz_non_existent")
        self.editor.update_tree_ui()
        
        tree_items = self.editor.tree.get_children("")
        self.assertEqual(len(tree_items), 0)
