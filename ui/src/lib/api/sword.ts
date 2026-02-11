/**
 * SWORD API Integration
 *
 * Provides access to original Hebrew (WLC) and Greek (SBLGNT) Bible texts
 * via SWORD modules through the Python parser backend.
 */

// Note: This assumes a future API endpoint. For now, uses mock data for development.
const USE_MOCK_DATA = true; // Toggle when API endpoint is ready

// Simple cache for verse data (30 minute TTL)
const verseCache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 30 * 60 * 1000; // 30 minutes

export interface VerseText {
	original_text: string;
	language: 'hebrew' | 'greek';
	strongs_numbers?: string[];
	book: string;
	chapter: number;
	verse: number;
	translation?: string; // English translation for context
}

export interface InterlinearWord {
	original: string;
	transliteration: string;
	gloss: string;
	strongs?: string;
	morphology?: string;
}

export interface InterlinearVerse {
	words: InterlinearWord[];
	book: string;
	chapter: number;
	verse: number;
	language: 'hebrew' | 'greek';
}

// Book lists for UI dropdowns
export const OT_BOOKS = [
	"Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
	"Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
	"1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
	"Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
	"Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah",
	"Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
	"Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
	"Zephaniah", "Haggai", "Zechariah", "Malachi"
];

export const NT_BOOKS = [
	"Matthew", "Mark", "Luke", "John", "Acts",
	"Romans", "1 Corinthians", "2 Corinthians", "Galatians",
	"Ephesians", "Philippians", "Colossians",
	"1 Thessalonians", "2 Thessalonians",
	"1 Timothy", "2 Timothy", "Titus", "Philemon",
	"Hebrews", "James", "1 Peter", "2 Peter",
	"1 John", "2 John", "3 John", "Jude", "Revelation"
];

/**
 * Get Hebrew text for an Old Testament verse
 */
export async function getHebrewText(book: string, chapter: number, verse: number): Promise<VerseText | null> {
	// Check cache first
	const cacheKey = `hebrew:${book}:${chapter}:${verse}`;
	const cached = verseCache.get(cacheKey);
	if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
		return cached.data;
	}

	if (USE_MOCK_DATA) {
		const data = getMockHebrewText(book, chapter, verse);
		verseCache.set(cacheKey, { data, timestamp: Date.now() });
		return data;
	}

	try {
		// TODO: Replace with actual API endpoint when backend is ready
		const response = await fetch(`/api/sword/hebrew`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ book, chapter, verse })
		});

		if (!response.ok) return null;
		const data = await response.json();
		verseCache.set(cacheKey, { data, timestamp: Date.now() });
		return data;
	} catch (error) {
		console.error('Error fetching Hebrew text:', error);
		return null;
	}
}

/**
 * Get Greek text for a New Testament verse
 */
export async function getGreekText(book: string, chapter: number, verse: number): Promise<VerseText | null> {
	if (USE_MOCK_DATA) {
		return getMockGreekText(book, chapter, verse);
	}

	try {
		// TODO: Replace with actual API endpoint when backend is ready
		const response = await fetch(`/api/sword/greek`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ book, chapter, verse })
		});

		if (!response.ok) return null;
		return await response.json();
	} catch (error) {
		console.error('Error fetching Greek text:', error);
		return null;
	}
}

/**
 * Get interlinear view (original + transliteration + gloss) for a verse
 */
export async function getInterlinear(book: string, chapter: number, verse: number): Promise<InterlinearVerse | null> {
	if (USE_MOCK_DATA) {
		return getMockInterlinear(book, chapter, verse);
	}

	try {
		// TODO: Replace with actual API endpoint when backend is ready
		const response = await fetch(`/api/sword/interlinear`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ book, chapter, verse })
		});

		if (!response.ok) return null;
		return await response.json();
	} catch (error) {
		console.error('Error fetching interlinear:', error);
		return null;
	}
}

/**
 * Determine if a book is OT or NT
 */
export function getTestament(book: string): 'OT' | 'NT' | null {
	if (OT_BOOKS.includes(book)) return 'OT';
	if (NT_BOOKS.includes(book)) return 'NT';
	return null;
}

/**
 * Get language for a book
 */
export function getLanguage(book: string): 'hebrew' | 'greek' | null {
	const testament = getTestament(book);
	if (testament === 'OT') return 'hebrew';
	if (testament === 'NT') return 'greek';
	return null;
}

// Mock data for development (will be removed when API is ready)

