"""Comprehensive metadata enrichment for Bible chunks."""

import re
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass

# ============================================================================
# LITERARY METADATA
# ============================================================================

# Author attribution for all 66 books
BOOK_AUTHORS = {
    # Torah (Pentateuch)
    "Genesis": "Moses", "Exodus": "Moses", "Leviticus": "Moses",
    "Numbers": "Moses", "Deuteronomy": "Moses",

    # Historical Books
    "Joshua": "Joshua", "Judges": "Unknown", "Ruth": "Unknown",
    "I Samuel": "Samuel", "II Samuel": "Unknown",
    "I Kings": "Unknown", "II Kings": "Unknown",
    "I Chronicles": "Ezra", "II Chronicles": "Ezra",
    "Ezra": "Ezra", "Nehemiah": "Nehemiah", "Esther": "Unknown",

    # Poetry & Wisdom
    "Job": "Unknown", "Psalms": "David (and others)",
    "Proverbs": "Solomon (and others)", "Ecclesiastes": "Solomon",
    "Song of Solomon": "Solomon",

    # Major Prophets
    "Isaiah": "Isaiah", "Jeremiah": "Jeremiah",
    "Lamentations": "Jeremiah", "Ezekiel": "Ezekiel", "Daniel": "Daniel",

    # Minor Prophets
    "Hosea": "Hosea", "Joel": "Joel", "Amos": "Amos",
    "Obadiah": "Obadiah", "Jonah": "Jonah", "Micah": "Micah",
    "Nahum": "Nahum", "Habakkuk": "Habakkuk", "Zephaniah": "Zephaniah",
    "Haggai": "Haggai", "Zechariah": "Zechariah", "Malachi": "Malachi",

    # Gospels & Acts
    "Matthew": "Matthew", "Mark": "Mark", "Luke": "Luke",
    "John": "John", "Acts": "Luke",

    # Pauline Epistles
    "Romans": "Paul", "I Corinthians": "Paul", "II Corinthians": "Paul",
    "Galatians": "Paul", "Ephesians": "Paul", "Philippians": "Paul",
    "Colossians": "Paul", "I Thessalonians": "Paul", "II Thessalonians": "Paul",
    "I Timothy": "Paul", "II Timothy": "Paul", "Titus": "Paul", "Philemon": "Paul",

    # General Epistles
    "Hebrews": "Unknown (possibly Paul)", "James": "James (brother of Jesus)",
    "I Peter": "Peter", "II Peter": "Peter",
    "I John": "John", "II John": "John", "III John": "John",
    "Jude": "Jude (brother of Jesus)", "Revelation of John": "John",
}

# Composition dates (using scholarly consensus where appropriate)
BOOK_DATES = {
    # Torah
    "Genesis": "1400 BCE (traditional) / 1000-400 BCE (critical)",
    "Exodus": "1400 BCE (traditional) / 1000-400 BCE (critical)",
    "Leviticus": "1400 BCE (traditional) / 1000-400 BCE (critical)",
    "Numbers": "1400 BCE (traditional) / 1000-400 BCE (critical)",
    "Deuteronomy": "1400 BCE (traditional) / 1000-400 BCE (critical)",

    # Historical
    "Joshua": "1200 BCE (traditional) / 600 BCE (critical)",
    "Judges": "1000 BCE", "Ruth": "1000 BCE",
    "I Samuel": "900 BCE", "II Samuel": "900 BCE",
    "I Kings": "550 BCE", "II Kings": "550 BCE",
    "I Chronicles": "400 BCE", "II Chronicles": "400 BCE",
    "Ezra": "400 BCE", "Nehemiah": "400 BCE", "Esther": "400 BCE",

    # Poetry & Wisdom
    "Job": "Unknown (possibly 2000-400 BCE)",
    "Psalms": "1000-400 BCE (compiled)",
    "Proverbs": "900-700 BCE",
    "Ecclesiastes": "300 BCE",
    "Song of Solomon": "900 BCE (traditional) / 400 BCE (critical)",

    # Major Prophets
    "Isaiah": "740-680 BCE (chapters 1-39), 540 BCE (40-66)",
    "Jeremiah": "627-580 BCE", "Lamentations": "586 BCE",
    "Ezekiel": "593-571 BCE", "Daniel": "165 BCE (critical) / 540 BCE (traditional)",

    # Minor Prophets
    "Hosea": "750 BCE", "Joel": "400 BCE", "Amos": "760 BCE",
    "Obadiah": "586 BCE", "Jonah": "760 BCE", "Micah": "735 BCE",
    "Nahum": "612 BCE", "Habakkuk": "600 BCE", "Zephaniah": "640 BCE",
    "Haggai": "520 BCE", "Zechariah": "520 BCE", "Malachi": "450 BCE",

    # Gospels & Acts
    "Matthew": "80-90 CE", "Mark": "65-70 CE",
    "Luke": "80-90 CE", "John": "90-110 CE", "Acts": "80-90 CE",

    # Pauline Epistles
    "Romans": "57 CE", "I Corinthians": "55 CE", "II Corinthians": "56 CE",
    "Galatians": "49 CE", "Ephesians": "60-62 CE", "Philippians": "61-62 CE",
    "Colossians": "60-62 CE", "I Thessalonians": "51 CE", "II Thessalonians": "51-52 CE",
    "I Timothy": "63 CE", "II Timothy": "67 CE", "Titus": "63 CE", "Philemon": "60 CE",

    # General Epistles
    "Hebrews": "60-90 CE", "James": "45-50 CE",
    "I Peter": "60-64 CE", "II Peter": "65-68 CE",
    "I John": "90-110 CE", "II John": "90-110 CE", "III John": "90-110 CE",
    "Jude": "65-80 CE", "Revelation of John": "95 CE",
}

