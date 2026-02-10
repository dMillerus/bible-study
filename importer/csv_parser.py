"""CSV parser for scrollmapper Bible database format."""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, List, Optional, Set, Dict, Any


# Bible book order and testament mapping (standard 66-book canon)
BIBLE_BOOKS = [
    # Old Testament (1-39)
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "I Samuel", "II Samuel",
    "I Kings", "II Kings", "I Chronicles", "II Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    # New Testament (40-66)
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "I Corinthians", "II Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "I Thessalonians", "II Thessalonians",
    "I Timothy", "II Timothy", "Titus", "Philemon",
    "Hebrews", "James", "I Peter", "II Peter",
    "I John", "II John", "III John", "Jude", "Revelation of John",
]

BOOK_TO_ID = {book: idx + 1 for idx, book in enumerate(BIBLE_BOOKS)}


# Genre definitions with optimal chunk parameters
GENRE_CHUNKING_PARAMS = {
    "poetry": {
        "target_tokens": 225,
        "description": "Poetic books with parallelism and imagery",
        "rationale": "Preserves stanza boundaries and poetic structure",
    },
    "wisdom": {
        "target_tokens": 250,
        "description": "Wisdom literature and proverbs",
        "rationale": "Short proverbial sayings, self-contained units",
    },
    "law": {
        "target_tokens": 325,
        "description": "Legal and ceremonial instructions",
        "rationale": "Structured legal code sections",
    },
    "narrative": {
        "target_tokens": 350,
        "description": "Story-driven historical books",
        "rationale": "Sequential events, current default baseline",
    },
    "gospel": {
        "target_tokens": 350,
        "description": "Gospel accounts of Jesus' life",
        "rationale": "Narrative with teaching, similar to historical narrative",
    },
    "prophecy": {
        "target_tokens": 375,
        "description": "Prophetic and apocalyptic literature",
        "rationale": "Dense symbolic imagery and oracles",
    },
    "epistle": {
        "target_tokens": 425,
        "description": "Letters with doctrinal teaching",
        "rationale": "Complex theological arguments span multiple verses",
    },
}

# Book-to-genre mapping (all 66 books)
BOOK_GENRES = {
    # Old Testament - Torah/Law (5 books)
    "Genesis": "narrative",
    "Exodus": "narrative",
    "Leviticus": "law",
    "Numbers": "law",
    "Deuteronomy": "law",

    # Old Testament - Historical (12 books)
    "Joshua": "narrative",
    "Judges": "narrative",
    "Ruth": "narrative",
    "I Samuel": "narrative",
    "II Samuel": "narrative",
    "I Kings": "narrative",
    "II Kings": "narrative",
    "I Chronicles": "narrative",
    "II Chronicles": "narrative",
    "Ezra": "narrative",
    "Nehemiah": "narrative",
    "Esther": "narrative",

    # Old Testament - Poetry (5 books)
    "Job": "poetry",
    "Psalms": "poetry",
    "Proverbs": "wisdom",
    "Ecclesiastes": "wisdom",
    "Song of Solomon": "poetry",

    # Old Testament - Major Prophets (5 books)
    "Isaiah": "prophecy",
    "Jeremiah": "prophecy",
    "Lamentations": "poetry",
    "Ezekiel": "prophecy",
    "Daniel": "prophecy",

    # Old Testament - Minor Prophets (12 books)
    "Hosea": "prophecy",
    "Joel": "prophecy",
    "Amos": "prophecy",
    "Obadiah": "prophecy",
    "Jonah": "narrative",
    "Micah": "prophecy",
    "Nahum": "prophecy",
    "Habakkuk": "prophecy",
    "Zephaniah": "prophecy",
    "Haggai": "prophecy",
    "Zechariah": "prophecy",
    "Malachi": "prophecy",

    # New Testament - Gospels (4 books)
    "Matthew": "gospel",
    "Mark": "gospel",
    "Luke": "gospel",
    "John": "gospel",

    # New Testament - History (1 book)
    "Acts": "narrative",

    # New Testament - Pauline Epistles (13 books)
    "Romans": "epistle",
    "I Corinthians": "epistle",
    "II Corinthians": "epistle",
    "Galatians": "epistle",
    "Ephesians": "epistle",
    "Philippians": "epistle",
    "Colossians": "epistle",
    "I Thessalonians": "epistle",
    "II Thessalonians": "epistle",
    "I Timothy": "epistle",
    "II Timothy": "epistle",
    "Titus": "epistle",
    "Philemon": "epistle",

    # New Testament - General Epistles (8 books)
    "Hebrews": "epistle",
    "James": "epistle",
    "I Peter": "epistle",
    "II Peter": "epistle",
    "I John": "epistle",
    "II John": "epistle",
    "III John": "epistle",
    "Jude": "epistle",

    # New Testament - Apocalyptic (1 book)
    "Revelation of John": "prophecy",
}


