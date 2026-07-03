import os
import re
import time
import json
import urllib.request
import urllib.parse
import hashlib
from rdflib import Graph, Literal, RDF, SKOS, URIRef

# Base namespace definition
NAMESPACE_BASE = "http://vocabs.bcdh.uni-bonn.de/hector_epochs/"

def c_uri(semantic_id):
    """Generates a stable, opaque abstract concept URI from a semantic ID/URI."""
    name = str(semantic_id).split('/')[-1]
    h = hashlib.sha256(name.encode('utf-8')).hexdigest()[:8]
    return URIRef(f"{NAMESPACE_BASE}c_{h}")

# Complete mapping of epochen.owl concepts to Wikidata QIDs
WIKIDATA_MAPPING = {
    "Bronzeit_Kreta": "Q134178",           # Minoan civilization
    "Bronzeit_Kykladen": "Q318144",         # Cycladic civilization
    "Helladisch": "Q937774",               # Helladic period
    "Kykladisch": "Q318144",               # Cycladic civilization
    "Minoisch": "Q134178",                 # Minoan civilization
    "akkadisch": "Q4461035",               # Akkadian Empire
    "alter_orient": "Q269678",             # ancient Near East
    "altertum": "Q41493",                  # ancient history
    "altesaegypten": "Q11768",             # Ancient Egypt
    "altlpaläolithikum": "Q7463501",       # Lower Paleolithic
    "altsteinzeit": "Q40203",              # Paleolithic
    "antike": "Q486761",                   # classical antiquity
    "archaisch": "Q271834",                # Archaic Greece
    "assyrien": "Q41137",                  # Assyrian Empire
    "babylonisch": "Q47690",               # Babylonia
    "bronzeit_griechisches_festland": "Q937774", # Helladic period
    "bronzezeit": "Q11761",                # Bronze Age
    "bronzezeit_mittelmeer": "Q11761",     # Map to general Bronze Age
    "byzantinisch": "Q12544",              # Byzantine Empire
    "dunkle_jahrhunderte": "Q210443",       # Greek Dark Ages
    "eisenzeit": "Q11764",                 # Iron Age
    "eisenzeit_griechenland": "Q210443",    # Greek Dark Ages / Iron Age Greece
    "eisenzeit_mittelmeer": "Q11764",      # Map to general Iron Age
    "epoche": "Q132712",                   # epoch / historical epoch
    "frueharchaisch": "Q271834",            # Archaic Greece
    "fruehgeometrisch": "Q852337",          # geometric art / period
    "fruehhelladisch": "Q22949209",         # Early Helladic
    "fruehklassisch": "Q11772",            # Ancient Greece / Classical Greece
    "fruehkykladisch": "Q57475796",        # Early Cycladic
    "fruehminoisch": "Q137262624",         # Early Minoan
    "geometrisch": "Q852337",              # geometric art / period
    "hellenismus": "Q428995",              # Hellenistic period
    "hellenismus_frueh": "Q428995",        # Hellenistic period
    "hellenismus_hoch": "Q428995",         # Hellenistic period
    "hellenismus_spaet": "Q428995",        # Hellenistic period
    "hochklassisch": "Q11772",             # Classical Greece
    "jungpaläolithikum": "Q479505",        # Upper Paleolithic
    "jungsteinzeit": "Q36422",             # Neolithic
    "karthagisch": "Q2429397",             # Ancient Carthage
    "klassisch": "Q11772",                 # Classical Greece
    "kupferzeit": "Q130253",               # Chalcolithic
    "mittelalter": "Q12554",               # Middle Ages
    "mittelarchaisch": "Q271834",          # Archaic Greece
    "mittelgeometrisch": "Q852337",        # geometric art / period
    "mittelhelladisch": "Q1940165",        # Middle Helladic
    "mittelkykladisch": None,              # None
    "mittelminoisch": "Q12056948",         # Middle Minoan
    "mittelpaläolithikum": "Q626270",      # Middle Paleolithic
    "mittelsteinzeit": "Q44155",           # Mesolithic
    "mykenisch": "Q181264",                # Mycenaean Greece
    "neuzeit": "Q3281534",                 # modern period
    "protogeometrisch": "Q138000931",      # Protogeometric period
    "punisch": "Q2429397",                 # Punic / Ancient Carthage
    "roemische_eisenzeit": "Q2566630",     # Roman Iron Age
    "roemische_kaiserzeit": "Q2277",       # Roman Empire
    "roemische_kaiserzeit_frueh": "Q787204",  # Early Roman Empire
    "roemische_kaiserzeit_mittel": "Q787204", # High Roman Empire
    "roemische_kaiserzeit_spaet": "Q120754706", # Late Roman Empire
    "spaetantike": "Q217050",              # Late antiquity
    "spaetarchaisch": "Q271834",            # Archaic Greece
    "spaetgeometrisch": "Q852337",          # geometric art / period
    "spaetklassisch": "Q11772",            # Classical Greece
    "spaetkykladisch": None,               # None
    "spaetlhelladisch": "Q2314802",        # Late Helladic
    "spaetminoisch": "Q137262642",         # Late Minoan
    "steinzeit": "Q11759",                 # Stone Age
    "subminoisch": None,                   # None
    "submykenisch": "Q1515819",            # Sub-Mycenaean pottery
    "sumerisch": "Q35355"                  # Sumerian
}

# English translations for category labels that don't match directly
ENGLISH_LABEL_OVERRIDES = {
    "Bronzeit_Kreta": "Bronze Age Crete",
    "Bronzeit_Kykladen": "Bronze Age Cyclades",
    "Helladisch": "Helladic Period",
    "Kykladisch": "Cycladic Period",
    "Minoisch": "Minoan Period",
    "akkadisch": "Akkadian Period",
    "alter_orient": "Ancient Near East",
    "altertum": "Antiquity",
    "altesaegypten": "Ancient Egypt",
    "altlpaläolithikum": "Lower Paleolithic",
    "altsteinzeit": "Paleolithic",
    "antike": "Classical Antiquity",
    "archaisch": "Archaic Period",
    "assyrien": "Assyrian Period",
    "babylonisch": "Babylonian Period",
    "bronzeit_griechisches_festland": "Bronze Age Greece (Mainland)",
    "bronzezeit": "Bronze Age",
    "bronzezeit_mittelmeer": "Mediterranean Bronze Age",
    "byzantinisch": "Byzantine Period",
    "dunkle_jahrhunderte": "Dark Ages (Greece)",
    "eisenzeit": "Iron Age",
    "eisenzeit_griechenland": "Greek Iron Age",
    "eisenzeit_mittelmeer": "Mediterranean Iron Age",
    "epoche": "Epoch",
    "frueharchaisch": "Early Archaic Period",
    "fruehgeometrisch": "Early Geometric Period",
    "fruehhelladisch": "Early Helladic Period",
    "fruehklassisch": "Early Classical Period",
    "fruehkykladisch": "Early Cycladic Period",
    "fruehminoisch": "Early Minoan Period",
    "geometrisch": "Geometric Period",
    "hellenismus": "Hellenistic Period",
    "hellenismus_frueh": "Early Hellenistic Period",
    "hellenismus_hoch": "High Hellenistic Period",
    "hellenismus_spaet": "Late Hellenistic Period",
    "hochklassisch": "High Classical Period",
    "jungpaläolithikum": "Upper Paleolithic",
    "jungsteinzeit": "Neolithic",
    "karthagisch": "Carthaginian Period",
    "klassisch": "Classical Period",
    "kupferzeit": "Copper Age",
    "mittelalter": "Middle Ages",
    "mittelarchaisch": "Middle Archaic Period",
    "mittelgeometrisch": "Middle Geometric Period",
    "mittelhelladisch": "Middle Helladic Period",
    "mittelkykladisch": "Middle Cycladic Period",
    "mittelminoisch": "Middle Minoan Period",
    "mittelpaläolithikum": "Middle Paleolithic",
    "mittelsteinzeit": "Mesolithic",
    "mykenisch": "Mycenaean Period",
    "neuzeit": "Modern Period",
    "protogeometrisch": "Protogeometric Period",
    "punisch": "Punic Period",
    "roemische_eisenzeit": "Roman Iron Age",
    "roemische_kaiserzeit": "Roman Imperial Period",
    "roemische_kaiserzeit_frueh": "Early Roman Imperial Period",
    "roemische_kaiserzeit_mittel": "Middle Roman Imperial Period",
    "roemische_kaiserzeit_spaet": "Late Roman Imperial Period",
    "spaetantike": "Late Antiquity",
    "spaetarchaisch": "Late Archaic Period",
    "spaetgeometrisch": "Late Geometric Period",
    "spaetklassisch": "Late Classical Period",
    "spaetkykladisch": "Late Cycladic Period",
    "spaetlhelladisch": "Late Helladic Period",
    "spaetminoisch": "Late Minoan Period",
    "steinzeit": "Stone Age",
    "subminoisch": "Sub-Minoan Period",
    "submykenisch": "Sub-Mycenaean Period",
    "sumerisch": "Sumerian Period"
}

