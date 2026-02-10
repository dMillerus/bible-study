"""Unit tests for genre classification and metadata."""

import pytest
from csv_parser import (
    get_book_genre,
    get_genre_params,
    BOOK_GENRES,
    GENRE_CHUNKING_PARAMS,
    BIBLE_BOOKS,
    identify_parallel_passages,
)
from metadata_enrichment import (
    BOOK_AUTHORS,
    BOOK_DATES,
    BOOK_AUDIENCES,
    BOOK_LANGUAGES,
    BIBLICAL_ERAS,
    THEOLOGICAL_THEMES,
    extract_named_entities,
    get_comprehensive_metadata,
)


class TestGenreClassification:
    """Test genre mapping for all 66 books."""

    def test_all_books_have_genre(self):
        """Every book in canon should have a genre."""
        for book in BIBLE_BOOKS:
            genre = get_book_genre(book)
            assert genre in GENRE_CHUNKING_PARAMS
            assert genre in [
                "poetry", "wisdom", "law", "narrative",
                "gospel", "prophecy", "epistle"
            ]

    def test_poetry_genre_assignments(self):
        """Verify poetry books correctly classified."""
        poetry_books = ["Job", "Psalms", "Song of Solomon", "Lamentations"]
        for book in poetry_books:
            assert get_book_genre(book) == "poetry"

    def test_wisdom_genre_assignments(self):
        """Verify wisdom books correctly classified."""
        wisdom_books = ["Proverbs", "Ecclesiastes"]
        for book in wisdom_books:
            assert get_book_genre(book) == "wisdom"

    def test_law_genre_assignments(self):
        """Verify law books correctly classified."""
        law_books = ["Leviticus", "Numbers", "Deuteronomy"]
        for book in law_books:
            assert get_book_genre(book) == "law"

    def test_epistle_genre_assignments(self):
        """Verify epistle books correctly classified."""
        epistles = [
            "Romans", "I Corinthians", "II Corinthians",
            "Galatians", "Ephesians", "Philippians",
            "Colossians", "I Thessalonians", "II Thessalonians",
            "I Timothy", "II Timothy", "Titus", "Philemon",
            "Hebrews", "James", "I Peter", "II Peter",
            "I John", "II John", "III John", "Jude",
        ]
        for book in epistles:
            assert get_book_genre(book) == "epistle"

    def test_gospel_genre_assignments(self):
        """Verify gospel books correctly classified."""
        gospels = ["Matthew", "Mark", "Luke", "John"]
        for book in gospels:
            assert get_book_genre(book) == "gospel"

    def test_prophecy_genre_assignments(self):
        """Verify prophecy books correctly classified."""
        prophecy_books = [
            "Isaiah", "Jeremiah", "Ezekiel", "Daniel",
            "Hosea", "Joel", "Amos", "Obadiah", "Micah",
            "Nahum", "Habakkuk", "Zephaniah", "Haggai",
            "Zechariah", "Malachi", "Revelation of John",
        ]
        for book in prophecy_books:
            assert get_book_genre(book) == "prophecy"

    def test_narrative_genre_assignments(self):
        """Verify narrative books correctly classified."""
        narrative_books = [
            "Genesis", "Exodus", "Joshua", "Judges", "Ruth",
            "I Samuel", "II Samuel", "I Kings", "II Kings",
            "I Chronicles", "II Chronicles", "Ezra", "Nehemiah",
            "Esther", "Jonah", "Acts",
        ]
        for book in narrative_books:
            assert get_book_genre(book) == "narrative"

    def test_genre_params_structure(self):
        """Genre params should have required fields."""
        for genre, params in GENRE_CHUNKING_PARAMS.items():
            assert "target_tokens" in params
            assert "description" in params
            assert "rationale" in params
            assert isinstance(params["target_tokens"], int)
            assert 200 <= params["target_tokens"] <= 500

    def test_genre_token_targets_are_differentiated(self):
        """Different genres should have different token targets."""
        poetry_target = GENRE_CHUNKING_PARAMS["poetry"]["target_tokens"]
        epistle_target = GENRE_CHUNKING_PARAMS["epistle"]["target_tokens"]
        narrative_target = GENRE_CHUNKING_PARAMS["narrative"]["target_tokens"]

        # Poetry should be smallest
        assert poetry_target < narrative_target
        # Epistle should be largest
        assert epistle_target > narrative_target
        # They should be meaningfully different (not just 1 token apart)
        assert epistle_target - poetry_target >= 150


class TestBookMetadata:
    """Test book metadata enrichment."""

    def test_all_books_have_authors(self):
        """All books should have author metadata."""
        for book in BIBLE_BOOKS:
            assert book in BOOK_AUTHORS
            assert isinstance(BOOK_AUTHORS[book], str)
            assert len(BOOK_AUTHORS[book]) > 0

    def test_all_books_have_dates(self):
        """All books should have approximate dating."""
        for book in BIBLE_BOOKS:
            assert book in BOOK_DATES
            assert isinstance(BOOK_DATES[book], str)
            # Dates should mention BCE or CE
            assert "BCE" in BOOK_DATES[book] or "CE" in BOOK_DATES[book]

    def test_all_books_have_languages(self):
        """All books should have original language metadata."""
        for book in BIBLE_BOOKS:
            assert book in BOOK_LANGUAGES
            language = BOOK_LANGUAGES[book]
            assert language in ["Hebrew", "Greek", "Hebrew/Aramaic"]

    def test_epistle_audience_metadata(self):
        """Epistles should have audience metadata."""
        epistles = ["Romans", "I Corinthians", "Galatians", "Ephesians"]
        for book in epistles:
            assert book in BOOK_AUDIENCES
            assert "Church" in BOOK_AUDIENCES[book] or "Timothy" in BOOK_AUDIENCES[book] or "Titus" in BOOK_AUDIENCES[book]

    def test_all_ot_books_have_eras(self):
        """OT books should have biblical era metadata."""
        ot_books = BIBLE_BOOKS[:39]  # First 39 are OT
        for book in ot_books:
            assert book in BIBLICAL_ERAS
            assert len(BIBLICAL_ERAS[book]) > 0

    def test_all_nt_books_have_eras(self):
        """NT books should have biblical era metadata."""
        nt_books = BIBLE_BOOKS[39:]  # Last 27 are NT
        for book in nt_books:
            assert book in BIBLICAL_ERAS
            assert len(BIBLICAL_ERAS[book]) > 0