def get_testament(book_id: int) -> str:
    """Get testament (OT/NT) from book ID."""
    return "OT" if book_id <= 39 else "NT"


def get_book_genre(book_name: str) -> str:
    """Get literary genre for a book."""
    return BOOK_GENRES.get(book_name, "narrative")


def get_genre_params(genre: str) -> dict:
    """Get chunking parameters for a genre."""
    return GENRE_CHUNKING_PARAMS.get(genre, GENRE_CHUNKING_PARAMS["narrative"])


# Major parallel passages (synoptic gospels and duplicate accounts)
PARALLEL_PASSAGES = {
    "feeding_5000": [
        ("Matthew", 14, 13, 21),
        ("Mark", 6, 30, 44),
        ("Luke", 9, 10, 17),
        ("John", 6, 1, 15),
    ],
    "walking_on_water": [
        ("Matthew", 14, 22, 33),
        ("Mark", 6, 45, 52),
        ("John", 6, 16, 21),
    ],
    "transfiguration": [
        ("Matthew", 17, 1, 13),
        ("Mark", 9, 2, 13),
        ("Luke", 9, 28, 36),
    ],
    "triumphal_entry": [
        ("Matthew", 21, 1, 11),
        ("Mark", 11, 1, 11),
        ("Luke", 19, 28, 44),
        ("John", 12, 12, 19),
    ],
    "cleansing_temple": [
        ("Matthew", 21, 12, 17),
        ("Mark", 11, 15, 19),
        ("Luke", 19, 45, 48),
        ("John", 2, 13, 22),
    ],
    "last_supper": [
        ("Matthew", 26, 17, 30),
        ("Mark", 14, 12, 26),
        ("Luke", 22, 7, 38),
        ("John", 13, 1, 38),
    ],
    "crucifixion": [
        ("Matthew", 27, 32, 56),
        ("Mark", 15, 21, 41),
        ("Luke", 23, 26, 49),
        ("John", 19, 16, 37),
    ],
    "resurrection": [
        ("Matthew", 28, 1, 10),
        ("Mark", 16, 1, 8),
        ("Luke", 24, 1, 12),
        ("John", 20, 1, 10),
    ],
    "great_commission": [
        ("Matthew", 28, 18, 20),
        ("Mark", 16, 15, 18),
        ("Luke", 24, 44, 49),
        ("Acts", 1, 4, 8),
    ],
    "beatitudes": [
        ("Matthew", 5, 3, 12),
        ("Luke", 6, 20, 23),
    ],
    "lords_prayer": [
        ("Matthew", 6, 9, 13),
        ("Luke", 11, 2, 4),
    ],
    "parable_sower": [
        ("Matthew", 13, 1, 23),
        ("Mark", 4, 1, 20),
        ("Luke", 8, 4, 15),
    ],
    "parable_mustard_seed": [
        ("Matthew", 13, 31, 32),
        ("Mark", 4, 30, 32),
        ("Luke", 13, 18, 19),
    ],
    "parable_lost_sheep": [
        ("Matthew", 18, 10, 14),
        ("Luke", 15, 3, 7),
    ],
    "olivet_discourse": [
        ("Matthew", 24, 1, 51),
        ("Mark", 13, 1, 37),
        ("Luke", 21, 5, 36),
    ],
}


def identify_parallel_passages(
    book_name: str,
    chapter: int,
    verse_start: int,
    verse_end: int,
) -> Optional[Dict[str, Any]]:
    """
    Check if chunk is part of a parallel passage.

    Args:
        book_name: Book name
        chapter: Chapter number
        verse_start: Starting verse
        verse_end: Ending verse

    Returns:
        Dict with event name and parallel references, or None
    """
    for event, passages in PARALLEL_PASSAGES.items():
        for psg_book, psg_ch, psg_v_start, psg_v_end in passages:
            # Check if this chunk overlaps with the passage
            if book_name == psg_book and chapter == psg_ch:
                # Simple overlap check
                if not (verse_end < psg_v_start or verse_start > psg_v_end):
                    # Build parallel references
                    parallels = []
                    for pb, pc, pvs, pve in passages:
                        if pb != book_name or pc != chapter:
                            parallels.append(f"{pb} {pc}:{pvs}-{pve}")

                    return {
                        "event": event,
                        "description": event.replace("_", " ").title(),
                        "parallel_passages": parallels,
                    }

    return None


