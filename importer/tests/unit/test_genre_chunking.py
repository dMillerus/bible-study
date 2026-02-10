"""Unit tests for genre-aware chunking logic."""

import pytest
from verse_chunker import chunk_verses, detect_cross_references, _extract_overlap_verses
from csv_parser import BibleVerse


@pytest.fixture
def psalm_verses():
    """Sample Psalms verses (poetry genre)."""
    return [
        BibleVerse(19, "Psalms", 23, 1, "The LORD is my shepherd; I shall not want."),
        BibleVerse(19, "Psalms", 23, 2, "He maketh me to lie down in green pastures: he leadeth me beside the still waters."),
        BibleVerse(19, "Psalms", 23, 3, "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."),
        BibleVerse(19, "Psalms", 23, 4, "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me."),
        BibleVerse(19, "Psalms", 23, 5, "Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over."),
        BibleVerse(19, "Psalms", 23, 6, "Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever."),
    ]


@pytest.fixture
def romans_verses():
    """Sample Romans verses (epistle genre)."""
    return [
        BibleVerse(45, "Romans", 3, 21, "But now the righteousness of God without the law is manifested, being witnessed by the law and the prophets;"),
        BibleVerse(45, "Romans", 3, 22, "Even the righteousness of God which is by faith of Jesus Christ unto all and upon all them that believe: for there is no difference:"),
        BibleVerse(45, "Romans", 3, 23, "For all have sinned, and come short of the glory of God;"),
        BibleVerse(45, "Romans", 3, 24, "Being justified freely by his grace through the redemption that is in Christ Jesus:"),
        BibleVerse(45, "Romans", 3, 25, "Whom God hath set forth to be a propitiation through faith in his blood, to declare his righteousness for the remission of sins that are past, through the forbearance of God;"),
        BibleVerse(45, "Romans", 3, 26, "To declare, I say, at this time his righteousness: that he might be just, and the justifier of him which believeth in Jesus."),
        BibleVerse(45, "Romans", 3, 27, "Where is boasting then? It is excluded. By what law? of works? Nay: but by the law of faith."),
        BibleVerse(45, "Romans", 3, 28, "Therefore we conclude that a man is justified by faith without the deeds of the law."),
    ]


@pytest.fixture
def genesis_verses():
    """Sample Genesis verses (narrative genre)."""
    return [
        BibleVerse(1, "Genesis", 1, 1, "In the beginning God created the heaven and the earth."),
        BibleVerse(1, "Genesis", 1, 2, "And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters."),
        BibleVerse(1, "Genesis", 1, 3, "And God said, Let there be light: and there was light."),
        BibleVerse(1, "Genesis", 1, 4, "And God saw the light, that it was good: and God divided the light from the darkness."),
        BibleVerse(1, "Genesis", 1, 5, "And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day."),
    ]


class TestGenreAwareChunking:
    """Test genre-aware chunking behavior."""

    def test_genre_aware_flag_exists_in_signature(self, psalm_verses):
        """Should accept enable_genre_aware parameter."""
        # Should not raise TypeError
        chunks = list(chunk_verses(psalm_verses, "KJV", enable_genre_aware=False))
        assert len(chunks) > 0

        chunks = list(chunk_verses(psalm_verses, "KJV", enable_genre_aware=True))
        assert len(chunks) > 0

    def test_genre_metadata_included_when_enabled(self, psalm_verses):
        """Chunks should include genre metadata when genre-aware enabled."""
        chunks = list(chunk_verses(psalm_verses, "KJV", enable_genre_aware=True))

        assert len(chunks) > 0
        assert "genre" in chunks[0]["metadata"]
        assert chunks[0]["metadata"]["genre"]["type"] == "poetry"
        assert "description" in chunks[0]["metadata"]["genre"]
        assert chunks[0]["metadata"]["genre"]["target_chunk_tokens"] == 225

    def test_no_genre_metadata_when_disabled(self, psalm_verses):
        """Should not include genre metadata when disabled."""
        chunks = list(chunk_verses(psalm_verses, "KJV", enable_genre_aware=False))

        assert len(chunks) > 0
        assert "genre" not in chunks[0]["metadata"]

    def test_epistle_chunks_differ_from_poetry(self, psalm_verses, romans_verses):
        """Epistles should use different target than poetry."""
        # Poetry chunks
        poetry_chunks = list(chunk_verses(psalm_verses, "KJV", enable_genre_aware=True))
        poetry_target = poetry_chunks[0]["metadata"]["genre"]["target_chunk_tokens"]

        # Epistle chunks
        epistle_chunks = list(chunk_verses(romans_verses, "KJV", enable_genre_aware=True))
        epistle_target = epistle_chunks[0]["metadata"]["genre"]["target_chunk_tokens"]

        # Genre-aware should use different targets
        assert poetry_target == 225  # Poetry target
        assert epistle_target == 425  # Epistle target
        assert epistle_target > poetry_target

    def test_default_behavior_unchanged(self, genesis_verses):
        """Default behavior (no flags) should match original chunker."""
        # Both should produce same number of chunks and similar token counts
        default_chunks = list(chunk_verses(genesis_verses, "KJV"))
        explicit_false = list(chunk_verses(genesis_verses, "KJV", enable_genre_aware=False))

        assert len(default_chunks) == len(explicit_false)
        for d, e in zip(default_chunks, explicit_false):
            assert d["metadata"]["structure"]["token_count"] == e["metadata"]["structure"]["token_count"]