# Ancient Egypt Dynasties to Kingdoms mappings
DYNASTY_TO_KINGDOM = {
    "Q1484140": "praedynastik",          # 0. Dynastie
    "Q203859": "fruehdynastisch",        # 1. Dynastie
    "Q207778": "fruehdynastisch",        # 2. Dynastie
    "Q220299": "altes_reich",            # 3. Dynastie
    "Q220272": "altes_reich",            # 4. Dynastie
    "Q269225": "altes_reich",            # 5. Dynastie
    "Q244805": "altes_reich",            # 6. Dynastie
    "Q269255": "erste_zwischenzeit",      # 7. & 8. Dynastie
    "Q269269": "erste_zwischenzeit",      # 9. & 10. Dynastie
    "Q719634": "mittleres_reich",        # 11. Dynastie
    "Q719639": "mittleres_reich",        # 12. Dynastie
    "Q721807": "zweite_zwischenzeit",     # 13. Dynastie
    "Q650945": "zweite_zwischenzeit",     # 14. Dynastie
    "Q728479": "zweite_zwischenzeit",     # 15. Dynastie
    "Q737695": "zweite_zwischenzeit",     # 16. Dynastie
    "Q642301": "zweite_zwischenzeit",     # 17. Dynastie
    "Q146055": "neues_reich",            # 18. Dynastie
    "Q157956": "neues_reich",            # 19. Dynastie
    "Q583501": "neues_reich",            # 20. Dynastie
    "Q748151": "dritte_zwischenzeit",     # 21. Dynastie
    "Q752834": "dritte_zwischenzeit",     # 22. Dynastie
    "Q748133": "dritte_zwischenzeit",     # 23. Dynastie
    "Q748135": "dritte_zwischenzeit",     # 24. Dynastie
    "Q244325": "dritte_zwischenzeit",     # 25. Dynastie
    "Q262071": "spaetzeit",              # 26. Dynastie
    "Q271813": "spaetzeit",              # 27. Dynastie
    "Q903029": "spaetzeit",              # 27. Dynastie
    "Q748140": "spaetzeit",              # 28. Dynastie
    "Q748143": "spaetzeit",              # 29. Dynastie
    "Q748148": "spaetzeit",              # 30. Dynastie
    "Q1278385": "spaetzeit",             # 31. Dynastie
    "Q903031": "spaetzeit",              # 31. Dynastie
    "Q207115": "ptolemaeisch",           # Ptolemaic Dynasty
    "Q131976": "ptolemaeisch"            # Ptolemaic Period
}

EGYPT_KINGDOMS = {
    "praedynastik": {"de": "Prä- und Protodynastische Periode", "en": "Predynastic Period"},
    "fruehdynastisch": {"de": "Frühdynastische Periode", "en": "Early Dynastic Period"},
    "altes_reich": {"de": "Altes Reich", "en": "Old Kingdom"},
    "erste_zwischenzeit": {"de": "Erste Zwischenzeit", "en": "First Intermediate Period"},
    "mittleres_reich": {"de": "Mittleres Reich", "en": "Middle Kingdom"},
    "zweite_zwischenzeit": {"de": "Zweite Zwischenzeit", "en": "Second Intermediate Period"},
    "neues_reich": {"de": "Neues Reich", "en": "New Kingdom"},
    "dritte_zwischenzeit": {"de": "Dritte Zwischenzeit", "en": "Third Intermediate Period"},
    "spaetzeit": {"de": "Spätzeit des Alten Ägyptens", "en": "Late Period"},
    "ptolemaeisch": {"de": "Ptolemäische Zeit", "en": "Ptolemaic Period"},
    "no_dynasty_fallback": {"de": "Pharaonen ohne bekannte Dynastie", "en": "Pharaohs without known Dynasty"}
}

# Medieval Countries/Regions and Dynasties for the Middle Ages
MEDIEVAL_REGIONS = {
    "deutschland_hrr": {"de": "Heiliges Römisches Reich (Dynastien)", "en": "Holy Roman Empire (Dynasties)"},
    "england": {"de": "England (Dynastien)", "en": "England (Dynasties)"},
    "frankreich": {"de": "Frankreich (Dynastien)", "en": "France (Dynasties)"},
    "spanien": {"de": "Spanien (Dynastien)", "en": "Spain (Dynasties)"},
    "italien": {"de": "Italien (Dynastien)", "en": "Italy (Dynasties)"}
}

MEDIEVAL_DYNASTIES = {
    # Germany / HRR
    "ottonen": {"de": "Ottonen", "en": "Ottonian Dynasty", "region": "deutschland_hrr", "wikidata": "Q161047", "rulers": ["Q43915", "Q150512", "Q151090", "Q103556"]},
    "salier": {"de": "Salier", "en": "Salian Dynasty", "region": "deutschland_hrr", "wikidata": "Q160161", "rulers": ["Q152256", "Q153023", "Q60094", "Q57321"]},
    "staufer": {"de": "Staufer", "en": "Hohenstaufen Dynasty", "region": "deutschland_hrr", "wikidata": "Q131413", "rulers": ["Q57181", "Q79789", "Q151415", "Q76435"]},
    "luxemburger": {"de": "Luxemburger", "en": "House of Luxembourg", "region": "deutschland_hrr", "wikidata": "Q152431", "rulers": ["Q57100", "Q155622", "Q57161", "Q57155"]},
    "habsburger": {"de": "Habsburger", "en": "House of Habsburg", "region": "deutschland_hrr", "wikidata": "Q65963", "rulers": ["Q154944", "Q57454", "Q57434", "Q150537"]},
    
    # England
    "england_normannen": {"de": "Normannen", "en": "House of Normandy", "region": "england", "wikidata": "Q106861", "rulers": ["Q37594", "Q71257", "Q101384", "Q82654"]},
    "plantagenet": {"de": "Plantagenet", "en": "House of Plantagenet", "region": "england", "wikidata": "Q104925", "rulers": ["Q39600", "Q42305", "Q83220", "Q41131", "Q78855", "Q57285", "Q129006", "Q81256"]},
    "lancaster": {"de": "Lancaster", "en": "House of Lancaster", "region": "england", "wikidata": "Q104278", "rulers": ["Q79888", "Q845155", "Q131427"]},
    "york": {"de": "York", "en": "House of York", "region": "england", "wikidata": "Q104443", "rulers": ["Q160341", "Q170470", "Q81341"]},

    # Frankreich
    "kapetinger": {"de": "Kapetinger", "en": "House of Capet", "region": "frankreich", "wikidata": "Q178928", "rulers": ["Q159451", "Q129959", "Q81126", "Q124003", "Q908", "Q132545", "Q34258", "Q102928", "Q346", "Q172203", "Q32824", "Q8358", "Q8392", "Q229272"]},
    "valois": {"de": "Valois", "en": "House of Valois", "region": "frankreich", "wikidata": "Q182142", "rulers": ["Q8438", "Q131377", "Q167669", "Q168574", "Q133372", "Q83332", "Q134901"]},

    # Spanien
    "spanien_burgund": {"de": "Haus Burgund", "en": "Castilian House of Burgundy", "region": "spanien", "wikidata": "Q1191024", "rulers": ["Q312906", "Q356616", "Q356064", "Q314917", "Q318063", "Q314972", "Q272607", "Q110976", "Q356637", "Q312845", "Q312882", "Q299105"]},
    "trastamara": {"de": "Trastámara", "en": "House of Trastámara", "region": "spanien", "wikidata": "Q510403", "rulers": ["Q312104", "Q310373", "Q270725", "Q219665", "Q310931", "Q45859", "Q12860"]},

    # Italien
    "hauteville": {"de": "Hauteville", "en": "House of Hauteville", "region": "italien", "wikidata": "Q830200", "rulers": ["Q193649", "Q367468", "Q367425", "Q367429"]},
    "anjou": {"de": "Anjou", "en": "Capetian House of Anjou", "region": "italien", "wikidata": "Q282512", "rulers": ["Q184617", "Q208571", "Q290710", "Q229618"]}
}

