# Prism Religious Studies - User Guide

**Version**: 1.0 (February 2026)
**Focus**: Christianity Module
**URL**: http://localhost:3003

## Table of Contents

1. [Getting Started](#getting-started)
2. [Semantic Search](#semantic-search)
3. [Biblical Geography](#biblical-geography)
4. [Original Languages](#original-languages)
5. [AI-Powered Analysis](#ai-powered-analysis)
6. [Export & Citation](#export--citation)
7. [Tips for Academic Research](#tips-for-academic-research)

---

## Getting Started

### First Visit

1. Navigate to **http://localhost:3003**
2. You'll see the landing page with four main features:
   - **Semantic Search** - Search across 5 English translations
   - **Biblical Geography** - Explore 1,342 places on an interactive map
   - **Original Languages** - Access Hebrew (WLC) and Greek (SBLGNT) texts
   - **AI Analysis** - Get contextual commentary and cross-references

3. Statistics displayed:
   - 5 Bible translations
   - 1,342 biblical places
   - 18,069 indexed verses
   - 2 original languages (Hebrew + Greek)

### Navigation

The top navigation bar provides access to all modules:
- **Search** - Semantic verse search
- **Geography** - Interactive map
- **Languages** - Hebrew/Greek texts
- **About** - Data sources and methodology

The **[Christianity]** badge indicates this is the Christianity module, with other religious traditions planned for future releases.

---

## Semantic Search

### Basic Search

1. Click **Search** in the top navigation (or use the search bar on the homepage)
2. Enter your query in the search bar:
   - **Word**: "shepherd" (finds all verses mentioning shepherds)
   - **Phrase**: "love your enemies" (semantic matching, not exact)
   - **Reference**: "John 3:16" (finds that specific verse)
3. Select which translations to search (default: all 5)
4. Press **Enter** or click **Search**

### Understanding Results

Each result shows:
- **Verse reference** (e.g., "Psalms 23:1")
- **Translation** (e.g., KJV)
- **Text preview** (first ~150 characters)
- **Similarity score** (0.0-1.0, higher = more relevant)

**Feature Icons**:
- **📍 (MapPin)** - Place mentioned (geography data available)
- **א (Hebrew)** - Old Testament verse (Hebrew text available)
- **Α (Greek)** - New Testament verse (Greek text available)

### Viewing Verse Details

1. Click any verse in the results list
2. The center panel shows selected translations side-by-side (up to 4)
3. The right panel provides AI-generated insights:
   - **Commentary** - Historical context, literary analysis, theological themes
   - **Cross-References** - Related passages with explanations
   - **Translation Insights** - Word choice comparisons and etymology

### Action Buttons

When a verse is selected with geography or language data:
- **View on Map** - Navigate to geography page with place highlighted
- **View in Hebrew/Greek** - Navigate to languages page with verse loaded

---

## Biblical Geography

### Interactive Map

1. Click **Geography** in the top navigation
2. The map loads with 1,342 biblical places
3. Markers are color-coded by confidence:
   - **Green** - High confidence (≥300) - well-established locations
   - **Yellow** - Moderate confidence (80-300) - probable locations
   - **Red** - Low confidence (<80) - uncertain identification

### Exploring Places

**Browse by Map**:
- Click and drag to pan
- Scroll to zoom in/out
- Click any marker to see place details

**Search for Places**:
1. Use the search bar at the top
2. Enter a place name (e.g., "Jerusalem", "Bethlehem")
3. Click **Search** - results appear on the map
4. Note: Descriptive queries work better than specific names (e.g., "capital city David" rather than "Jerusalem")

**Filter Places**:
- **Place Type**: Settlement, mountain, river, valley, region, body of water, wilderness, etc.
- **Confidence Level**: High, Moderate, Low
- Filters can be combined

### Place Details Panel

When you click a marker, the detail panel shows:
- **Name** and **Alternate Names**
- **Coordinates** (latitude/longitude)
- **Place Type** (e.g., settlement, mountain)
- **Confidence Score** and **Level**
- **Verse References** (clickable - first 20 shown)
- **Action Button**: "Search Verses About This Place" (semantic search)

### Data Source

Geography data from **OpenBible.info** (CC-BY 4.0 license)
Citation: OpenBible.info Biblical Places Database (2016)

---

## Original Languages

### Hebrew (Old Testament)

1. Click **Languages** in the top navigation
2. The **Hebrew (א)** tab is selected for Old Testament books
3. Select a book (e.g., Genesis), chapter, and verse using the dropdowns
4. The Hebrew text displays in large, clear Unicode font (Noto Serif Hebrew)
5. Use **Previous Verse** / **Next Verse** buttons to navigate

**Features**:
- Right-to-left (RTL) text rendering
- Strong's numbers displayed when available
- English translation shown below for context

### Greek (New Testament)

1. Switch to the **Greek (Α)** tab for New Testament books
2. Select a book (e.g., John), chapter, and verse
3. The Greek text displays in Noto Sans Greek font
4. Same navigation options as Hebrew

### Interlinear View

The interlinear view provides word-by-word alignment:

1. Toggle to **Interlinear** view
2. For each word, you see four rows:
   ```
   Original Script:   בְּרֵאשִׁית        (Hebrew or Greek)
   Transliteration:   bərēšîṯ          (scholarly standard)
   Gloss:             in-beginning     (English meaning)
   Strong's:          H7225            (lexical reference)
   ```

**Reading Guide**:
- Read columns left-to-right (Hebrew interlinear follows transliteration order)
- **Original Script**: The actual Hebrew/Greek word as it appears in WLC/SBLGNT
- **Transliteration**: Phonetic representation for pronunciation
- **Gloss**: Word-for-word English translation
- **Strong's**: Reference number for concordance and lexicon study

### Data Sources

- **Hebrew**: Westminster Leningrad Codex (WLC 4.20) - public domain
- **Greek**: Society of Biblical Literature Greek New Testament (SBLGNT 1.0) - CC-BY 4.0

---

## AI-Powered Analysis

### Generating Insights

1. Search for a verse (or navigate via geography/languages)
2. Select a verse from results
3. The AI panel (right side on desktop) automatically generates:
   - **Commentary** - Historical and literary context
   - **Cross-References** - Related passages with explanations
   - **Translation Insights** - Analysis of word choice differences

### Understanding AI Output

**Commentary** includes:
- Historical context (era, culture, audience)
- Literary analysis (genre, structure, themes)
- Theological significance
- Archaeological or textual notes

**Cross-References** show:
- Related verses (by theme, quotation, or parallel)
- Explanation of the connection
- Similarity to the selected verse

**Translation Insights** analyze:
- Different word choices across translations
- Etymology and original language nuances
- Textual variants (when applicable)

### AI Model Details

- **Model**: Qwen 2.5 14B (local Ollama)
- **Temperature**: 0.7 (balanced creativity and accuracy)
- **Cache**: 1-hour cache for faster repeated queries
- **Purpose**: Research exploration, not definitive interpretation

**Important Disclaimer**: AI insights are for research guidance. Always consult critical editions and scholarly commentaries for authoritative interpretation.

---

## Export & Citation

### Copying Citations

1. Select a verse in the translation grid
2. Click **Copy Citation** button
3. Format copied: `{Verse Reference} ({TRANSLATION})`
   - Example: "Genesis 1:1 (KJV)"
4. Paste into your research notes or document

### Exporting Search Results

1. After performing a search, click the **Export** button in the search bar
2. Choose format:
   - **Text (.txt)** - Formatted list with headers and attribution
   - **JSON (.json)** - Structured data with metadata
   - **CSV (.csv)** - Spreadsheet-compatible with proper escaping

**Export Contents**:
- Query and timestamp
- Selected translations
- All results with similarity scores
- Verse references and text
- Data source attribution

### Academic Attribution

When citing Prism Religious Studies in academic work:

**Recommended Citation**:
```
Prism Religious Studies, Christianity Module. Semantic search powered by
nomic-embed-text embeddings. Data sources: SWORD Project (Bible texts),
OpenBible.info (geography), Westminster Leningrad Codex, SBLGNT.
Accessed [DATE].
```

**Component Citations**:
- **Bible Texts**: SWORD Project modules (Public Domain)
- **Geography**: OpenBible.info (CC-BY 4.0)
- **Hebrew**: Westminster Leningrad Codex 4.20
- **Greek**: Society of Biblical Literature Greek New Testament 1.0
- **Search**: Prism (PostgreSQL + pgvector + nomic-embed-text)
- **AI**: Ollama (Qwen 2.5 14B)

---

## Tips for Academic Research

### Effective Searching

**Do**:
- Use semantic queries: "passages about divine forgiveness"
- Combine keywords: "parable kingdom heaven"
- Try synonyms if initial results are poor
- Filter by translation for textual comparison

**Don't**:
- Expect exact phrase matching (this is semantic, not keyword search)
- Use overly broad queries: "God" (too generic)
- Rely solely on search without reviewing original context

### Geography Research

**Best Practices**:
- Start with high-confidence places (green markers) for established locations
- Use moderate-confidence (yellow) for probable identifications
- Low-confidence (red) indicates scholarly debate - cross-check sources
- Always cite OpenBible.info when using geographic data
- Consider archaeological updates (data from 2016)

### Original Language Study

**Workflow**:
1. Read English translation for context
2. Switch to Hebrew/Greek tab to see original wording
3. Use interlinear view for word-by-word analysis
4. Note Strong's numbers for lexicon study
5. Compare multiple translations to see interpretation choices
6. Consult academic commentaries for morphology and syntax

**Limitations**:
- Interlinear is simplified (does not show full morphological parsing)
- Glosses are basic translations (not exhaustive semantic range)
- Strong's numbers are starting points, not complete lexical analysis

### AI Analysis

**Use Cases**:
- Initial exploration of unfamiliar passages
- Identifying cross-references for further study
- Understanding historical context quickly
- Discovering literary structures or themes

**Verification**:
- Always cross-check AI suggestions with scholarly sources
- Verify cross-references in original texts
- Consult critical commentaries for interpretation
- Be aware of AI limitations (e.g., no access to latest scholarship)

### Combining Features

**Example Research Workflow**:
1. **Search**: "shepherd imagery Psalms" → Find Psalm 23:1
2. **Original Text**: Switch to Hebrew tab to see "יְהוָה רֹעִי" (YHWH is my shepherd)
3. **Geography**: Click "View on Map" to see locations mentioned in the psalm
4. **AI Analysis**: Review commentary for historical shepherding practices
5. **Cross-References**: Explore Ezekiel 34 (God as shepherd theme)
6. **Export**: Save results as JSON for citation management

---

## Troubleshooting

### Search Returns No Results

- Check that translations are selected (checkboxes above search bar)
- Try broader keywords or synonyms
- Verify Prism API is running (see CLAUDE.md for technical diagnostics)

### Map Not Loading

- Check network connection
- Refresh the page (Ctrl+R or Cmd+R)
- Verify browser supports Leaflet.js (Chrome, Firefox, Safari, Edge all supported)

### Hebrew/Greek Not Displaying

- Ensure proper Unicode fonts are loaded (automatic with Google Fonts)
- Try a different browser if rendering issues persist
- Note: Original texts currently use mock data (SWORD backend integration pending)

### AI Commentary Fails

- Wait a few moments for LLM inference (first load: 3-5 seconds)
- Check that Ollama service is running (technical: see CLAUDE.md)
- If cached results load instantly, new commentary may take longer

---

## Future Enhancements

**Planned Features**:
- Additional religious traditions (Islam, Judaism)
- SWORD backend integration for full original text access
- Advanced word study tools (lexicons, parsing)
- Textual criticism apparatus
- Custom annotation and notes
- Collaborative research workspaces

---

## Support & Documentation

- **User Documentation**: This guide
- **Technical Documentation**: `CLAUDE.md` (developer guide)
- **Data Sources**: See `/about` page for comprehensive attributions
- **Repository**: `/dpool/aiml-stack/bible-study/`

For technical issues or feature requests, consult the developer documentation or main aiml-stack repository.

---

**Last Updated**: February 2026
**Version**: 1.0 (Christianity Module)
**License**: Application code is open source. Data sources have varied licenses (see /about page).
