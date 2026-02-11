<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Map, Search, Filter, Loader } from 'lucide-svelte';
	import GeographyMap from '$lib/components/GeographyMap.svelte';
	import PlaceDetail from '$lib/components/PlaceDetail.svelte';
	import {
		fetchBiblicalPlaces,
		searchPlacesByName,
		getPlaceTypes,
		type BiblicalPlace
	} from '$lib/api/geography';
	import { goto } from '$app/navigation';

	let places: BiblicalPlace[] = [];
	let filteredPlaces: BiblicalPlace[] = [];
	let selectedPlace: BiblicalPlace | null = null;
	let loading = true;
	let error: string | null = null;

	// Filters
	let searchQuery = '';
	let selectedPlaceType = 'all';
	let selectedConfidence = 'all';
	let placeTypes: string[] = [];

	onMount(async () => {
		try {
			// Fetch place types
			placeTypes = await getPlaceTypes();

			// Fetch all places
			const response = await fetchBiblicalPlaces({ limit: 2000 });
			places = response.places;
			filteredPlaces = places;

			// Check URL parameters for initial search
			const params = $page.url.searchParams;
			const searchParam = params.get('search');
			if (searchParam) {
				searchQuery = searchParam;
				await handleSearch();
			}

			loading = false;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load geography data';
			loading = false;
		}
	});

	async function handleSearch() {
		if (!searchQuery.trim()) {
			filteredPlaces = places;
			return;
		}

		try {
			loading = true;
			const results = await searchPlacesByName(searchQuery, 50);
			filteredPlaces = results;
			loading = false;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Search failed';
			loading = false;
		}
	}

	function handleFilterChange() {
		let filtered = [...places];

		// Filter by place type
		if (selectedPlaceType !== 'all') {
			filtered = filtered.filter(p => p.place_type === selectedPlaceType);
		}

		// Filter by confidence level
		if (selectedConfidence !== 'all') {
			filtered = filtered.filter(p => p.confidence_level === selectedConfidence);
		}

		filteredPlaces = filtered;
	}

	function handlePlaceSelect(place: BiblicalPlace) {
		selectedPlace = place;
	}

	function handleCloseDetail() {
		selectedPlace = null;
	}

	function handleSearchVerses(reference: string) {
		// Navigate to search page with query
		goto(`/search?q=${encodeURIComponent(reference)}`);
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleSearch();
		}
	}

	// Update filtered places when filters change
	$: if (selectedPlaceType || selectedConfidence) {
		handleFilterChange();
	}
</script>

<svelte:head>
	<title>Biblical Geography - Prism Religious Studies</title>
</svelte:head>

