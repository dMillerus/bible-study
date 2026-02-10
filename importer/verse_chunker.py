"""Adaptive verse chunking for optimal LLM consumption."""

import re
import tiktoken
from typing import Generator, List, Dict, Any, Optional

from csv_parser import BibleVerse, group_by_chapter, get_book_genre, get_genre_params, identify_parallel_passages
from config import settings


# Initialize tiktoken encoder (cl100k_base is used by GPT-4 and compatible models)
encoder = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    return len(encoder.encode(text))


# Regex pattern for verse references
VERSE_REFERENCE_PATTERN = re.compile(
    r'\b(' + '|'.join([
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "Samuel", "Kings", "Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms?", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
        "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi",
        "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
        "Corinthians", "Galatians", "Ephesians", "Philippians",
        "Colossians", "Thessalonians", "Timothy", "Titus", "Philemon",
        "Hebrews", "James", "Peter", "Jude", "Revelation"
    ]) + r')\s+(\d+):(\d+)(?:-(\d+))?',
    re.IGNORECASE
)


def detect_cross_references(text: str) -> List[str]:
    """
    Extract verse references mentioned in text.

    Args:
        text: Verse content to scan

    Returns:
        List of referenced verses (e.g., ["Genesis 15:6", "Psalm 32:1"])
    """
    matches = VERSE_REFERENCE_PATTERN.findall(text)
    references = []

    for match in matches:
        book, chapter, verse_start, verse_end = match
        if verse_end:
            ref = f"{book} {chapter}:{verse_start}-{verse_end}"
        else:
            ref = f"{book} {chapter}:{verse_start}"
        references.append(ref)

    return references


def chunk_verses(
    verses: List[BibleVerse],
    translation: str,
    enable_genre_aware: bool = False,
    enable_overlap: bool = False,
    overlap_tokens: int = 50,
) -> Generator[Dict[str, Any], None, None]:
    """
    Group verses into optimal chunks for LLM consumption.

    Strategy:
    - Process chapter-by-chapter (never span chapters)
    - Use genre-specific target tokens if enable_genre_aware=True
    - Add overlap between chunks if enable_overlap=True
    - Handle long verses (>max_tokens) as standalone chunks
    - Merge small trailing chunks with previous if possible

    Args:
        verses: List of verses in canonical order
        translation: Translation identifier (e.g., "KJV")
        enable_genre_aware: Use genre-specific chunk sizes (default: False)
        enable_overlap: Add token overlap between chunks (default: False)
        overlap_tokens: Number of tokens to overlap (default: 50)

    Yields:
        Dict representations of chunks ready for Prism import
    """
    previous_chunk_verses: Optional[List[BibleVerse]] = None

    for chapter_verses in group_by_chapter(verses):
        # Determine target tokens for this chapter
        target_tokens = settings.target_chunk_tokens
        genre = None

        if enable_genre_aware and chapter_verses:
            genre = get_book_genre(chapter_verses[0].book_name)
            genre_params = get_genre_params(genre)
            target_tokens = genre_params["target_tokens"]

        for chunk in _chunk_chapter(
            chapter_verses,
            translation,
            target_tokens=target_tokens,
            genre=genre,
            enable_overlap=enable_overlap,
            overlap_tokens=overlap_tokens,
            previous_chunk_verses=previous_chunk_verses,
        ):
            yield chunk
            # Update previous chunk for next iteration
            if enable_overlap:
                previous_chunk_verses = chapter_verses  # Will be sliced in _extract_overlap_verses