@dataclass
class BibleBook:
    """Metadata for a Bible book."""

    book_id: int
    name: str
    testament: str
    genre: str = "narrative"

    @property
    def genre_params(self) -> dict:
        """Get chunking parameters for this book's genre."""
        return get_genre_params(self.genre)

    @property
    def normalized_name(self) -> str:
        """Get standardized book name for display."""
        return self.name


@dataclass
class BibleVerse:
    """A single Bible verse with metadata."""

    book_id: int
    book_name: str
    chapter: int
    verse: int
    text: str

    @property
    def testament(self) -> str:
        """Get testament for this verse."""
        return get_testament(self.book_id)

    @property
    def reference(self) -> str:
        """Get human-readable reference (e.g., 'Genesis 1:1')."""
        return f"{self.book_name} {self.chapter}:{self.verse}"

    def __lt__(self, other: "BibleVerse") -> bool:
        """Enable sorting by canonical order."""
        return (self.book_id, self.chapter, self.verse) < (
            other.book_id,
            other.chapter,
            other.verse,
        )


def parse_bible_csv(
    verses_path: Path,
    translation: str,
    filter_books: Optional[List[str]] = None,
) -> List[BibleVerse]:
    """
    Parse scrollmapper Bible CSV format.

    Args:
        verses_path: Path to verses CSV file (e.g., KJV.csv)
        translation: Translation identifier (e.g., "KJV")
        filter_books: Optional list of book names to import (for testing)

    Returns:
        List of BibleVerse objects in canonical order

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid or contains unknown books
    """
    if not verses_path.exists():
        raise FileNotFoundError(f"Verses CSV not found: {verses_path}")

    verses: List[BibleVerse] = []
    unknown_books: Set[str] = set()

    with open(verses_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if not all(col in reader.fieldnames for col in ["Book", "Chapter", "Verse", "Text"]):
            raise ValueError(
                f"Invalid CSV format in {verses_path}. "
                "Expected columns: Book, Chapter, Verse, Text"
            )

        for row in reader:
            book_name = row["Book"]

            # Skip books not in filter if provided
            if filter_books and book_name not in filter_books:
                continue

            # Track unknown books
            if book_name not in BOOK_TO_ID:
                unknown_books.add(book_name)
                continue

            verse = BibleVerse(
                book_id=BOOK_TO_ID[book_name],
                book_name=book_name,
                chapter=int(row["Chapter"]),
                verse=int(row["Verse"]),
                text=row["Text"].strip(),
            )
            verses.append(verse)

    if unknown_books:
        raise ValueError(
            f"Unknown books found in {translation} CSV: {sorted(unknown_books)}. "
            "These books are not in the standard 66-book canon."
        )

    if not verses:
        raise ValueError(f"No verses found in {verses_path}")

    # Sort by canonical order
    verses.sort()

    return verses


def get_available_books(verses_path: Path) -> List[str]:
    """Get list of all book names in a verses CSV file."""
    if not verses_path.exists():
        raise FileNotFoundError(f"Verses CSV not found: {verses_path}")

    books: Set[str] = set()
    with open(verses_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.add(row["Book"])

    return sorted(books)


def group_by_chapter(verses: List[BibleVerse]) -> Generator[List[BibleVerse], None, None]:
    """
    Group verses by chapter.

    Yields:
        Lists of verses for each chapter in canonical order
    """
    if not verses:
        return

    current_chapter_verses: List[BibleVerse] = []
    current_book_id = verses[0].book_id
    current_chapter = verses[0].chapter

    for verse in verses:
        # Check if we've moved to a new chapter
        if verse.book_id != current_book_id or verse.chapter != current_chapter:
            if current_chapter_verses:
                yield current_chapter_verses
            current_chapter_verses = []
            current_book_id = verse.book_id
            current_chapter = verse.chapter

        current_chapter_verses.append(verse)

    # Yield final chapter
    if current_chapter_verses:
        yield current_chapter_verses


def validate_verse_integrity(verses: List[BibleVerse]) -> Dict[str, Any]:
    """
    Validate verse data integrity.

    Returns:
        Dict with validation statistics and any issues found
    """
    issues: List[str] = []
    total_verses = len(verses)
    books_found: Set[str] = set()
    chapters_by_book: Dict[str, Set[int]] = {}

    for verse in verses:
        books_found.add(verse.book_name)
        if verse.book_name not in chapters_by_book:
            chapters_by_book[verse.book_name] = set()
        chapters_by_book[verse.book_name].add(verse.chapter)

        # Check for empty text
        if not verse.text or not verse.text.strip():
            issues.append(f"Empty text in {verse.reference}")

    return {
        "total_verses": total_verses,
        "books_found": len(books_found),
        "chapters_found": sum(len(chapters) for chapters in chapters_by_book.values()),
        "books": sorted(books_found),
        "issues": issues,
    }