<div class="flex-1 bg-sand-50 flex flex-col overflow-hidden">
	<!-- Header with filters -->
	<div class="bg-white border-b border-sand-200 px-6 py-4">
		<div class="max-w-7xl mx-auto">
			<div class="flex items-center gap-3 mb-4">
				<Map class="h-6 w-6 text-olive-600" />
				<div>
					<h1 class="text-2xl font-heading font-bold text-indigo-900">Biblical Geography</h1>
					<p class="text-sm text-gray-600">Interactive map of {places.length} biblical places</p>
				</div>
			</div>

			<!-- Search and Filters -->
			<div class="grid md:grid-cols-4 gap-4">
				<!-- Search -->
				<div class="md:col-span-2">
					<div class="relative">
						<input
							type="text"
							bind:value={searchQuery}
							on:keypress={handleKeyPress}
							placeholder="Search places (e.g., 'capital city', 'mountain near'...)"
							class="w-full px-4 py-2 pl-10 border border-sand-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
						/>
						<Search class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
						<button
							on:click={handleSearch}
							class="absolute right-2 top-1.5 bg-primary-600 hover:bg-primary-700 text-white px-4 py-1.5 rounded text-sm transition-colors"
						>
							Search
						</button>
					</div>
					<p class="text-xs text-gray-500 mt-1">
						Tip: Use descriptive queries like "capital city" or "mountain near Jerusalem"
					</p>
				</div>

				<!-- Place Type Filter -->
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-1">
						<Filter class="h-4 w-4" />
						Place Type
					</label>
					<select
						bind:value={selectedPlaceType}
						class="w-full px-3 py-2 border border-sand-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
					>
						<option value="all">All Types</option>
						{#each placeTypes as type}
							<option value={type}>{type}</option>
						{/each}
					</select>
				</div>

				<!-- Confidence Filter -->
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-1">
						<Filter class="h-4 w-4" />
						Confidence
					</label>
					<select
						bind:value={selectedConfidence}
						class="w-full px-3 py-2 border border-sand-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
					>
						<option value="all">All Levels</option>
						<option value="high">High (≥300)</option>
						<option value="moderate">Moderate (80-300)</option>
						<option value="low">Low (<80)</option>
					</select>
				</div>
			</div>
		</div>
	</div>

	<!-- Map Container -->
	<div class="flex-1 relative overflow-hidden">
		{#if loading}
			<div class="absolute inset-0 flex flex-col items-center justify-center bg-sand-50 z-10 p-8">
				<Loader class="h-12 w-12 text-primary-600 animate-spin mb-4" />
				<p class="text-gray-600 mb-6">Loading biblical geography data...</p>
				<!-- Skeleton preview -->
				<div class="w-full max-w-4xl bg-white rounded-lg shadow-lg p-6 border border-sand-200">
					<div class="skeleton-loader">
						<div class="h-8 bg-gray-200 rounded w-1/3 mb-4 animate-pulse"></div>
						<div class="h-64 bg-gray-100 rounded mb-4 animate-pulse"></div>
						<div class="grid grid-cols-3 gap-4">
							<div class="h-4 bg-gray-200 rounded animate-pulse"></div>
							<div class="h-4 bg-gray-200 rounded animate-pulse"></div>
							<div class="h-4 bg-gray-200 rounded animate-pulse"></div>
						</div>
					</div>
				</div>
			</div>
		{:else if error}
			<div class="absolute inset-0 flex items-center justify-center bg-sand-50 z-10 p-8">
				<div class="bg-red-50 border-2 border-red-200 rounded-lg p-8 max-w-2xl">
					<div class="flex items-start gap-4">
						<div class="flex-shrink-0">
							<svg class="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
							</svg>
						</div>
						<div class="flex-1">
							<h3 class="text-lg font-heading font-semibold text-red-900 mb-2">Error Loading Geography Data</h3>
							<p class="text-sm text-red-700 mb-4">{error}</p>

							<div class="bg-red-100 rounded p-3 mb-4">
								<p class="text-xs text-red-800 font-medium mb-2">Troubleshooting steps:</p>
								<ol class="text-xs text-red-800 space-y-1 list-decimal list-inside">
									<li>Verify Prism API is running: <code class="bg-white px-1 rounded">docker compose ps prism</code></li>
									<li>Check API health: <code class="bg-white px-1 rounded">curl http://localhost:8100/health</code></li>
									<li>Review logs: <code class="bg-white px-1 rounded">docker compose logs -f prism</code></li>
								</ol>
							</div>

							<div class="flex gap-2">
								<button
									on:click={() => window.location.reload()}
									class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors flex items-center gap-2"
								>
									<RefreshCw class="h-4 w-4" />
									Reload Page
								</button>
								<a
									href="/about"
									class="bg-white hover:bg-gray-50 text-red-700 border border-red-300 px-4 py-2 rounded-lg text-sm transition-colors"
								>
									View Documentation
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		{:else}
			<GeographyMap
				{places: filteredPlaces}
				{selectedPlace}
				onPlaceSelect={handlePlaceSelect}
			/>
		{/if}

		<!-- Place Detail Panel (Overlay) -->
		{#if selectedPlace}
			<div class="absolute top-4 right-4 z-[1001] max-h-[calc(100%-2rem)] overflow-hidden">
				<PlaceDetail
					place={selectedPlace}
					onClose={handleCloseDetail}
					onSearchVerses={handleSearchVerses}
				/>
			</div>
		{/if}
	</div>
</div>
