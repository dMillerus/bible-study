/**
 * Geography API Integration
 *
 * Provides access to biblical geography data (1,342 places) via Prism API
 * Data source: OpenBible.info (CC-BY 4.0)
 */

// Get API URL from environment or use default
const PRISM_API_URL = import.meta.env.VITE_PRISM_API_URL || 'http://localhost:8100';

// Simple in-memory cache for places (10 minute TTL)
let placesCache: { data: BiblicalPlace[]; timestamp: number } | null = null;
const CACHE_TTL = 10 * 60 * 1000; // 10 minutes

export interface BiblicalPlace {
	id: string;
	document_id: string;
	name: string;
	latitude: number;
	longitude: number;
	place_type: string;
	confidence_score: number;
	confidence_level: 'high' | 'moderate' | 'low';
	verse_references: string[];
	alternate_names: string[];
	content: string;
}

export interface PlacesResponse {
	places: BiblicalPlace[];
	total: number;
}

export interface SearchPlacesParams {
	query?: string;
	placeType?: string;
	confidenceLevel?: 'high' | 'moderate' | 'low';
	limit?: number;
	offset?: number;
}

/**
 * Fetch all biblical places from Prism
 */
export async function fetchBiblicalPlaces(params: SearchPlacesParams = {}): Promise<PlacesResponse> {
	const { limit = 100, offset = 0, placeType, confidenceLevel } = params;

	// Check cache if no filters applied
	if (!placeType && !confidenceLevel && placesCache && Date.now() - placesCache.timestamp < CACHE_TTL) {
		return {
			places: placesCache.data.slice(offset, offset + limit),
			total: placesCache.data.length
		};
	}

	try {
		const filters: any = {
			'metadata.domain': { $eq: 'geography/biblical' }
		};

		if (placeType) {
			filters['metadata.place_type'] = { $eq: placeType };
		}

		if (confidenceLevel) {
			filters['metadata.confidence_level'] = { $eq: confidenceLevel };
		}

		const response = await fetch(`${PRISM_API_URL}/api/v1/documents`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		});

		if (!response.ok) {
			if (response.status === 404) {
				throw new Error('Geography data not found. Please ensure biblical places have been imported into Prism.');
			} else if (response.status === 503) {
				throw new Error('Prism API is unavailable. Please check that the service is running.');
			} else {
				throw new Error(`Failed to load geography data (HTTP ${response.status}). Check API logs for details.`);
			}
		}

		const data = await response.json();

		// Transform Prism documents to BiblicalPlace format
		const allPlaces: BiblicalPlace[] = data.documents
			.filter((doc: any) => doc.metadata?.domain === 'geography/biblical')
			.map((doc: any) => transformDocumentToPlace(doc));

		// Cache all places if no filters
		if (!placeType && !confidenceLevel) {
			placesCache = { data: allPlaces, timestamp: Date.now() };
		}

		const places = allPlaces.slice(offset, offset + limit);

		return {
			places,
			total: data.total || allPlaces.length
		};
	} catch (error) {
		console.error('Error fetching biblical places:', error);
		if (error instanceof Error) {
			throw error;
		}
		throw new Error('Network error. Please check your connection and try again.');
	}
}

/**
 * Search for places by name using semantic search
 */
export async function searchPlacesByName(query: string, topK: number = 20): Promise<BiblicalPlace[]> {
	try {
		const response = await fetch(`${PRISM_API_URL}/api/v1/search`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				query,
				domain: 'geography/biblical',
				top_k: topK,
				similarity_threshold: 0.5
			}),
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data = await response.json();

		// Transform search results to BiblicalPlace format
		return data.results.map((result: any) => ({
			id: result.document_id,
			document_id: result.document_id,
			name: result.metadata?.name || extractNameFromContent(result.content),
			latitude: result.metadata?.latitude || 0,
			longitude: result.metadata?.longitude || 0,
			place_type: result.metadata?.place_type || 'unknown',
			confidence_score: result.metadata?.confidence || 0,
			confidence_level: getConfidenceLevel(result.metadata?.confidence || 0),
			verse_references: result.metadata?.verse_references || [],
			alternate_names: result.metadata?.alternate_names || [],
			content: result.content,
		}));
	} catch (error) {
		console.error('Error searching places:', error);
		throw error;
	}
}

/**
 * Get detailed information about a specific place
 */
export async function getPlaceDetails(documentId: string): Promise<BiblicalPlace | null> {
	try {
		const response = await fetch(`${PRISM_API_URL}/api/v1/documents/${documentId}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		});

		if (!response.ok) {
			if (response.status === 404) {
				return null;
			}
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const doc = await response.json();
		return transformDocumentToPlace(doc);
	} catch (error) {
		console.error('Error fetching place details:', error);
		throw error;
	}
}

/**
 * Get places by type (settlement, mountain, river, etc.)
 */
export async function getPlacesByType(placeType: string, limit: number = 50): Promise<BiblicalPlace[]> {
	return fetchBiblicalPlaces({ placeType, limit }).then(response => response.places);
}

/**
 * Get available place types
 */
export async function getPlaceTypes(): Promise<string[]> {
	// Common place types in biblical geography
	return [
		'settlement',
		'mountain',
		'river',
		'valley',
		'region',
		'body of water',
		'city',
		'town',
		'wilderness',
		'other'
	];
}

// Helper functions

function transformDocumentToPlace(doc: any): BiblicalPlace {
	const metadata = doc.metadata || {};

	return {
		id: doc.id || doc.document_id,
		document_id: doc.document_id || doc.id,
		name: metadata.name || extractNameFromContent(doc.content),
		latitude: parseFloat(metadata.latitude) || 0,
		longitude: parseFloat(metadata.longitude) || 0,
		place_type: metadata.place_type || 'unknown',
		confidence_score: parseFloat(metadata.confidence) || 0,
		confidence_level: getConfidenceLevel(parseFloat(metadata.confidence) || 0),
		verse_references: Array.isArray(metadata.verse_references)
			? metadata.verse_references
			: (metadata.verse_references || '').split(',').filter(Boolean),
		alternate_names: Array.isArray(metadata.alternate_names)
			? metadata.alternate_names
			: (metadata.alternate_names || '').split(',').filter(Boolean),
		content: doc.content || '',
	};
}

function getConfidenceLevel(score: number): 'high' | 'moderate' | 'low' {
	if (score >= 300) return 'high';
	if (score >= 80) return 'moderate';
	return 'low';
}

function extractNameFromContent(content: string): string {
	// Try to extract place name from content (first line or first few words)
	if (!content) return 'Unknown Place';

	const firstLine = content.split('\n')[0];
	const match = firstLine.match(/^([^:]+)/);
	return match ? match[1].trim() : firstLine.substring(0, 50);
}

/**
 * Get color for confidence level (for map markers)
 */
export function getConfidenceColor(level: 'high' | 'moderate' | 'low'): string {
	switch (level) {
		case 'high':
			return '#22c55e'; // Green
		case 'moderate':
			return '#eab308'; // Yellow
		case 'low':
			return '#ef4444'; // Red
		default:
			return '#9ca3af'; // Gray
	}
}