def fetch_wikidata_details(qids):
    """Fetches details for a list of Wikidata QIDs in batch requests."""
    entity_data = {}
    qid_list = list(qids)
    batch_size = 40
    for i in range(0, len(qid_list), batch_size):
        batch = qid_list[i:i+batch_size]
        qids_str = "|".join(batch)
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qids_str}&props=labels|descriptions|claims&format=json"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'HECTOR-Editor/1.0 (https://github.com/bcdhbonn/hector-editor; langm@uni-bonn.de) Python-urllib/3.x'
        })
        
        print(f"  Fetching batch {i // batch_size + 1} ({len(batch)} entities)...")
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                entities = data.get("entities", {})
                entity_data.update(entities)
            time.sleep(0.5)  # Respectful delay
        except Exception as e:
            print(f"Error fetching batch: {e}")
            
    return entity_data

def fetch_roman_emperors():
    """Fetches all Roman Emperors with their date of death from Wikidata's SPARQL endpoint."""
    print("Querying Wikidata for Roman emperors with death dates via SPARQL...")
    query = """
    SELECT DISTINCT ?emperor ?label_de ?label_en ?desc_de ?desc_en ?gnd ?aat ?death_date WHERE {
      { ?emperor wdt:P39 wd:Q842606 . }
      UNION
      { ?emperor wdt:P31 wd:Q11696 . }
      
      OPTIONAL { ?emperor wdt:P570 ?death_date . }
      OPTIONAL {
        ?emperor rdfs:label ?label_de .
        FILTER(LANG(?label_de) = "de")
      }
      OPTIONAL {
        ?emperor rdfs:label ?label_en .
        FILTER(LANG(?label_en) = "en")
      }
      OPTIONAL {
        ?emperor schema:description ?desc_de .
        FILTER(LANG(?desc_de) = "de")
      }
      OPTIONAL {
        ?emperor schema:description ?desc_en .
        FILTER(LANG(?desc_en) = "en")
      }
      OPTIONAL { ?emperor wdt:P227 ?gnd . }
      OPTIONAL { ?emperor wdt:P1014 ?aat . }
    }
    """
    url = 'https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query) + '&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'HECTOR-Editor/1.0 (https://github.com/bcdhbonn/hector-editor; langm@uni-bonn.de) Python-urllib/3.x'
    })
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', {}).get('bindings', [])
            return results
    except Exception as e:
        print(f"Error querying Roman emperors: {e}")
        return []

def fetch_holy_roman_emperors():
    """Fetches all Holy Roman Emperors with their date of death from Wikidata's SPARQL endpoint."""
    print("Querying Wikidata for Holy Roman Emperors (Römisch-deutsche Kaiser) via SPARQL...")
    query = """
    SELECT DISTINCT ?emperor ?label_de ?label_en ?desc_de ?desc_en ?gnd ?aat ?death_date WHERE {
      ?emperor wdt:P39 wd:Q181765 .
      OPTIONAL { ?emperor wdt:P570 ?death_date . }
      OPTIONAL {
        ?emperor rdfs:label ?label_de .
        FILTER(LANG(?label_de) = "de")
      }
      OPTIONAL {
        ?emperor rdfs:label ?label_en .
        FILTER(LANG(?label_en) = "en")
      }
      OPTIONAL {
        ?emperor schema:description ?desc_de .
        FILTER(LANG(?desc_de) = "de")
      }
      OPTIONAL {
        ?emperor schema:description ?desc_en .
        FILTER(LANG(?desc_en) = "en")
      }
      OPTIONAL { ?emperor wdt:P227 ?gnd . }
      OPTIONAL { ?emperor wdt:P1014 ?aat . }
    }
    """
    url = 'https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query) + '&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'HECTOR-Editor/1.0 (https://github.com/bcdhbonn/hector-editor; langm@uni-bonn.de) Python-urllib/3.x'
    })
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', {}).get('bindings', [])
            return results
    except Exception as e:
        print(f"Error querying Holy Roman emperors: {e}")
        return []

