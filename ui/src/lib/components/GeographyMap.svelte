<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { BiblicalPlace } from '$lib/api/geography';
	import { getConfidenceColor } from '$lib/api/geography';

	// Props
	export let places: BiblicalPlace[] = [];
	export let selectedPlace: BiblicalPlace | null = null;
	export let onPlaceSelect: (place: BiblicalPlace) => void = () => {};

	let mapContainer: HTMLDivElement;
	let map: any;
	let markers: any[] = [];
	let L: any;

	onMount(async () => {
		// Dynamically import Leaflet (client-side only)
		L = await import('leaflet');

		// Import Leaflet CSS
		const link = document.createElement('link');
		link.rel = 'stylesheet';
		link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
		document.head.appendChild(link);

		// Initialize map centered on ancient Near East
		map = L.map(mapContainer, {
			center: [31.7767, 35.2345], // Jerusalem coordinates
			zoom: 7,
			scrollWheelZoom: true,
			zoomControl: true
		});

		// Add CartoDB Positron tiles (clean, minimal design)
		L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
			maxZoom: 19,
			subdomains: 'abcd'
		}).addTo(map);

		// Add markers for places
		renderMarkers();
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});

	function renderMarkers() {
		if (!map || !L) return;

		// Clear existing markers
		markers.forEach(marker => marker.remove());
		markers = [];

		// Add markers for each place
		places.forEach(place => {
			if (!place.latitude || !place.longitude) return;

			const color = getConfidenceColor(place.confidence_level);

			// Create custom icon with confidence-based color
			const icon = L.divIcon({
				className: 'custom-marker',
				html: `
					<div style="
						background-color: ${color};
						width: 12px;
						height: 12px;
						border-radius: 50%;
						border: 2px solid white;
						box-shadow: 0 2px 4px rgba(0,0,0,0.3);
						cursor: pointer;
					"></div>
				`,
				iconSize: [16, 16],
				iconAnchor: [8, 8],
			});

			const marker = L.marker([place.latitude, place.longitude], { icon })
				.addTo(map)
				.bindPopup(`
					<div style="min-width: 200px;">
						<h3 style="font-weight: bold; margin-bottom: 4px; font-size: 14px;">${place.name}</h3>
						<p style="font-size: 12px; color: #666; margin-bottom: 4px;">
							<strong>Type:</strong> ${place.place_type}<br/>
							<strong>Confidence:</strong> ${place.confidence_level} (${place.confidence_score})
						</p>
						<button
							onclick="window.selectPlace('${place.document_id}')"
							style="
								background-color: #E2725B;
								color: white;
								padding: 4px 12px;
								border-radius: 4px;
								border: none;
								cursor: pointer;
								font-size: 12px;
								margin-top: 4px;
							"
						>
							View Details
						</button>
					</div>
				`);

			marker.on('click', () => {
				onPlaceSelect(place);
			});

			markers.push(marker);
		});

		// Fit map to show all markers
		if (markers.length > 0) {
			const group = L.featureGroup(markers);
			map.fitBounds(group.getBounds().pad(0.1));
		}
	}

	// Re-render markers when places change
	$: if (map && places) {
		renderMarkers();
	}

	// Center on selected place
	$: if (map && selectedPlace && selectedPlace.latitude && selectedPlace.longitude) {
		map.setView([selectedPlace.latitude, selectedPlace.longitude], 12);
	}

	// Expose selectPlace function for popup button
	if (typeof window !== 'undefined') {
		(window as any).selectPlace = (documentId: string) => {
			const place = places.find(p => p.document_id === documentId);
			if (place) {
				onPlaceSelect(place);
			}
		};
	}
</script>

<div class="map-wrapper h-full w-full relative">
	<div bind:this={mapContainer} class="h-full w-full rounded-lg shadow-lg"></div>

	<!-- Legend -->
	<div class="absolute bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 z-[1000]">
		<h4 class="text-sm font-semibold text-gray-900 mb-2">Confidence Level</h4>
		<div class="space-y-1 text-xs">
			<div class="flex items-center gap-2">
				<div class="w-3 h-3 rounded-full bg-green-500 border-2 border-white"></div>
				<span class="text-gray-700">High (≥300)</span>
			</div>
			<div class="flex items-center gap-2">
				<div class="w-3 h-3 rounded-full bg-yellow-500 border-2 border-white"></div>
				<span class="text-gray-700">Moderate (80-300)</span>
			</div>
			<div class="flex items-center gap-2">
				<div class="w-3 h-3 rounded-full bg-red-500 border-2 border-white"></div>
				<span class="text-gray-700">Low (&lt;80)</span>
			</div>
		</div>
		<div class="mt-3 pt-3 border-t border-gray-200 text-xs text-gray-500">
			{places.length} places shown
		</div>
	</div>
</div>

<style>
	.map-wrapper :global(.leaflet-container) {
		background: #f5f1e8; /* Sand background */
	}

	.map-wrapper :global(.leaflet-popup-content-wrapper) {
		border-radius: 8px;
	}

	.map-wrapper :global(.leaflet-popup-content) {
		margin: 12px;
	}
</style>
