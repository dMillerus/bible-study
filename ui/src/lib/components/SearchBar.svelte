<script lang="ts">
	import { searchQuery, searchFilters, isSearching, searchResults, searchError, toggleTranslation, selectedTranslations } from '$lib/stores/search';
	import { searchBible } from '$lib/api/prism';
	import { Search, X, Download } from 'lucide-svelte';
	import type { Translation } from '$lib/types/bible';

	const TRANSLATIONS: { id: Translation; label: string; year: string }[] = [
		{ id: 'kjv', label: 'KJV', year: '1611' },
		{ id: 'asv', label: 'ASV', year: '1901' },
		{ id: 'bbe', label: 'BBE', year: '1965' },
		{ id: 'ylt', label: 'YLT', year: '1862' },
		{ id: 'webster', label: 'Webster', year: '1833' }
	];

	let query = '';
	let debounceTimer: ReturnType<typeof setTimeout>;

	// Subscribe to search query store
	searchQuery.subscribe(q => query = q);

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		query = target.value;
		searchQuery.set(query);

		// Debounce search (wait 500ms after user stops typing)
		clearTimeout(debounceTimer);

		if (query.trim().length > 2) {
			debounceTimer = setTimeout(() => {
				performSearch();
			}, 500);
		} else {
			searchResults.set([]);
		}
	}

	async function performSearch() {
		if (query.trim().length < 3) {
			return;
		}

		isSearching.set(true);
		searchError.set(null);

		try {
			const results = await searchBible(
				query,
				$selectedTranslations,
				$searchFilters.top_k
			);

			searchResults.set(results);
		} catch (error) {
			console.error('Search failed:', error);
			searchError.set('Search failed. Please check that Prism is running.');
		} finally {
			isSearching.set(false);
		}
	}

	function handleSubmit(event: Event) {
		event.preventDefault();
		if (query.trim().length > 2) {
			performSearch();
		}
	}

	function clearSearch() {
		query = '';
		searchQuery.set('');
		searchResults.set([]);
		searchError.set(null);
	}

	function handleTranslationToggle(translation: Translation) {
		toggleTranslation(translation);
	}

	function exportResults() {
		if ($searchResults.length === 0) return;

		const lines = [
			`Search Query: "${$searchQuery}"`,
			`Results: ${$searchResults.length}`,
			`Translations: ${$selectedTranslations.join(', ').toUpperCase()}`,
			`Date: ${new Date().toLocaleDateString()}`,
			'',
			'=' .repeat(80),
			''
		];

		$searchResults.forEach((result, index) => {
			lines.push(`${index + 1}. ${result.verse_ref} (${result.translation.toUpperCase()})`);
			lines.push(`   Similarity: ${(result.similarity * 100).toFixed(0)}%`);
			lines.push(`   ${result.text}`);
			lines.push('');
		});

		lines.push('=' .repeat(80));
		lines.push('');
		lines.push('Source: Prism Religious Studies (Christianity Module)');
		lines.push('Search Engine: Prism (Personal Semantic Data Layer)');
		lines.push('Embedding Model: nomic-embed-text (768 dimensions)');

		const content = lines.join('\n');
		const blob = new Blob([content], { type: 'text/plain' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `search_${$searchQuery.replace(/\s+/g, '_').substring(0, 30)}_${Date.now()}.txt`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}

	function exportAsJSON() {
		if ($searchResults.length === 0) return;

		const data = {
			query: $searchQuery,
			timestamp: new Date().toISOString(),
			translations: $selectedTranslations,
			total_results: $searchResults.length,
			results: $searchResults.map(r => ({
				verse_ref: r.verse_ref,
				book: r.book,
				chapter: r.chapter,
				verse: r.verse,
				translation: r.translation,
				text: r.text,
				similarity: r.similarity
			}))
		};

		const content = JSON.stringify(data, null, 2);
		const blob = new Blob([content], { type: 'application/json' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `search_${$searchQuery.replace(/\s+/g, '_').substring(0, 30)}_${Date.now()}.json`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}

	function exportAsCSV() {
		if ($searchResults.length === 0) return;

		const headers = ['Reference', 'Book', 'Chapter', 'Verse', 'Translation', 'Similarity', 'Text'];
		const rows = $searchResults.map(r => [
			r.verse_ref,
			r.book,
			r.chapter.toString(),
			r.verse.toString(),
			r.translation.toUpperCase(),
			(r.similarity * 100).toFixed(0) + '%',
			`"${r.text.replace(/"/g, '""')}"`  // Escape quotes in CSV
		]);

		const csvContent = [
			headers.join(','),
			...rows.map(row => row.join(','))
		].join('\n');

		const blob = new Blob([csvContent], { type: 'text/csv' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `search_${$searchQuery.replace(/\s+/g, '_').substring(0, 30)}_${Date.now()}.csv`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}
</script>

<div class="search-bar bg-white border-b border-gray-200 p-4">
	<form on:submit={handleSubmit} class="space-y-3">
		<!-- Search input -->
		<div class="relative">
			<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
				<Search class="h-5 w-5 text-gray-400" />
			</div>

			<input
				type="text"
				value={query}
				on:input={handleInput}
				placeholder="Search the Bible (e.g., 'faith hope love', 'shepherd', 'John 3:16')..."
				class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg
					   focus:ring-2 focus:ring-primary-500 focus:border-primary-500
					   text-base placeholder-gray-400"
			/>

			{#if query}
				<button
					type="button"
					on:click={clearSearch}
					class="absolute inset-y-0 right-0 pr-3 flex items-center"
				>
					<X class="h-5 w-5 text-gray-400 hover:text-gray-600" />
				</button>
			{/if}
		</div>

		<!-- Translation filters and export -->
		<div class="flex items-center justify-between gap-2 flex-wrap">
			<div class="flex items-center gap-2 flex-wrap">
				<span class="text-sm font-medium text-gray-700">Translations:</span>

				{#each TRANSLATIONS as translation}
					<button
						type="button"
						on:click={() => handleTranslationToggle(translation.id)}
						class="px-3 py-1 text-sm rounded-md border transition-colors
							   {$selectedTranslations.includes(translation.id)
								? 'bg-primary-100 border-primary-500 text-primary-700'
								: 'bg-gray-50 border-gray-300 text-gray-600 hover:bg-gray-100'}"
					>
						{translation.label}
						<span class="text-xs opacity-70">({translation.year})</span>
					</button>
				{/each}

				<span class="text-xs text-gray-500 ml-2">
					{$selectedTranslations.length} selected
				</span>
			</div>

			<!-- Export dropdown -->
			{#if $searchResults.length > 0}
				<div class="relative group">
					<button
						type="button"
						class="flex items-center gap-1 px-3 py-1.5 bg-primary-100 hover:bg-primary-200 text-primary-800 rounded-md text-sm transition-colors"
					>
						<Download class="h-4 w-4" />
						Export ({$searchResults.length})
					</button>
					<div class="absolute right-0 mt-1 w-40 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
						<button
							type="button"
							on:click={exportResults}
							class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-t-lg"
						>
							Text (.txt)
						</button>
						<button
							type="button"
							on:click={exportAsJSON}
							class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
						>
							JSON (.json)
						</button>
						<button
							type="button"
							on:click={exportAsCSV}
							class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-b-lg"
						>
							CSV (.csv)
						</button>
					</div>
				</div>
			{/if}
		</div>

		<!-- Search status -->
		{#if $isSearching}
			<div class="text-sm text-gray-600 flex items-center gap-2">
				<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
				Searching...
			</div>
		{/if}

		{#if $searchError}
			<div class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">
				{$searchError}
			</div>
		{/if}
	</form>
</div>

<style>
	/* Component-specific styles */
	.search-bar {
		min-height: fit-content;
	}
</style>