def fetch_egyptian_dynasties():
    """Fetches all Egyptian Dynasties from Wikidata."""
    print("Querying Wikidata for Egyptian dynasties via SPARQL...")
    query = """
    SELECT DISTINCT ?dynasty ?label_de ?label_en WHERE {
      ?dynasty wdt:P31 wd:Q11876947 .
      OPTIONAL {
        ?dynasty rdfs:label ?label_de .
        FILTER(LANG(?label_de) = "de")
      }
      OPTIONAL {
        ?dynasty rdfs:label ?label_en .
        FILTER(LANG(?label_en) = "en")
      }
    }
    """
    url = 'https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query) + '&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'HECTOR-Editor/1.0 (https://github.com/bcdhbonn/hector-editor; langm@uni-bonn.de) Python-urllib/3.x'
    })
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('results', {}).get('bindings', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_pharaohs():
    """Fetches all Pharaohs of Ancient Egypt from Wikidata."""
    print("Querying Wikidata for Pharaohs via SPARQL...")
    query = """
    SELECT DISTINCT ?pharaoh ?label_de ?label_en ?desc_de ?desc_en ?dynasty ?gnd ?aat WHERE {
      { ?pharaoh wdt:P39 wd:Q37110 . }
      UNION
      { ?pharaoh wdt:P31 wd:Q134041 . }
      
      OPTIONAL {
        ?pharaoh wdt:P53 ?dynasty .
        ?dynasty wdt:P31 wd:Q11876947 .
      }
      OPTIONAL {
        ?pharaoh rdfs:label ?label_de .
        FILTER(LANG(?label_de) = "de")
      }
      OPTIONAL {
        ?pharaoh rdfs:label ?label_en .
        FILTER(LANG(?label_en) = "en")
      }
      OPTIONAL {
        ?pharaoh schema:description ?desc_de .
        FILTER(LANG(?desc_de) = "de")
      }
      OPTIONAL {
        ?pharaoh schema:description ?desc_en .
        FILTER(LANG(?desc_en) = "en")
      }
      OPTIONAL { ?pharaoh wdt:P227 ?gnd . }
      OPTIONAL { ?pharaoh wdt:P1014 ?aat . }
    }
    """
    url = 'https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query) + '&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'HECTOR-Editor/1.0 (https://github.com/bcdhbonn/hector-editor; langm@uni-bonn.de) Python-urllib/3.x'
    })
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('results', {}).get('bindings', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_wikidata_temporal_entities():
    """Queries all millennia and centuries from Wikidata to map QIDs."""
    print("Querying Wikidata for Millennia and Centuries QIDs...")
    query = """
    SELECT DISTINCT ?item ?label WHERE {
      { ?item wdt:P31/wdt:P279* wd:Q578 . } # Century
      UNION
      { ?item wdt:P31/wdt:P279* wd:Q36507 . } # Millennium
      ?item rdfs:label ?label .
      FILTER(LANG(?label) = "en")
    }
    """
    url = 'https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query) + '&format=json'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'HECTOR-Editor/1.0 (https://github.com/bcdhbonn/hector-editor; langm@uni-bonn.de) Python-urllib/3.x'
    })
    
    millennia_map = {}
    centuries_map = {}
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', {}).get('bindings', [])
            
            m_regex = re.compile(r'^(\d+)(?:st|nd|rd|th)\s+millennium(?:\s+(BC|AD|B\.C\.|A\.D\.))?$', re.IGNORECASE)
            c_regex = re.compile(r'^(\d+)(?:st|nd|rd|th)\s+century(?:\s+(BC|AD|B\.C\.|A\.D\.))?$', re.IGNORECASE)
            
            for r in results:
                qid = r['item']['value'].split('/')[-1]
                lbl = r['label']['value'].strip()
                
                m = m_regex.match(lbl)
                if m:
                    num = int(m.group(1))
                    era = m.group(2)
                    is_bc = era is not None and ('bc' in era.lower())
                    millennia_map[(num, is_bc)] = qid
                    continue
                    
                m = c_regex.match(lbl)
                if m:
                    num = int(m.group(1))
                    era = m.group(2)
                    is_bc = era is not None and ('bc' in era.lower())
                    centuries_map[(num, is_bc)] = qid
                    
    except Exception as e:
        print(f"Error fetching Wikidata temporal entities: {e}")
        
    return millennia_map, centuries_map

def slugify(text, prefix="emperor_"):
    """Creates a URL-safe, clean slug for concept URIs."""
    text = text.lower().strip()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "_", text)
    return prefix + text.strip("_")