# Primary audience/recipients
BOOK_AUDIENCES = {
    # Epistles (explicit recipients)
    "Romans": "Church in Rome",
    "I Corinthians": "Church in Corinth",
    "II Corinthians": "Church in Corinth",
    "Galatians": "Churches in Galatia",
    "Ephesians": "Church in Ephesus (and possibly circular letter)",
    "Philippians": "Church in Philippi",
    "Colossians": "Church in Colossae",
    "I Thessalonians": "Church in Thessalonica",
    "II Thessalonians": "Church in Thessalonica",
    "I Timothy": "Timothy (pastoral letter)",
    "II Timothy": "Timothy (pastoral letter)",
    "Titus": "Titus (pastoral letter)",
    "Philemon": "Philemon (personal letter)",
    "Hebrews": "Jewish Christians (possibly in Rome)",
    "James": "Jewish Christians in diaspora",
    "I Peter": "Christians in Asia Minor",
    "II Peter": "Christians in Asia Minor",
    "I John": "Church communities in Asia Minor",
    "II John": "Elect lady and her children",
    "III John": "Gaius",
    "Jude": "Jewish Christians",
    "Revelation of John": "Seven churches in Asia Minor",

    # Gospels
    "Matthew": "Jewish Christians",
    "Mark": "Gentile Christians (possibly in Rome)",
    "Luke": "Theophilus and Gentile Christians",
    "John": "All believers (emphasis on Greek-speaking world)",
}

# Original languages
BOOK_LANGUAGES = {
    # OT books in Hebrew (with some Aramaic sections)
    **{book: "Hebrew" for book in [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "I Samuel", "II Samuel",
        "I Kings", "II Kings", "I Chronicles", "II Chronicles",
        "Nehemiah", "Esther", "Job", "Psalms",
        "Proverbs", "Ecclesiastes", "Song of Solomon",
        "Isaiah", "Jeremiah", "Lamentations", "Hosea", "Joel", "Amos", "Obadiah", "Jonah",
        "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi",
    ]},

    # NT books in Koine Greek
    **{book: "Greek" for book in [
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "I Corinthians", "II Corinthians",
        "Galatians", "Ephesians", "Philippians", "Colossians",
        "I Thessalonians", "II Thessalonians",
        "I Timothy", "II Timothy", "Titus", "Philemon",
        "Hebrews", "James", "I Peter", "II Peter",
        "I John", "II John", "III John", "Jude",
        "Revelation of John",
    ]},

    # Books with significant Aramaic sections
    "Ezra": "Hebrew/Aramaic",
    "Daniel": "Hebrew/Aramaic",
    "Ezekiel": "Hebrew",
}

# ============================================================================
# HISTORICAL/CHRONOLOGICAL METADATA
# ============================================================================