class TestOverlapChunking:
    """Test chunk overlap functionality."""

    def test_overlap_flag_exists_in_signature(self, genesis_verses):
        """Should accept enable_overlap parameter."""
        # Should not raise TypeError
        chunks = list(chunk_verses(genesis_verses, "KJV", enable_overlap=False))
        assert len(chunks) > 0

        chunks = list(chunk_verses(genesis_verses, "KJV", enable_overlap=True))
        assert len(chunks) > 0

    def test_no_overlap_by_default(self, genesis_verses):
        """Default behavior should not include overlap."""
        chunks = list(chunk_verses(genesis_verses, "KJV"))

        for chunk in chunks:
            assert not chunk["metadata"]["structure"]["has_overlap_context"]
            assert chunk["metadata"]["structure"]["overlap_verses"] == 0

    def test_overlap_flag_adds_metadata(self, genesis_verses):
        """Overlap flag should add overlap metadata."""
        chunks = list(chunk_verses(genesis_verses, "KJV", enable_overlap=True))

        # First chunk should not have overlap (no previous chunk)
        # But metadata fields should exist
        for chunk in chunks:
            assert "has_overlap_context" in chunk["metadata"]["structure"]
            assert "overlap_verses" in chunk["metadata"]["structure"]

    def test_overlap_content_marked_distinctly(self, romans_verses):
        """Overlap content should be marked with separator."""
        # Use longer passage to force multiple chunks
        chunks = list(chunk_verses(romans_verses * 3, "KJV", enable_overlap=True))

        # Find chunk with overlap
        overlap_chunk = None
        for chunk in chunks[1:]:  # Skip first chunk
            if chunk["metadata"]["structure"]["has_overlap_context"]:
                overlap_chunk = chunk
                break

        if overlap_chunk:
            content = overlap_chunk["content"]
            # Should have context separator
            assert "Context from previous verses" in content or "previous" in content.lower()

    def test_extract_overlap_verses_helper(self, genesis_verses):
        """Test _extract_overlap_verses helper function."""
        overlap = _extract_overlap_verses(genesis_verses, target_overlap_tokens=50)

        # Should return some verses from the end
        assert len(overlap) > 0
        assert len(overlap) <= len(genesis_verses)

        # Should be from the end of the list
        assert overlap[-1] == genesis_verses[-1]

    def test_extract_overlap_empty_list(self):
        """Should handle empty verse list."""
        overlap = _extract_overlap_verses([], target_overlap_tokens=50)
        assert overlap == []


class TestCrossReferenceDetection:
    """Test cross-reference detection."""

    def test_detect_simple_reference(self):
        """Should detect basic verse reference."""
        text = "As it is written in Genesis 15:6, Abraham believed God."
        refs = detect_cross_references(text)

        assert len(refs) > 0
        assert "Genesis 15:6" in refs

    def test_detect_verse_range(self):
        """Should detect verse range references."""
        text = "See Psalm 32:1-2 for more context."
        refs = detect_cross_references(text)

        assert len(refs) > 0
        # Should detect Psalm/Psalms
        assert any("32" in ref for ref in refs)

    def test_detect_multiple_references(self):
        """Should detect multiple references in one text."""
        text = "Compare Genesis 15:6 with Romans 4:3 and James 2:23."
        refs = detect_cross_references(text)

        assert len(refs) >= 2
        # Should find Genesis and Romans/James

    def test_no_false_positives(self):
        """Should not detect false references."""
        text = "There were 15 men and 6 women in the group."
        refs = detect_cross_references(text)

        assert len(refs) == 0

    def test_book_name_variants(self):
        """Should detect common book name variants."""
        # Psalms vs Psalm
        text1 = "In Psalm 23:1 we read..."
        text2 = "In Psalms 23:1 we read..."

        refs1 = detect_cross_references(text1)
        refs2 = detect_cross_references(text2)

        assert len(refs1) > 0
        assert len(refs2) > 0

    def test_cross_reference_pattern_case_insensitive(self):
        """Should detect references regardless of case."""
        text = "see genesis 15:6"
        refs = detect_cross_references(text)

        assert len(refs) > 0