class TestParallelPassages:
    """Test parallel passage identification."""

    def test_identifies_feeding_5000(self):
        """Should identify feeding of 5000 across gospels."""
        result = identify_parallel_passages("Matthew", 14, 13, 21)

        assert result is not None
        assert result["event"] == "feeding_5000"
        assert "parallel_passages" in result
        assert any("Mark 6" in p for p in result["parallel_passages"])
        assert any("Luke 9" in p for p in result["parallel_passages"])
        assert any("John 6" in p for p in result["parallel_passages"])

    def test_identifies_crucifixion(self):
        """Should identify crucifixion across all four gospels."""
        result = identify_parallel_passages("Matthew", 27, 32, 56)

        assert result is not None
        assert result["event"] == "crucifixion"
        assert len(result["parallel_passages"]) == 3  # Other 3 gospels

    def test_identifies_beatitudes(self):
        """Should identify beatitudes in Matthew and Luke."""
        result = identify_parallel_passages("Matthew", 5, 3, 12)

        assert result is not None
        assert result["event"] == "beatitudes"
        assert any("Luke 6" in p for p in result["parallel_passages"])

    def test_no_parallel_for_unique_passage(self):
        """Should return None for passages without parallels."""
        result = identify_parallel_passages("Romans", 3, 21, 31)
        assert result is None

        result = identify_parallel_passages("Psalms", 23, 1, 6)
        assert result is None

    def test_parallel_passage_event_descriptions(self):
        """Event descriptions should be human-readable."""
        result = identify_parallel_passages("Mark", 6, 30, 44)

        assert result is not None
        assert "description" in result
        # Should be title case and readable
        assert result["description"] == "Feeding 5000"


class TestNamedEntityExtraction:
    """Test named entity recognition."""

    def test_extract_person_entities(self):
        """Should detect common biblical people."""
        text = "And Jesus said to Peter and John, follow me."
        entities = extract_named_entities(text)

        assert "Jesus" in entities["people"]
        assert "Peter" in entities["people"]
        assert "John" in entities["people"]

    def test_extract_place_entities(self):
        """Should detect common biblical places."""
        text = "They traveled from Jerusalem to Galilee via Samaria."
        entities = extract_named_entities(text)

        assert "Jerusalem" in entities["places"]
        assert "Galilee" in entities["places"]

    def test_no_false_positives(self):
        """Should not detect entities that aren't present."""
        text = "The Lord is my shepherd; I shall not want."
        entities = extract_named_entities(text)

        # "Lord" alone shouldn't match without context
        # Should be empty or very minimal
        assert len(entities["people"]) < 3

    def test_entity_case_insensitive(self):
        """Should detect entities regardless of case."""
        text = "jesus spoke to peter"
        entities = extract_named_entities(text)

        assert "Jesus" in entities["people"]
        assert "Peter" in entities["people"]


class TestComprehensiveMetadata:
    """Test comprehensive metadata generation."""

    def test_comprehensive_metadata_structure(self):
        """Should return well-structured metadata."""
        metadata = get_comprehensive_metadata(
            "Romans", 3, 21, 31, "But now the righteousness of God...", "epistle"
        )

        assert "literary_analysis" in metadata
        assert "historical_context" in metadata
        assert "theological_themes" in metadata

    def test_literary_analysis_complete(self):
        """Literary analysis should have all fields."""
        metadata = get_comprehensive_metadata(
            "Romans", 3, 21, 31, "But now...", "epistle"
        )

        lit = metadata["literary_analysis"]
        assert "author" in lit
        assert lit["author"] == "Paul"
        assert "approximate_date" in lit
        assert "57 CE" in lit["approximate_date"]
        assert "original_language" in lit
        assert lit["original_language"] == "Greek"

    def test_epistle_has_audience(self):
        """Epistles should include audience metadata."""
        metadata = get_comprehensive_metadata(
            "Romans", 1, 1, 7, "Paul, a servant...", "epistle"
        )

        assert "audience" in metadata["literary_analysis"]
        assert "Rome" in metadata["literary_analysis"]["audience"]

    def test_historical_context_has_eras(self):
        """Should include biblical era information."""
        metadata = get_comprehensive_metadata(
            "Exodus", 14, 21, 31, "And Moses stretched out his hand...", "narrative"
        )

        assert "biblical_eras" in metadata["historical_context"]
        assert "exodus" in metadata["historical_context"]["biblical_eras"]

    def test_theological_themes_present(self):
        """Should include theological themes."""
        metadata = get_comprehensive_metadata(
            "Romans", 3, 21, 31, "But now the righteousness...", "epistle"
        )

        assert len(metadata["theological_themes"]) > 0
        # Romans should have justification theme
        assert "justification" in metadata["theological_themes"]