# Biblical eras for narrative context
BIBLICAL_ERAS = {
    # Primeval History
    "Genesis": ["primeval_history", "patriarchs", "egyptian_sojourn"],
    "Exodus": ["exodus", "wilderness"],
    "Leviticus": ["wilderness"],
    "Numbers": ["wilderness"],
    "Deuteronomy": ["wilderness"],

    # Conquest & Settlement
    "Joshua": ["conquest"],
    "Judges": ["judges"],
    "Ruth": ["judges"],

    # United Monarchy
    "I Samuel": ["united_kingdom"],
    "II Samuel": ["united_kingdom"],
    "I Kings": ["united_kingdom", "divided_kingdom"],
    "II Kings": ["divided_kingdom", "exile"],

    # Post-Exilic
    "I Chronicles": ["united_kingdom"],
    "II Chronicles": ["united_kingdom", "divided_kingdom"],
    "Ezra": ["post_exile"],
    "Nehemiah": ["post_exile"],
    "Esther": ["exile"],

    # Wisdom & Poetry (various eras)
    "Job": ["patriarchs"],  # Traditionally dated to patriarchal period
    "Psalms": ["united_kingdom"],  # Primarily Davidic era
    "Proverbs": ["united_kingdom"],  # Solomon's era
    "Ecclesiastes": ["united_kingdom"],  # Solomon's era
    "Song of Solomon": ["united_kingdom"],  # Solomon's era

    # Major Prophets
    "Isaiah": ["divided_kingdom"],
    "Jeremiah": ["divided_kingdom", "exile"],
    "Lamentations": ["exile"],
    "Ezekiel": ["exile"],
    "Daniel": ["exile", "post_exile"],

    # Minor Prophets
    "Hosea": ["divided_kingdom"],
    "Joel": ["post_exile"],
    "Amos": ["divided_kingdom"],
    "Obadiah": ["exile"],
    "Jonah": ["divided_kingdom"],
    "Micah": ["divided_kingdom"],
    "Nahum": ["divided_kingdom"],
    "Habakkuk": ["divided_kingdom"],
    "Zephaniah": ["divided_kingdom"],
    "Haggai": ["post_exile"],
    "Zechariah": ["post_exile"],
    "Malachi": ["post_exile"],

    # Second Temple Period
    "Matthew": ["second_temple"],
    "Mark": ["second_temple"],
    "Luke": ["second_temple"],
    "John": ["second_temple"],
    "Acts": ["apostolic_age"],

    # NT Epistles
    **{book: ["apostolic_age"] for book in [
        "Romans", "I Corinthians", "II Corinthians",
        "Galatians", "Ephesians", "Philippians", "Colossians",
        "I Thessalonians", "II Thessalonians",
        "I Timothy", "II Timothy", "Titus", "Philemon",
        "Hebrews", "James", "I Peter", "II Peter",
        "I John", "II John", "III John", "Jude",
    ]},

    "Revelation of John": ["apostolic_age", "roman_persecution"],
}

ERA_DESCRIPTIONS = {
    "primeval_history": "Creation to Abraham (Genesis 1-11)",
    "patriarchs": "Abraham, Isaac, Jacob, Joseph (2000-1800 BCE)",
    "egyptian_sojourn": "Israel in Egypt (1800-1400 BCE)",
    "exodus": "Deliverance from Egypt (1400 BCE)",
    "wilderness": "Desert wandering (1400-1360 BCE)",
    "conquest": "Conquest of Canaan (1400-1350 BCE)",
    "judges": "Tribal confederation (1350-1050 BCE)",
    "united_kingdom": "Saul, David, Solomon (1050-930 BCE)",
    "divided_kingdom": "Israel and Judah (930-586 BCE)",
    "exile": "Babylonian captivity (586-538 BCE)",
    "post_exile": "Return and rebuilding (538-400 BCE)",
    "intertestamental": "Between OT and NT (400 BCE - 4 BCE)",
    "second_temple": "Ministry of Jesus (4 BCE - 30 CE)",
    "apostolic_age": "Early church (30-100 CE)",
    "roman_persecution": "Imperial persecution (64-313 CE)",
}

# ============================================================================
# THEOLOGICAL/TOPICAL METADATA
# ============================================================================

# Major theological themes by book
THEOLOGICAL_THEMES = {
    "Genesis": ["creation", "covenant", "providence", "faith"],
    "Exodus": ["redemption", "law", "covenant", "holiness"],
    "Leviticus": ["holiness", "atonement", "sacrifice", "priesthood"],
    "Numbers": ["wilderness", "faith", "rebellion", "covenant"],
    "Deuteronomy": ["law", "covenant", "obedience", "blessing"],
    "Psalms": ["worship", "prayer", "lament", "praise", "messianic_prophecy"],
    "Proverbs": ["wisdom", "righteousness", "discipline", "fear_of_God"],
    "Isaiah": ["holiness", "judgment", "messiah", "remnant", "salvation"],
    "Jeremiah": ["judgment", "new_covenant", "remnant", "restoration"],
    "Matthew": ["kingdom_of_heaven", "messiah", "fulfillment", "discipleship"],
    "Mark": ["servanthood", "suffering", "messiah", "discipleship"],
    "Luke": ["compassion", "salvation", "Holy_Spirit", "prayer"],
    "John": ["eternal_life", "deity_of_christ", "faith", "love"],
    "Acts": ["Holy_Spirit", "church", "missions", "persecution"],
    "Romans": ["justification", "faith", "grace", "law", "salvation"],
    "I Corinthians": ["church", "spiritual_gifts", "love", "resurrection"],
    "II Corinthians": ["suffering", "ministry", "reconciliation", "grace"],
    "Galatians": ["justification", "faith", "law", "freedom"],
    "Ephesians": ["church", "unity", "grace", "spiritual_warfare"],
    "Philippians": ["joy", "humility", "contentment", "Christ"],
    "Colossians": ["supremacy_of_christ", "false_teaching", "new_life"],
    "I Thessalonians": ["second_coming", "holiness", "encouragement"],
    "II Thessalonians": ["second_coming", "perseverance", "judgment"],
    "Hebrews": ["superiority_of_christ", "faith", "new_covenant"],
    "James": ["faith_and_works", "wisdom", "trials", "prayer"],
    "I Peter": ["suffering", "holiness", "hope", "submission"],
    "II Peter": ["false_teaching", "growth", "second_coming"],
    "I John": ["love", "truth", "fellowship", "assurance"],
    "Revelation of John": ["prophecy", "judgment", "victory", "new_creation"],
}