def _chunk_chapter(
    verses: List[BibleVerse],
    translation: str,
    target_tokens: int = None,
    genre: str = None,
    enable_overlap: bool = False,
    overlap_tokens: int = 50,
    previous_chunk_verses: Optional[List[BibleVerse]] = None,
) -> Generator[Dict[str, Any], None, None]:
    """
    Chunk a single chapter using token-aware grouping.

    Args:
        verses: All verses from one chapter
        translation: Translation identifier
        target_tokens: Override for genre-specific targets
        genre: Literary genre (for metadata)
        enable_overlap: Add overlap from previous chunk
        overlap_tokens: Number of tokens to overlap
        previous_chunk_verses: Verses from previous chunk (for overlap)

    Yields:
        Chunk documents ready for Prism
    """
    if not verses:
        return

    if target_tokens is None:
        target_tokens = settings.target_chunk_tokens

    current_chunk: List[BibleVerse] = []
    current_tokens = 0
    overlap_context: List[BibleVerse] = []

    # Handle overlap from previous chunk (only for first chunk in chapter)
    if enable_overlap and previous_chunk_verses:
        overlap_context = _extract_overlap_verses(
            previous_chunk_verses, overlap_tokens
        )

    for i, verse in enumerate(verses):
        verse_tokens = count_tokens(verse.text)

        # Case 1: Single verse exceeds max_tokens - make it standalone
        if verse_tokens > settings.max_chunk_tokens:
            # First, flush current chunk if it exists
            if current_chunk:
                yield _create_chunk_document(
                    current_chunk,
                    translation,
                    genre=genre,
                    overlap_context=overlap_context,
                )
                overlap_context = _extract_overlap_verses(
                    current_chunk, overlap_tokens
                ) if enable_overlap else []
                current_chunk = []
                current_tokens = 0

            # Emit oversized verse as standalone chunk
            yield _create_chunk_document(
                [verse],
                translation,
                genre=genre,
                overlap_context=overlap_context,
            )
            overlap_context = [verse] if enable_overlap else []
            continue

        # Case 2: Adding this verse would exceed target - decide whether to flush
        if current_tokens + verse_tokens > target_tokens:
            # Only flush if we're near or above target
            # This prevents creating tiny chunks when we're close to target
            if current_tokens >= target_tokens * 0.8:  # 80% threshold
                yield _create_chunk_document(
                    current_chunk,
                    translation,
                    genre=genre,
                    overlap_context=overlap_context,
                )
                overlap_context = _extract_overlap_verses(
                    current_chunk, overlap_tokens
                ) if enable_overlap else []
                current_chunk = [verse]
                current_tokens = verse_tokens
            else:
                # We're below 80% of target, keep accumulating
                current_chunk.append(verse)
                current_tokens += verse_tokens
        else:
            # Case 3: Normal accumulation
            current_chunk.append(verse)
            current_tokens += verse_tokens

    # Flush final chunk
    if current_chunk:
        yield _create_chunk_document(
            current_chunk,
            translation,
            genre=genre,
            overlap_context=overlap_context,
        )


def _extract_overlap_verses(
    verses: List[BibleVerse],
    target_overlap_tokens: int,
) -> List[BibleVerse]:
    """
    Extract verses from end of chunk for overlap context.

    Args:
        verses: Verses from previous chunk
        target_overlap_tokens: Target number of tokens to overlap

    Returns:
        List of verses totaling ~target_overlap_tokens from end of chunk
    """
    if not verses:
        return []

    overlap_verses = []
    overlap_tokens = 0

    # Work backwards from end of chunk
    for verse in reversed(verses):
        verse_tokens = count_tokens(verse.text)
        if overlap_tokens + verse_tokens > target_overlap_tokens * 1.5:
            break
        overlap_verses.insert(0, verse)
        overlap_tokens += verse_tokens

    return overlap_verses