function getMockHebrewText(book: string, chapter: number, verse: number): VerseText {
	const samples: Record<string, string> = {
		"Genesis:1:1": "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
		"Genesis:1:2": "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל־פְּנֵי תְהוֹם וְרוּחַ אֱלֹהִים מְרַחֶפֶת עַל־פְּנֵי הַמָּיִם",
		"Psalms:23:1": "יְהוָה רֹעִי לֹא אֶחְסָר",
		"Psalms:23:2": "בִּנְאוֹת דֶּשֶׁא יַרְבִּיצֵנִי עַל־מֵי מְנֻחוֹת יְנַהֲלֵנִי",
	};

	const key = `${book}:${chapter}:${verse}`;
	const original_text = samples[key] || "בְּרֵאשִׁית בָּרָא אֱלֹהִים";

	return {
		original_text,
		language: 'hebrew',
		book,
		chapter,
		verse,
		translation: "In the beginning God created...",
		strongs_numbers: ["H7225", "H1254", "H430"]
	};
}

function getMockGreekText(book: string, chapter: number, verse: number): VerseText {
	const samples: Record<string, string> = {
		"John:1:1": "Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν καὶ θεὸς ἦν ὁ λόγος",
		"John:1:2": "οὗτος ἦν ἐν ἀρχῇ πρὸς τὸν θεόν",
		"John:3:16": "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον ὥστε τὸν υἱὸν τὸν μονογενῆ ἔδωκεν",
		"Matthew:1:1": "Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυὶδ υἱοῦ Ἀβραάμ",
	};

	const key = `${book}:${chapter}:${verse}`;
	const original_text = samples[key] || "Ἐν ἀρχῇ ἦν ὁ λόγος";

	return {
		original_text,
		language: 'greek',
		book,
		chapter,
		verse,
		translation: "In the beginning was the Word...",
		strongs_numbers: ["G1722", "G746", "G1510", "G3056"]
	};
}

function getMockInterlinear(book: string, chapter: number, verse: number): InterlinearVerse {
	const testament = getTestament(book);

	if (testament === 'OT') {
		// Genesis 1:1 example
		return {
			book,
			chapter,
			verse,
			language: 'hebrew',
			words: [
				{ original: "בְּרֵאשִׁית", transliteration: "bərēšîṯ", gloss: "in-beginning", strongs: "H7225" },
				{ original: "בָּרָא", transliteration: "bārā", gloss: "he-created", strongs: "H1254" },
				{ original: "אֱלֹהִים", transliteration: "ʾĕlōhîm", gloss: "God", strongs: "H430" },
				{ original: "אֵת", transliteration: "ʾēṯ", gloss: "(obj)", strongs: "H853" },
				{ original: "הַשָּׁמַיִם", transliteration: "haš-šāmayim", gloss: "the-heavens", strongs: "H8064" },
				{ original: "וְאֵת", transliteration: "wə-ʾēṯ", gloss: "and-(obj)", strongs: "H853" },
				{ original: "הָאָרֶץ", transliteration: "hā-ʾāreṣ", gloss: "the-earth", strongs: "H776" },
			]
		};
	} else {
		// John 1:1 example
		return {
			book,
			chapter,
			verse,
			language: 'greek',
			words: [
				{ original: "Ἐν", transliteration: "En", gloss: "In", strongs: "G1722" },
				{ original: "ἀρχῇ", transliteration: "archē", gloss: "beginning", strongs: "G746" },
				{ original: "ἦν", transliteration: "ēn", gloss: "was", strongs: "G1510" },
				{ original: "ὁ", transliteration: "ho", gloss: "the", strongs: "G3588" },
				{ original: "λόγος", transliteration: "logos", gloss: "Word", strongs: "G3056" },
				{ original: "καὶ", transliteration: "kai", gloss: "and", strongs: "G2532" },
				{ original: "ὁ", transliteration: "ho", gloss: "the", strongs: "G3588" },
				{ original: "λόγος", transliteration: "logos", gloss: "Word", strongs: "G3056" },
				{ original: "ἦν", transliteration: "ēn", gloss: "was", strongs: "G1510" },
				{ original: "πρὸς", transliteration: "pros", gloss: "with", strongs: "G4314" },
				{ original: "τὸν", transliteration: "ton", gloss: "the", strongs: "G3588" },
				{ original: "θεόν", transliteration: "theon", gloss: "God", strongs: "G2316" },
			]
		};
	}
}