# ============================================================================
# NAMED ENTITY RECOGNITION
# ============================================================================

# Common biblical names and entities
PERSON_ENTITIES = {
    # Major OT figures
    "Abraham", "Isaac", "Jacob", "Joseph", "Moses", "Aaron",
    "Joshua", "Gideon", "Samuel", "Saul", "David", "Solomon",
    "Elijah", "Elisha", "Isaiah", "Jeremiah", "Ezekiel", "Daniel",

    # Major NT figures
    "Jesus", "John the Baptist", "Mary", "Peter", "James", "John",
    "Paul", "Timothy", "Titus", "Barnabas", "Stephen", "Philip",

    # Groups
    "Pharisees", "Sadducees", "Essenes", "Zealots", "Scribes",
    "Israel", "Judah", "Israelites", "Jews", "Gentiles",
}

PLACE_ENTITIES = {
    # OT Geography
    "Eden", "Ur", "Haran", "Canaan", "Egypt", "Sinai", "Wilderness",
    "Jerusalem", "Bethlehem", "Hebron", "Samaria", "Babylon", "Assyria",

    # NT Geography
    "Nazareth", "Galilee", "Judea", "Jerusalem", "Bethlehem",
    "Capernaum", "Damascus", "Antioch", "Ephesus", "Corinth",
    "Philippi", "Thessalonica", "Rome", "Asia Minor",

    # Geographic features
    "Jordan River", "Dead Sea", "Sea of Galilee", "Red Sea",
    "Mount Sinai", "Mount Zion", "Mount of Olives",
}


def extract_named_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract named entities (people, places) from text.

    Simple regex-based extraction for common Biblical names.
    Could be enhanced with spaCy NER or custom model.
    """
    entities = {"people": [], "places": [], "groups": []}

    # Extract people
    for person in PERSON_ENTITIES:
        if re.search(r'\b' + re.escape(person) + r'\b', text, re.IGNORECASE):
            entities["people"].append(person)

    # Extract places
    for place in PLACE_ENTITIES:
        if re.search(r'\b' + re.escape(place) + r'\b', text, re.IGNORECASE):
            entities["places"].append(place)

    return entities


# ============================================================================
# METADATA AGGREGATION
# ============================================================================

def get_comprehensive_metadata(
    book_name: str,
    chapter: int,
    verse_start: int,
    verse_end: int,
    content: str,
    genre: str,
) -> Dict[str, Any]:
    """
    Build comprehensive metadata for a chunk.

    Aggregates all metadata sources into single structure.
    """
    metadata = {
        # Literary metadata
        "literary_analysis": {
            "author": BOOK_AUTHORS.get(book_name, "Unknown"),
            "approximate_date": BOOK_DATES.get(book_name, "Unknown"),
            "original_language": BOOK_LANGUAGES.get(book_name, "Unknown"),
        },

        # Historical context
        "historical_context": {
            "biblical_eras": BIBLICAL_ERAS.get(book_name, []),
            "era_descriptions": [
                {era: ERA_DESCRIPTIONS[era]}
                for era in BIBLICAL_ERAS.get(book_name, [])
                if era in ERA_DESCRIPTIONS
            ],
        },

        # Theological themes
        "theological_themes": THEOLOGICAL_THEMES.get(book_name, []),
    }

    # Add audience if available
    if book_name in BOOK_AUDIENCES:
        metadata["literary_analysis"]["audience"] = BOOK_AUDIENCES[book_name]

    # Extract named entities from content
    entities = extract_named_entities(content)
    if any(entities.values()):
        metadata["entities"] = entities

    return metadata