def _create_chunk_document(
    verses: List[BibleVerse],
    translation: str,
    genre: str = None,
    overlap_context: List[BibleVerse] = None,
) -> Dict[str, Any]:
    """
    Create a Prism document from a verse group.

    Args:
        verses: One or more consecutive verses
        translation: Translation identifier
        genre: Literary genre (for metadata)
        overlap_context: Verses from previous chunk (for context)

    Returns:
        Dict ready for Prism corpus import API
    """
    if not verses:
        raise ValueError("Cannot create chunk from empty verse list")

    first_verse = verses[0]
    last_verse = verses[-1]

    # Build verse range (e.g., "1-5" or just "1" for single verse)
    if len(verses) == 1:
        verse_range = str(first_verse.verse)
        title = f"{first_verse.book_name} {first_verse.chapter}:{first_verse.verse} ({translation})"
    else:
        verse_range = f"{first_verse.verse}-{last_verse.verse}"
        title = (
            f"{first_verse.book_name} {first_verse.chapter}:{verse_range} ({translation})"
        )

    # Combine verse texts with verse numbers
    content_lines = []

    # Add overlap context if present (marked distinctly)
    if overlap_context:
        content_lines.append("--- Context from previous verses ---")
        for verse in overlap_context:
            content_lines.append(f"{verse.verse} {verse.text}")
        content_lines.append("--- Current passage ---")

    for verse in verses:
        content_lines.append(f"{verse.verse} {verse.text}")

    content = "\n".join(content_lines)

    # Calculate token count for verification
    token_count = count_tokens(content)

    # Build hierarchical path for navigation
    path = (
        f"{translation} > {first_verse.book_name} > "
        f"Chapter {first_verse.chapter} > Verses {verse_range}"
    )

    # Detect cross-references in content
    cross_refs = detect_cross_references(content)

    # Check for parallel passages
    parallel_info = identify_parallel_passages(
        first_verse.book_name,
        first_verse.chapter,
        first_verse.verse,
        last_verse.verse,
    )

    # Get comprehensive metadata if available
    try:
        from metadata_enrichment import get_comprehensive_metadata
        comprehensive_meta = get_comprehensive_metadata(
            first_verse.book_name,
            first_verse.chapter,
            first_verse.verse,
            last_verse.verse,
            content,
            genre,
        )
    except ImportError:
        comprehensive_meta = {}

    # Build base metadata structure
    metadata = {
        "book": first_verse.book_name,
        "book_id": first_verse.book_id,
        "chapter": first_verse.chapter,
        "verse_start": first_verse.verse,
        "verse_end": last_verse.verse,
        "testament": first_verse.testament,
        "translation": translation,
        "language": "en",  # Translation language (content language)

        "structure": {
            "path": path,
            "book_number": first_verse.book_id,
            "total_verses": len(verses),
            "token_count": token_count,
            "has_overlap_context": bool(overlap_context),
            "overlap_verses": len(overlap_context) if overlap_context else 0,
        },

        "source": {
            "type": "corpus",
            "origin": "scrollmapper/bible_databases",
            "url": "https://github.com/scrollmapper/bible_databases",
            "format": "csv",
        },
    }

    # Add genre if provided
    if genre:
        metadata["genre"] = {
            "type": genre,
            "description": get_genre_params(genre)["description"],
            "target_chunk_tokens": get_genre_params(genre)["target_tokens"],
        }

    # Cross-references from text analysis
    if cross_refs:
        metadata["cross_references"] = cross_refs

    # Parallel passages from synoptic gospels
    if parallel_info:
        metadata["parallel_passages"] = parallel_info

    # Comprehensive metadata from enrichment module
    metadata.update(comprehensive_meta)

    return {
        "title": title,
        "content": content,
        "domain": f"bible/{translation.lower()}",
        "metadata": metadata,
    }


def analyze_chunking_quality(verses: List[BibleVerse], translation: str) -> Dict[str, Any]:
    """
    Analyze chunking quality without creating documents.

    Returns statistics about token distribution, chunk counts, etc.

    Args:
        verses: Verses to analyze
        translation: Translation identifier

    Returns:
        Dict with quality metrics
    """
    chunks = list(chunk_verses(verses, translation))

    token_counts = [chunk["metadata"]["structure"]["token_count"] for chunk in chunks]

    return {
        "total_verses": len(verses),
        "total_chunks": len(chunks),
        "verses_per_chunk_avg": len(verses) / len(chunks) if chunks else 0,
        "token_stats": {
            "min": min(token_counts) if token_counts else 0,
            "max": max(token_counts) if token_counts else 0,
            "avg": sum(token_counts) / len(token_counts) if token_counts else 0,
        },
        "chunks_below_min": sum(1 for t in token_counts if t < settings.min_chunk_tokens),
        "chunks_above_max": sum(1 for t in token_counts if t > settings.max_chunk_tokens),
        "chunks_in_target_range": sum(
            1
            for t in token_counts
            if settings.target_chunk_tokens * 0.8
            <= t
            <= settings.target_chunk_tokens * 1.2
        ),
    }