def generate_temporal_grid(g, scheme, root_uri, millennia_wiki, centuries_wiki):
    """Generates the Millennia, Centuries, Halves, and Quarters chronological grid branch with polyhierarchical links for Neuzeit."""
    print("Generating chronological temporal grid...")
    grid_root = c_uri("temporal_grid_root")
    g.add((grid_root, RDF.type, SKOS.Concept))
    g.add((grid_root, SKOS.inScheme, scheme))
    g.add((grid_root, SKOS.prefLabel, Literal("Chronologisches Raster", lang="de")))
    g.add((grid_root, SKOS.prefLabel, Literal("Chronological Grid", lang="en")))
    g.add((grid_root, SKOS.definition, Literal("Ein strukturiertes Zeitraster aus Jahrtausenden, Jahrhunderten, Hälften und Vierteln.", lang="de")))
    g.add((grid_root, SKOS.definition, Literal("A structured grid of millennia, centuries, halves, and quarters.", lang="en")))
    g.add((grid_root, SKOS.broader, root_uri))

    def ord_suffix(num):
        if 11 <= (num % 100) <= 13:
            return f"{num}th"
        return f"{num}" + {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")

    # Millennia configurations
    millennia = [
        (3, True), (2, True), (1, True),
        (1, False), (2, False), (3, False)
    ]

    for m_num, is_bc in millennia:
        era_de = "v. Chr." if is_bc else "n. Chr."
        era_en = "BC" if is_bc else "AD"
        era_slug = "v_chr" if is_bc else "n_chr"

        m_uri = c_uri(f"millennium_{m_num}_{era_slug}")
        m_lbl_de = f"{m_num}. Jahrtausend {era_de}"
        m_lbl_en = f"{ord_suffix(m_num)} Millennium {era_en}"
        
        g.add((m_uri, RDF.type, SKOS.Concept))
        g.add((m_uri, SKOS.inScheme, scheme))
        g.add((m_uri, SKOS.prefLabel, Literal(m_lbl_de, lang="de")))
        g.add((m_uri, SKOS.prefLabel, Literal(m_lbl_en, lang="en")))
        g.add((m_uri, SKOS.broader, grid_root))

        m_qid = millennia_wiki.get((m_num, is_bc))
        if m_qid:
            g.add((m_uri, SKOS.exactMatch, URIRef(f"http://www.wikidata.org/entity/{m_qid}")))

        if not is_bc and m_num == 3:
            centuries = [21]
        elif is_bc:
            centuries = list(range(m_num * 10, (m_num - 1) * 10, -1))
        else:
            centuries = list(range((m_num - 1) * 10 + 1, m_num * 10 + 1))

        for c_num in centuries:
            c_uri_concept = c_uri(f"century_{c_num}_{era_slug}")
            c_lbl_de = f"{c_num}. Jahrhundert {era_de}"
            c_lbl_en = f"{ord_suffix(c_num)} Century {era_en}"
            
            if is_bc:
                c_start = c_num * 100
                c_end = (c_num - 1) * 100 + 1
                def_de = f"Zeitabschnitt von {c_start} {era_de} bis {c_end} {era_de}."
                def_en = f"Time period from {c_start} {era_en} to {c_end} {era_en}."
            else:
                c_start = (c_num - 1) * 100 + 1
                c_end = c_num * 100
                def_de = f"Zeitabschnitt von {c_start} {era_de} bis {c_end} {era_de}."
                def_en = f"Time period from {c_start} {era_en} to {c_end} {era_en}."

            g.add((c_uri_concept, RDF.type, SKOS.Concept))
            g.add((c_uri_concept, SKOS.inScheme, scheme))
            g.add((c_uri_concept, SKOS.prefLabel, Literal(c_lbl_de, lang="de")))
            g.add((c_uri_concept, SKOS.prefLabel, Literal(c_lbl_en, lang="en")))
            g.add((c_uri_concept, SKOS.definition, Literal(def_de, lang="de")))
            g.add((c_uri_concept, SKOS.definition, Literal(def_en, lang="en")))
            
            g.add((c_uri_concept, SKOS.broader, m_uri))

            if not is_bc and c_num >= 16:
                g.add((c_uri_concept, SKOS.broader, c_uri("neuzeit")))

            c_qid = centuries_wiki.get((c_num, is_bc))
            if c_qid:
                g.add((c_uri_concept, SKOS.exactMatch, URIRef(f"http://www.wikidata.org/entity/{c_qid}")))

            # Century Halves: 1st, 2nd
            for h in [1, 2]:
                h_uri = c_uri(f"half_{h}_century_{c_num}_{era_slug}")
                h_lbl_de = f"{h}. Hälfte {c_num}. Jh. {era_de}"
                h_lbl_en = f"{ord_suffix(h)} Half {ord_suffix(c_num)} Century {era_en}"
                
                if is_bc:
                    if h == 1:
                        h_start = c_start
                        h_end = c_start - 49
                    else:
                        h_start = c_start - 50
                        h_end = c_end
                else:
                    if h == 1:
                        h_start = c_start
                        h_end = c_start + 49
                    else:
                        h_start = c_start + 50
                        h_end = c_end
                        
                h_def_de = f"Hälfte eines Jahrhunderts von {h_start} {era_de} bis {h_end} {era_de}."
                h_def_en = f"Half of a century from {h_start} {era_en} to {h_end} {era_en}."

                g.add((h_uri, RDF.type, SKOS.Concept))
                g.add((h_uri, SKOS.inScheme, scheme))
                g.add((h_uri, SKOS.prefLabel, Literal(h_lbl_de, lang="de")))
                g.add((h_uri, SKOS.prefLabel, Literal(h_lbl_en, lang="en")))
                g.add((h_uri, SKOS.definition, Literal(h_def_de, lang="de")))
                g.add((h_uri, SKOS.definition, Literal(h_def_en, lang="en")))
                g.add((h_uri, SKOS.broader, c_uri_concept))

            # Century Quarters: 1st, 2nd, 3rd, 4th
            for q in [1, 2, 3, 4]:
                q_uri = c_uri(f"quarter_{q}_century_{c_num}_{era_slug}")
                q_lbl_de = f"{q}. Viertel {c_num}. Jh. {era_de}"
                q_lbl_en = f"{ord_suffix(q)} Quarter {ord_suffix(c_num)} Century {era_en}"
                
                if is_bc:
                    q_start = c_start - (q - 1) * 25
                    q_end = q_start - 24
                    q_def_de = f"Viertel-Jahrhundert von {q_start} {era_de} bis {q_end} {era_de}."
                    q_def_en = f"Quarter-century from {q_start} {era_en} to {q_end} {era_en}."
                else:
                    q_start = c_start + (q - 1) * 25
                    q_end = q_start + 24
                    q_def_de = f"Viertel-Jahrhundert von {q_start} {era_de} bis {q_end} {era_de}."
                    q_def_en = f"Quarter-century from {q_start} {era_en} to {q_end} {era_en}."

                h_parent_num = 1 if q <= 2 else 2
                h_parent_uri = c_uri(f"half_{h_parent_num}_century_{c_num}_{era_slug}")

                g.add((q_uri, RDF.type, SKOS.Concept))
                g.add((q_uri, SKOS.inScheme, scheme))
                g.add((q_uri, SKOS.prefLabel, Literal(q_lbl_de, lang="de")))
                g.add((q_uri, SKOS.prefLabel, Literal(q_lbl_en, lang="en")))
                g.add((q_uri, SKOS.definition, Literal(q_def_de, lang="de")))
                g.add((q_uri, SKOS.definition, Literal(q_def_en, lang="en")))
                g.add((q_uri, SKOS.broader, h_parent_uri))

def main():
    owl_file = "epochen.owl"
    output_dir = "hector_epochs"
    output_file = os.path.join(output_dir, "HECTOR_Epoch.ttl")
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(owl_file):
        print(f"Error: {owl_file} not found!")
        return

    print("Parsing epochen.owl graph...")
    g_owl = Graph()
    g_owl.parse(owl_file, format="xml")
    print(f"Loaded OWL graph (triples: {len(g_owl)})")
    
    # Extract Wikidata details for the 69 core concepts
    qids_to_fetch = set([v for v in WIKIDATA_MAPPING.values() if v])
    print(f"Querying Wikidata details for {len(qids_to_fetch)} unique entities...")
    wiki_data = fetch_wikidata_details(qids_to_fetch)
    print(f"Successfully retrieved data for {len(wiki_data)} entities.")

    g_out = Graph()
    g_out.bind("skos", SKOS)
    g_out.bind("rdf", RDF)
    g_out.bind("dcterms", URIRef("http://purl.org/dc/terms/"))
    g_out.bind("foaf", URIRef("http://xmlns.com/foaf/0.1/"))
    g_out.bind("hector_epochs", URIRef(NAMESPACE_BASE))

    # 1. Create unified concept scheme
    global_scheme = URIRef(f"{NAMESPACE_BASE}scheme")
    g_out.add((global_scheme, RDF.type, SKOS.ConceptScheme))
    g_out.add((global_scheme, SKOS.prefLabel, Literal("ArcheoInf Epochen (SKOS Version)", lang="de")))
    g_out.add((global_scheme, SKOS.prefLabel, Literal("ArcheoInf Epochs (SKOS Version)", lang="en")))
    g_out.add((global_scheme, SKOS.definition, Literal("A SKOS-compliant vocabulary for archaeological epochs, enriched with Wikidata, Getty AAT, and GND authorities.", lang="en")))
    g_out.add((global_scheme, SKOS.definition, Literal("Ein SKOS-konformes Vokabular für archäologische Epochen, angereichert mit Wikidata, Getty AAT und GND Identifikatoren.", lang="de")))

    # 2. Add all concepts defined in epochen.owl
    print("Processing and enriching core concepts...")
    owl_concepts = list(g_owl.subjects(RDF.type, SKOS.Concept))
    
    for oc in owl_concepts:
        abs_oc = c_uri(oc)
        g_out.add((abs_oc, RDF.type, SKOS.Concept))
        g_out.add((abs_oc, SKOS.inScheme, global_scheme))
        local_name = str(oc).split('/')[-1]
        
        lbl_de = g_owl.value(oc, SKOS.prefLabel)
        lbl_de_str = str(lbl_de).strip() if lbl_de else ""
        if not lbl_de_str:
            if local_name == "assyrien": lbl_de_str = "Assyrische Epoche"
            elif local_name == "eisenzeit_mittelmeer": lbl_de_str = "Eisenzeit Mediterranean"
            elif local_name == "spaetantike": lbl_de_str = "Spätantike"
            else: lbl_de_str = local_name.replace("_", " ").capitalize()
            
        lbl_en_str = ENGLISH_LABEL_OVERRIDES.get(local_name, lbl_de_str)
        
        g_out.add((abs_oc, SKOS.prefLabel, Literal(lbl_de_str, lang="de")))
        g_out.add((abs_oc, SKOS.prefLabel, Literal(lbl_en_str, lang="en")))
        
        for al in g_owl.objects(oc, SKOS.altLabel):
            g_out.add((abs_oc, SKOS.altLabel, al))
            
        for parent in g_owl.objects(oc, SKOS.broader):
            g_out.add((abs_oc, SKOS.broader, c_uri(parent)))
            
        for parent in g_owl.subjects(SKOS.narrower, oc):
            g_out.add((abs_oc, SKOS.broader, c_uri(parent)))
            
        qid = WIKIDATA_MAPPING.get(local_name)
        if qid and qid in wiki_data:
            entity = wiki_data[qid]
            desc_de = entity.get("descriptions", {}).get("de", {}).get("value")
            desc_en = entity.get("descriptions", {}).get("en", {}).get("value")
            
            if desc_de:
                g_out.add((abs_oc, SKOS.definition, Literal(desc_de, lang="de")))
            if desc_en:
                g_out.add((abs_oc, SKOS.definition, Literal(desc_en, lang="en")))
                
            wiki_uri = URIRef(f"http://www.wikidata.org/entity/{qid}")
            g_out.add((abs_oc, SKOS.exactMatch, wiki_uri))
            
            claims = entity.get("claims", {})
            if "P1014" in claims:
                try:
                    mainsnak = claims["P1014"][0].get("mainsnak", {})
                    aat_val = mainsnak.get("datavalue", {}).get("value")
                    if aat_val:
                        aat_uri = URIRef(f"http://vocab.getty.edu/aat/{aat_val}")
                        g_out.add((abs_oc, SKOS.exactMatch, aat_uri))
                except:
                    pass
                    
            if "P227" in claims:
                try:
                    mainsnak = claims["P227"][0].get("mainsnak", {})
                    gnd_val = mainsnak.get("datavalue", {}).get("value")
                    if gnd_val:
                        gnd_uri = URIRef(f"http://d-nb.info/gnd/{gnd_val}")
                        g_out.add((abs_oc, SKOS.exactMatch, gnd_uri))
                except:
                    pass

    # 3. Add Roman Emperors and Classify them Chronologically
    print("Fetching and adding Roman Emperors from Wikidata...")
    emperors_list = fetch_roman_emperors()
    
    deduped_emperors = {}
    for item in emperors_list:
        emp_uri_str = item['emperor']['value']
        emp_qid = emp_uri_str.split('/')[-1]
        
        lbl_de = item.get('label_de', {}).get('value')
        lbl_en = item.get('label_en', {}).get('value')
        desc_de = item.get('desc_de', {}).get('value', 'römischer Kaiser')
        desc_en = item.get('desc_en', {}).get('value', 'Roman Emperor')
        gnd = item.get('gnd', {}).get('value')
        aat = item.get('aat', {}).get('value')
        death_str = item.get('death_date', {}).get('value', '')
        
        if emp_qid not in deduped_emperors or (death_str and not deduped_emperors[emp_qid]['death']):
            deduped_emperors[emp_qid] = {
                'uri': emp_uri_str,
                'lbl_de': lbl_de,
                'lbl_en': lbl_en,
                'desc_de': desc_de,
                'desc_en': desc_en,
                'gnd': gnd,
                'aat': aat,
                'death': death_str
            }

    print(f"Adding {len(deduped_emperors)} deduplicated emperors into sub-periods...")
    for qid, emp in deduped_emperors.items():
        lbl_de = emp['lbl_de']
        lbl_en = emp['lbl_en']
        desc_de = emp['desc_de']
        desc_en = emp['desc_en']
        gnd = emp['gnd']
        aat = emp['aat']
        death_str = emp['death']
        
        year = None
        if death_str:
            m = re.match(r'^([+-]?\d+)', death_str)
            if m:
                year = int(m.group(1))
                
        if year is None:
            parent_uri = c_uri("roemische_kaiserzeit_spaet")
            sub_lbl = "Späte Kaiserzeit (Default)"
        elif year <= 235:
            parent_uri = c_uri("roemische_kaiserzeit_frueh")
            sub_lbl = f"Frühe Kaiserzeit (reg. bis {year} n. Chr.)"
        elif year <= 284:
            parent_uri = c_uri("roemische_kaiserzeit_mittel")
            sub_lbl = f"Mittlere Kaiserzeit (reg. bis {year} n. Chr.)"
        else:
            parent_uri = c_uri("roemische_kaiserzeit_spaet")
            sub_lbl = f"Späte Kaiserzeit (reg. bis {year} n. Chr.)"

        if not lbl_de:
            lbl_de = lbl_en if lbl_en else qid
        if not lbl_en:
            lbl_en = lbl_de
            
        emp_concept_uri = c_uri(slugify(lbl_en, "emperor_"))
        
        g_out.add((emp_concept_uri, RDF.type, SKOS.Concept))
        g_out.add((emp_concept_uri, SKOS.inScheme, global_scheme))
        g_out.add((emp_concept_uri, SKOS.prefLabel, Literal(lbl_de, lang="de")))
        g_out.add((emp_concept_uri, SKOS.prefLabel, Literal(lbl_en, lang="en")))
        
        desc_de_rich = f"{desc_de} ({sub_lbl})"
        desc_en_rich = f"{desc_en} (death year: {year if year is not None else 'unknown'})"
        g_out.add((emp_concept_uri, SKOS.definition, Literal(desc_de_rich, lang="de")))
        g_out.add((emp_concept_uri, SKOS.definition, Literal(desc_en_rich, lang="en")))
        g_out.add((emp_concept_uri, SKOS.broader, parent_uri))
        
        g_out.add((emp_concept_uri, SKOS.exactMatch, URIRef(emp['uri'])))
        if gnd:
            g_out.add((emp_concept_uri, SKOS.exactMatch, URIRef(f"http://d-nb.info/gnd/{gnd}")))
        if aat:
            g_out.add((emp_concept_uri, SKOS.exactMatch, URIRef(f"http://vocab.getty.edu/aat/{aat}")))

    # 4. Restructure Middle Ages (Mittelalter)
    print("Creating Middle Ages chronological sub-periods...")
    mittelalter_uri = c_uri("mittelalter")
    
    sub_periods = {
        "fruehmittelalter": {"de": "Frühmittelalter", "en": "Early Middle Ages", "def": "Epoche des europäischen Mittelalters von ca. 500 bis 1050 n. Chr."},
        "hochmittelalter": {"de": "Hochmittelalter", "en": "High Middle Ages", "def": "Epoche des europäischen Mittelalters von ca. 1050 bis 1250 n. Chr."},
        "spaetmittelalter": {"de": "Spätmittelalter", "en": "Late Middle Ages", "def": "Epoche des europäischen Mittelalters von ca. 1250 bis 1500 n. Chr."}
    }
    
    for k, v in sub_periods.items():
        sp_uri = c_uri(k)
        g_out.add((sp_uri, RDF.type, SKOS.Concept))
        g_out.add((sp_uri, SKOS.inScheme, global_scheme))
        g_out.add((sp_uri, SKOS.prefLabel, Literal(v["de"], lang="de")))
        g_out.add((sp_uri, SKOS.prefLabel, Literal(v["en"], lang="en")))
        g_out.add((sp_uri, SKOS.definition, Literal(v["def"], lang="de")))
        g_out.add((sp_uri, SKOS.broader, mittelalter_uri))

    # 4a. Create Medieval Regions/Countries & Dynasties
    print("Creating medieval country branches & dynasties...")
    for reg_key, reg_data in MEDIEVAL_REGIONS.items():
        reg_uri = c_uri(f"dynasty_region_{reg_key}")
        g_out.add((reg_uri, RDF.type, SKOS.Concept))
        g_out.add((reg_uri, SKOS.inScheme, global_scheme))
        g_out.add((reg_uri, SKOS.prefLabel, Literal(reg_data["de"], lang="de")))
        g_out.add((reg_uri, SKOS.prefLabel, Literal(reg_data["en"], lang="en")))
        g_out.add((reg_uri, SKOS.broader, mittelalter_uri))

    # Create Dynasties
    for dyn_key, dyn_data in MEDIEVAL_DYNASTIES.items():
        dyn_uri = c_uri(f"dynasty_{dyn_key}")
        g_out.add((dyn_uri, RDF.type, SKOS.Concept))
        g_out.add((dyn_uri, SKOS.inScheme, global_scheme))
        g_out.add((dyn_uri, SKOS.prefLabel, Literal(dyn_data["de"], lang="de")))
        g_out.add((dyn_uri, SKOS.prefLabel, Literal(dyn_data["en"], lang="en")))
        g_out.add((dyn_uri, SKOS.broader, c_uri(f"dynasty_region_{dyn_data['region']}")))
        if dyn_data.get("wikidata"):
            g_out.add((dyn_uri, SKOS.exactMatch, URIRef(f"http://www.wikidata.org/entity/{dyn_data['wikidata']}")))

    # Compile and Fetch all Medieval Rulers
    all_ruler_qids = set()
    for dyn_data in MEDIEVAL_DYNASTIES.values():
        all_ruler_qids.update(dyn_data["rulers"])
        
    print(f"Fetching details for {len(all_ruler_qids)} medieval rulers...")
    rulers_wiki_data = fetch_wikidata_details(all_ruler_qids)

    print("Adding medieval rulers to their dynasties...")
    for dyn_key, dyn_data in MEDIEVAL_DYNASTIES.items():
        dyn_uri = c_uri(f"dynasty_{dyn_key}")
        for r_qid in dyn_data["rulers"]:
            if r_qid in rulers_wiki_data:
                r_entity = rulers_wiki_data[r_qid]
                lbl_de = r_entity.get("labels", {}).get("de", {}).get("value")
                lbl_en = r_entity.get("labels", {}).get("en", {}).get("value")
                desc_de = r_entity.get("descriptions", {}).get("de", {}).get("value", "")
                desc_en = r_entity.get("descriptions", {}).get("en", {}).get("value", "")
                
                if not lbl_de:
                    lbl_de = lbl_en if lbl_en else r_qid
                if not lbl_en:
                    lbl_en = lbl_de
                    
                ruler_uri = c_uri(f"ruler_{r_qid.lower()}")
                g_out.add((ruler_uri, RDF.type, SKOS.Concept))
                g_out.add((ruler_uri, SKOS.inScheme, global_scheme))
                g_out.add((ruler_uri, SKOS.prefLabel, Literal(lbl_de, lang="de")))
                g_out.add((ruler_uri, SKOS.prefLabel, Literal(lbl_en, lang="en")))
                
                # Suffix description with dynasty name
                rich_desc_de = f"{desc_de} ({dyn_data['de']})" if desc_de else f"Herrscher ({dyn_data['de']})"
                rich_desc_en = f"{desc_en} ({dyn_data['en']})" if desc_en else f"Ruler ({dyn_data['en']})"
                g_out.add((ruler_uri, SKOS.definition, Literal(rich_desc_de, lang="de")))
                g_out.add((ruler_uri, SKOS.definition, Literal(rich_desc_en, lang="en")))
                
                g_out.add((ruler_uri, SKOS.broader, dyn_uri))
                
                g_out.add((ruler_uri, SKOS.exactMatch, URIRef(f"http://www.wikidata.org/entity/{r_qid}")))
                
                # Fetch GND/AAT claims if present
                claims = r_entity.get("claims", {})
                if "P227" in claims:
                    try:
                        gnd_val = claims["P227"][0]["mainsnak"]["datavalue"]["value"]
                        g_out.add((ruler_uri, SKOS.exactMatch, URIRef(f"http://d-nb.info/gnd/{gnd_val}")))
                    except: pass
                if "P1014" in claims:
                    try:
                        aat_val = claims["P1014"][0]["mainsnak"]["datavalue"]["value"]
                        g_out.add((ruler_uri, SKOS.exactMatch, URIRef(f"http://vocab.getty.edu/aat/{aat_val}")))
                    except: pass

    # 4b. Fetch and Add Holy Roman Emperors (Modern ones post-1500 only)
    print("Fetching and adding Holy Roman Emperors...")
    hre_list = fetch_holy_roman_emperors()
    
    deduped_hre = {}
    for item in hre_list:
        hre_uri_str = item['emperor']['value']
        hre_qid = hre_uri_str.split('/')[-1]
        
        lbl_de = item.get('label_de', {}).get('value')
        lbl_en = item.get('label_en', {}).get('value')
        desc_de = item.get('desc_de', {}).get('value', 'römisch-deutscher Kaiser')
        desc_en = item.get('desc_en', {}).get('value', 'Holy Roman Emperor')
        gnd = item.get('gnd', {}).get('value')
        aat = item.get('aat', {}).get('value')
        death_str = item.get('death_date', {}).get('value', '')
        
        if hre_qid not in deduped_hre or (death_str and not deduped_hre[hre_qid]['death']):
            deduped_hre[hre_qid] = {
                'uri': hre_uri_str,
                'lbl_de': lbl_de,
                'lbl_en': lbl_en,
                'desc_de': desc_de,
                'desc_en': desc_en,
                'gnd': gnd,
                'aat': aat,
                'death': death_str
            }

    print(f"Adding modern Holy Roman Emperors to Neuzeit centuries...")
    for qid, emp in deduped_hre.items():
        lbl_de = emp['lbl_de']
        lbl_en = emp['lbl_en']
        desc_de = emp['desc_de']
        desc_en = emp['desc_en']
        gnd = emp['gnd']
        aat = emp['aat']
        death_str = emp['death']
        
        year = None
        if death_str:
            m = re.match(r'^([+-]?\d+)', death_str)
            if m:
                year = int(m.group(1))
                
        if not lbl_de:
            lbl_de = lbl_en if lbl_en else qid
        if not lbl_en:
            lbl_en = lbl_de
            
        if year is not None and year > 1500:
            c_num = (year - 1) // 100 + 1
            parent_uri = c_uri(f"century_{c_num}_n_chr")
            era_lbl = f"{c_num}. Jahrhundert n. Chr. (gest. {year} n. Chr.)"

            emp_concept_uri = c_uri(slugify(lbl_en, "hre_"))
            
            g_out.add((emp_concept_uri, RDF.type, SKOS.Concept))
            g_out.add((emp_concept_uri, SKOS.inScheme, global_scheme))
            g_out.add((emp_concept_uri, SKOS.prefLabel, Literal(lbl_de, lang="de")))
            g_out.add((emp_concept_uri, SKOS.prefLabel, Literal(lbl_en, lang="en")))
            
            desc_de_rich = f"{desc_de} ({era_lbl})"
            desc_en_rich = f"{desc_en} (death year: {year if year is not None else 'unknown'})"
            g_out.add((emp_concept_uri, SKOS.definition, Literal(desc_de_rich, lang="de")))
            g_out.add((emp_concept_uri, SKOS.definition, Literal(desc_en_rich, lang="en")))
            g_out.add((emp_concept_uri, SKOS.broader, parent_uri))
            
            g_out.add((emp_concept_uri, SKOS.exactMatch, URIRef(emp['uri'])))
            if gnd:
                g_out.add((emp_concept_uri, SKOS.exactMatch, URIRef(f"http://d-nb.info/gnd/{gnd}")))
            if aat:
                g_out.add((emp_concept_uri, SKOS.exactMatch, URIRef(f"http://vocab.getty.edu/aat/{aat}")))

    # 5. Add Egyptian Kingdoms, Dynasties, and Pharaohs
    print("Generating Egyptian Kingdoms...")
    egypt_root_uri = c_uri("altesaegypten")
    
    for key, data in EGYPT_KINGDOMS.items():
        k_uri = c_uri(f"egypt_kingdom_{key}")
        g_out.add((k_uri, RDF.type, SKOS.Concept))
        g_out.add((k_uri, SKOS.inScheme, global_scheme))
        g_out.add((k_uri, SKOS.prefLabel, Literal(data["de"], lang="de")))
        g_out.add((k_uri, SKOS.prefLabel, Literal(data["en"], lang="en")))
        g_out.add((k_uri, SKOS.broader, egypt_root_uri))

    # Fetch and write Dynasties
    dynasties_list = fetch_egyptian_dynasties()
    deduped_dynasties = {}
    for item in dynasties_list:
        dyn_uri_str = item['dynasty']['value']
        dyn_qid = dyn_uri_str.split('/')[-1]
        lbl_de = item.get('label_de', {}).get('value')
        lbl_en = item.get('label_en', {}).get('value')
        
        if not lbl_de:
            lbl_de = lbl_en if lbl_en else dyn_qid
        if not lbl_en:
            lbl_en = lbl_de
            
        deduped_dynasties[dyn_qid] = {
            'uri': dyn_uri_str,
            'lbl_de': lbl_de,
            'lbl_en': lbl_en
        }

    print(f"Adding {len(deduped_dynasties)} Dynasties to Kingdoms...")
    for qid, dyn in deduped_dynasties.items():
        dyn_uri = c_uri(f"egypt_dynasty_{qid.lower()}")
        g_out.add((dyn_uri, RDF.type, SKOS.Concept))
        g_out.add((dyn_uri, SKOS.inScheme, global_scheme))
        g_out.add((dyn_uri, SKOS.prefLabel, Literal(dyn['lbl_de'], lang="de")))
        g_out.add((dyn_uri, SKOS.prefLabel, Literal(dyn['lbl_en'], lang="en")))
        g_out.add((dyn_uri, SKOS.exactMatch, URIRef(dyn['uri'])))
        
        kingdom_key = DYNASTY_TO_KINGDOM.get(qid, "no_dynasty_fallback")
        parent_k_uri = c_uri(f"egypt_kingdom_{kingdom_key}")
        g_out.add((dyn_uri, SKOS.broader, parent_k_uri))

    # Fetch and write Pharaohs
    pharaohs_list = fetch_pharaohs()
    deduped_pharaohs = {}
    for item in pharaohs_list:
        ph_uri_str = item['pharaoh']['value']
        ph_qid = ph_uri_str.split('/')[-1]
        
        lbl_de = item.get('label_de', {}).get('value')
        lbl_en = item.get('label_en', {}).get('value')
        desc_de = item.get('desc_de', {}).get('value', 'ägyptischer Pharao')
        desc_en = item.get('desc_en', {}).get('value', 'Pharaoh of Egypt')
        dynasty_qid = item.get('dynasty', {}).get('value', '').split('/')[-1]
        gnd = item.get('gnd', {}).get('value')
        aat = item.get('aat', {}).get('value')
        
        if ph_qid not in deduped_pharaohs or (dynasty_qid and not deduped_pharaohs[ph_qid]['dynasty']):
            deduped_pharaohs[ph_qid] = {
                'uri': ph_uri_str,
                'lbl_de': lbl_de,
                'lbl_en': lbl_en,
                'desc_de': desc_de,
                'desc_en': desc_en,
                'dynasty': dynasty_qid,
                'gnd': gnd,
                'aat': aat
            }

    print(f"Adding {len(deduped_pharaohs)} Pharaohs to Dynasties...")
    for qid, ph in deduped_pharaohs.items():
        lbl_de = ph['lbl_de']
        lbl_en = ph['lbl_en']
        desc_de = ph['desc_de']
        desc_en = ph['desc_en']
        dynasty_qid = ph['dynasty']
        gnd = ph['gnd']
        aat = ph['aat']
        
        if not lbl_de:
            lbl_de = lbl_en if lbl_en else qid
        if not lbl_en:
            lbl_en = lbl_de
            
        ph_uri = c_uri(f"pharaoh_{qid.lower()}")
        g_out.add((ph_uri, RDF.type, SKOS.Concept))
        g_out.add((ph_uri, SKOS.inScheme, global_scheme))
        g_out.add((ph_uri, SKOS.prefLabel, Literal(lbl_de, lang="de")))
        g_out.add((ph_uri, SKOS.prefLabel, Literal(lbl_en, lang="en")))
        g_out.add((ph_uri, SKOS.definition, Literal(desc_de, lang="de")))
        g_out.add((ph_uri, SKOS.definition, Literal(desc_en, lang="en")))
        
        g_out.add((ph_uri, SKOS.exactMatch, URIRef(ph['uri'])))
        if gnd:
            g_out.add((ph_uri, SKOS.exactMatch, URIRef(f"http://d-nb.info/gnd/{gnd}")))
        if aat:
            g_out.add((ph_uri, SKOS.exactMatch, URIRef(f"http://vocab.getty.edu/aat/{aat}")))
            
        if dynasty_qid and dynasty_qid in deduped_dynasties:
            parent_dyn_uri = c_uri(f"egypt_dynasty_{dynasty_qid.lower()}")
            g_out.add((ph_uri, SKOS.broader, parent_dyn_uri))
        else:
            fallback_uri = c_uri("egypt_kingdom_no_dynasty_fallback")
            g_out.add((ph_uri, SKOS.broader, fallback_uri))

    # 6. Generate Chronological Temporal Grid with Wikidata exactMatch (no prefixes)
    millennia_wiki, centuries_wiki = fetch_wikidata_temporal_entities()
    epoche_uri = c_uri("epoche")
    generate_temporal_grid(g_out, global_scheme, epoche_uri, millennia_wiki, centuries_wiki)

    # 7. Add Three Big Wars to their respective Century Concepts
    print("Adding three major wars under Modern Period centuries...")
    wars = [
        {
            "uri": "dreissigjaehriger_krieg",
            "parent": "century_17_n_chr",
            "lbl_de": "Dreißigjähriger Krieg",
            "lbl_en": "Thirty Years' War",
            "def_de": "Ein Konflikt um die Vormachtstellung im Heiligen Römischen Reich und in Europa von 1618 bis 1648.",
            "def_en": "A series of wars in Central Europe between 1618 and 1648.",
            "wikidata": "http://www.wikidata.org/entity/Q134053"
        },
        {
            "uri": "erster_weltkrieg",
            "parent": "century_20_n_chr",
            "lbl_de": "Erster Weltkrieg",
            "lbl_en": "World War I",
            "def_de": "Ein globaler Krieg von 1914 bis 1918, der in Europa begann.",
            "def_en": "A global war originating in Europe that lasted from 1914 to 1918.",
            "wikidata": "http://www.wikidata.org/entity/Q361"
        },
        {
            "uri": "zweiter_weltkrieg",
            "parent": "century_20_n_chr",
            "lbl_de": "Zweiter Weltkrieg",
            "lbl_en": "World War II",
            "def_de": "Ein globaler Konflikt von 1939 bis 1945, an dem die große Mehrheit der Länder der Welt beteiligt war.",
            "def_en": "A global war that lasted from 1939 to 1945.",
            "wikidata": "http://www.wikidata.org/entity/Q362"
        }
    ]
    
    for w in wars:
        w_uri = c_uri(w["uri"])
        g_out.add((w_uri, RDF.type, SKOS.Concept))
        g_out.add((w_uri, SKOS.inScheme, global_scheme))
        g_out.add((w_uri, SKOS.prefLabel, Literal(w["lbl_de"], lang="de")))
        g_out.add((w_uri, SKOS.prefLabel, Literal(w["lbl_en"], lang="en")))
        g_out.add((w_uri, SKOS.definition, Literal(w["def_de"], lang="de")))
        g_out.add((w_uri, SKOS.definition, Literal(w["def_en"], lang="en")))
        g_out.add((w_uri, SKOS.broader, c_uri(w["parent"])))
        g_out.add((w_uri, SKOS.exactMatch, URIRef(w["wikidata"])))

    # 8. Apply structural hierarchy fixes
    print("Applying structural hierarchy fixes...")
    eisenzeit_uri = c_uri("eisenzeit")
    antike_uri = c_uri("antike")
    kaiserzeit_uri = c_uri("roemische_kaiserzeit")
    
    g_out.add((c_uri("eisenzeit_mittelmeer"), SKOS.broader, eisenzeit_uri))
    g_out.add((c_uri("spaetantike"), SKOS.broader, antike_uri))
    g_out.add((c_uri("roemische_kaiserzeit_frueh"), SKOS.broader, kaiserzeit_uri))
    g_out.add((c_uri("roemische_kaiserzeit_mittel"), SKOS.broader, kaiserzeit_uri))
    g_out.add((c_uri("roemische_kaiserzeit_spaet"), SKOS.broader, kaiserzeit_uri))

    g_out.add((epoche_uri, SKOS.topConceptOf, global_scheme))
    g_out.add((global_scheme, SKOS.hasTopConcept, epoche_uri))
    g_out.remove((epoche_uri, SKOS.broader, None))

    print(f"Saving enriched SKOS graph to {output_file}...")
    g_out.serialize(destination=output_file, format="turtle")
    print("Done! Converted successfully.")

if __name__ == "__main__":
    main()