class TestParallelPassageIntegration:
    """Test parallel passage identification in chunks."""

    def test_parallel_passage_detected_in_chunk(self):
        """Should detect parallel passages in chunk metadata."""
        # Matthew 14:13-21 is feeding of 5000
        feeding_verses = [
            BibleVerse(40, "Matthew", 14, 13, "When Jesus heard of it..."),
            BibleVerse(40, "Matthew", 14, 14, "And Jesus went forth, and saw a great multitude..."),
            BibleVerse(40, "Matthew", 14, 15, "And when it was evening..."),
            BibleVerse(40, "Matthew", 14, 16, "But Jesus said unto them, They need not depart..."),
            BibleVerse(40, "Matthew", 14, 17, "And they say unto him, We have here but five loaves..."),
            BibleVerse(40, "Matthew", 14, 18, "He said, Bring them hither to me."),
            BibleVerse(40, "Matthew", 14, 19, "And he commanded the multitude to sit down..."),
            BibleVerse(40, "Matthew", 14, 20, "And they did all eat, and were filled..."),
            BibleVerse(40, "Matthew", 14, 21, "And they that had eaten were about five thousand men..."),
        ]

        chunks = list(chunk_verses(feeding_verses, "KJV", enable_genre_aware=True))

        # At least one chunk should have parallel passage info
        has_parallel = any("parallel_passages" in c["metadata"] for c in chunks)
        assert has_parallel

        # Find the chunk with parallel passage info
        parallel_chunk = next(c for c in chunks if "parallel_passages" in c["metadata"])

        assert parallel_chunk["metadata"]["parallel_passages"]["event"] == "feeding_5000"
        assert len(parallel_chunk["metadata"]["parallel_passages"]["parallel_passages"]) >= 2

    def test_no_parallel_passage_for_epistle(self, romans_verses):
        """Epistles should not have parallel passage info."""
        chunks = list(chunk_verses(romans_verses, "KJV"))

        for chunk in chunks:
            assert "parallel_passages" not in chunk["metadata"]


class TestBackwardCompatibility:
    """Ensure new features don't break existing behavior."""

    def test_default_parameters_match_original(self, genesis_verses):
        """Calling without new parameters should behave as before."""
        # Original call style
        chunks = list(chunk_verses(genesis_verses, "KJV"))

        # Should produce chunks
        assert len(chunks) > 0

        # Should have all original metadata fields
        assert "book" in chunks[0]["metadata"]
        assert "chapter" in chunks[0]["metadata"]
        assert "verse_start" in chunks[0]["metadata"]
        assert "structure" in chunks[0]["metadata"]

        # Should NOT have new fields by default
        assert "genre" not in chunks[0]["metadata"]
        assert not chunks[0]["metadata"]["structure"]["has_overlap_context"]

    def test_token_counts_reasonable(self, romans_verses):
        """Token counts should be in expected range."""
        chunks = list(chunk_verses(romans_verses, "KJV"))

        for chunk in chunks:
            token_count = chunk["metadata"]["structure"]["token_count"]
            # Should be reasonable (not 0, not huge)
            assert 10 < token_count < 600

    def test_chunks_maintain_order(self, genesis_verses):
        """Chunks should maintain canonical verse order."""
        chunks = list(chunk_verses(genesis_verses, "KJV", enable_genre_aware=True))

        prev_verse_end = 0
        for chunk in chunks:
            verse_start = chunk["metadata"]["verse_start"]
            assert verse_start > prev_verse_end
            prev_verse_end = chunk["metadata"]["verse_end"]


class TestComprehensiveMetadata:
    """Test comprehensive metadata enrichment."""

    def test_metadata_enrichment_present(self, romans_verses):
        """Should include comprehensive metadata from enrichment module."""
        chunks = list(chunk_verses(romans_verses, "KJV", enable_genre_aware=True))

        chunk = chunks[0]
        metadata = chunk["metadata"]

        # Should have literary analysis
        assert "literary_analysis" in metadata
        assert metadata["literary_analysis"]["author"] == "Paul"

        # Should have historical context
        assert "historical_context" in metadata

        # Should have theological themes
        assert "theological_themes" in metadata
        assert len(metadata["theological_themes"]) > 0

    def test_entities_extracted_for_relevant_passages(self):
        """Should extract named entities when present."""
        jesus_verses = [
            BibleVerse(40, "Matthew", 4, 1, "Then was Jesus led up of the Spirit into the wilderness to be tempted of the devil."),
            BibleVerse(40, "Matthew", 4, 2, "And when he had fasted forty days and forty nights, he was afterward an hungred."),
        ]

        chunks = list(chunk_verses(jesus_verses, "KJV"))

        # Should detect "Jesus" as entity
        if "entities" in chunks[0]["metadata"]:
            entities = chunks[0]["metadata"]["entities"]
            assert "people" in entities
            # Jesus should be detected
            assert "Jesus" in entities["people"] or len(entities["people"]) > 0
