<script lang="ts">
	import { onMount } from 'svelte';
	import { ChevronLeft, ChevronRight, Loader } from 'lucide-svelte';
	import { getHebrewText, getGreekText, getTestament, OT_BOOKS, NT_BOOKS, type VerseText } from '$lib/api/sword';

	export let initialBook: string = 'Genesis';
	export let initialChapter: number = 1;
	export let initialVerse: number = 1;

	type TabType = 'hebrew' | 'greek';

	let currentTab: TabType = 'hebrew';
	let selectedBook = initialBook;
	let selectedChapter = initialChapter;
	let selectedVerse = initialVerse;

	let verseData: VerseText | null = null;
	let loading = false;
	let error: string | null = null;

	// Book lists based on current tab
	$: availableBooks = currentTab === 'hebrew' ? OT_BOOKS : NT_BOOKS;

	// Auto-switch tab when book changes testament
	$: {
		const testament = getTestament(selectedBook);
		if (testament === 'OT' && currentTab === 'greek') {
			currentTab = 'hebrew';
		} else if (testament === 'NT' && currentTab === 'hebrew') {
			currentTab = 'greek';
		}
	}

	onMount(() => {
		loadVerse();
	});

	async function loadVerse() {
		loading = true;
		error = null;

		try {
			if (currentTab === 'hebrew') {
				verseData = await getHebrewText(selectedBook, selectedChapter, selectedVerse);
			} else {
				verseData = await getGreekText(selectedBook, selectedChapter, selectedVerse);
			}

			if (!verseData) {
				error = 'Verse not found or module not available';
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load verse';
		} finally {
			loading = false;
		}
	}

	function handleTabChange(tab: TabType) {
		currentTab = tab;
		// Switch to appropriate book
		if (tab === 'hebrew' && !OT_BOOKS.includes(selectedBook)) {
			selectedBook = 'Genesis';
			selectedChapter = 1;
			selectedVerse = 1;
		} else if (tab === 'greek' && !NT_BOOKS.includes(selectedBook)) {
			selectedBook = 'John';
			selectedChapter = 1;
			selectedVerse = 1;
		}
		loadVerse();
	}

	function previousVerse() {
		if (selectedVerse > 1) {
			selectedVerse--;
			loadVerse();
		} else if (selectedChapter > 1) {
			selectedChapter--;
			selectedVerse = 1; // Simplified - would need max verse lookup
			loadVerse();
		}
	}

	function nextVerse() {
		selectedVerse++;
		loadVerse();
	}

	// Reload when book/chapter/verse changes
	$: if (selectedBook || selectedChapter || selectedVerse) {
		loadVerse();
	}
</script>

<div class="language-viewer bg-white rounded-lg shadow-lg border border-sand-200 overflow-hidden">
	<!-- Tab Navigation -->
	<div class="flex border-b border-sand-200 bg-sand-50">
		<button
			on:click={() => handleTabChange('hebrew')}
			class="flex-1 px-6 py-3 text-sm font-medium transition-colors relative {currentTab === 'hebrew'
				? 'text-primary-700 bg-white border-b-2 border-primary-600'
				: 'text-gray-600 hover:text-gray-900 hover:bg-sand-100'}"
		>
			<span class="hebrew-text text-lg mr-2">א</span>
			Hebrew (OT)
		</button>
		<button
			on:click={() => handleTabChange('greek')}
			class="flex-1 px-6 py-3 text-sm font-medium transition-colors relative {currentTab === 'greek'
				? 'text-primary-700 bg-white border-b-2 border-primary-600'
				: 'text-gray-600 hover:text-gray-900 hover:bg-sand-100'}"
		>
			<span class="greek-text text-lg mr-2">Α</span>
			Greek (NT)
		</button>
	</div>

	<!-- Selectors -->
	<div class="bg-sand-50 px-6 py-4 border-b border-sand-200">
		<div class="grid grid-cols-3 gap-4">
			<!-- Book Selector -->
			<div>
				<label class="block text-xs font-medium text-gray-700 mb-1">Book</label>
				<select
					bind:value={selectedBook}
					class="w-full px-3 py-2 border border-sand-300 rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
				>
					{#each availableBooks as book}
						<option value={book}>{book}</option>
					{/each}
				</select>
			</div>

			<!-- Chapter Selector -->
			<div>
				<label class="block text-xs font-medium text-gray-700 mb-1">Chapter</label>
				<input
					type="number"
					bind:value={selectedChapter}
					min="1"
					max="150"
					class="w-full px-3 py-2 border border-sand-300 rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
				/>
			</div>

			<!-- Verse Selector -->
			<div>
				<label class="block text-xs font-medium text-gray-700 mb-1">Verse</label>
				<input
					type="number"
					bind:value={selectedVerse}
					min="1"
					max="200"
					class="w-full px-3 py-2 border border-sand-300 rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
				/>
			</div>
		</div>

		<!-- Navigation Buttons -->
		<div class="flex items-center justify-between mt-4">
			<button
				on:click={previousVerse}
				class="flex items-center gap-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
				disabled={selectedChapter === 1 && selectedVerse === 1}
			>
				<ChevronLeft class="h-4 w-4" />
				Previous
			</button>

			<div class="text-sm text-gray-600 font-medium">
				{selectedBook} {selectedChapter}:{selectedVerse}
			</div>

			<button
				on:click={nextVerse}
				class="flex items-center gap-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm transition-colors"
			>
				Next
				<ChevronRight class="h-4 w-4" />
			</button>
		</div>
	</div>

	<!-- Content Area -->
	<div class="p-8 min-h-[400px]">
		{#if loading}
			<div class="flex flex-col items-center justify-center h-64">
				<Loader class="h-12 w-12 text-primary-600 animate-spin mb-4" />
				<p class="text-gray-600">Loading original text...</p>
			</div>
		{:else if error}
			<div class="flex items-center justify-center h-64">
				<div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
					<h3 class="text-lg font-heading font-semibold text-red-900 mb-2">Error</h3>
					<p class="text-sm text-red-700">{error}</p>
				</div>
			</div>
		{:else if verseData}
			<!-- Original Text Display -->
			<div class="space-y-6">
				<!-- Original Language Text -->
				<div class="bg-gradient-to-br from-sand-50 to-primary-50 rounded-lg p-8 border border-sand-200">
					<div class="text-center mb-4">
						<h3 class="text-sm font-medium text-gray-600 mb-2">
							{currentTab === 'hebrew' ? 'Hebrew (WLC 4.20)' : 'Greek (SBLGNT 1.0)'}
						</h3>
					</div>
					<p
						class="{currentTab === 'hebrew' ? 'hebrew-text' : 'greek-text'} text-3xl leading-loose text-center"
						dir={currentTab === 'hebrew' ? 'rtl' : 'ltr'}
					>
						{verseData.original_text}
					</p>
				</div>

				<!-- English Translation for Context -->
				{#if verseData.translation}
					<div class="bg-sand-50 rounded-lg p-6 border border-sand-200">
						<h3 class="text-xs font-medium text-gray-600 mb-2">Translation (for context)</h3>
						<p class="text-gray-800 leading-relaxed">
							{verseData.translation}
						</p>
					</div>
				{/if}

				<!-- Strong's Numbers (if available) -->
				{#if verseData.strongs_numbers && verseData.strongs_numbers.length > 0}
					<div class="bg-indigo-50 rounded-lg p-6 border border-indigo-200">
						<h3 class="text-sm font-heading font-semibold text-indigo-900 mb-3">
							Strong's Numbers
						</h3>
						<div class="flex flex-wrap gap-2">
							{#each verseData.strongs_numbers as strongs}
								<span class="bg-white px-3 py-1 rounded-full text-sm font-mono text-indigo-700 border border-indigo-300">
									{strongs}
								</span>
							{/each}
						</div>
						<p class="text-xs text-gray-600 mt-3">
							Strong's Concordance numbers for lexical study (click to view definitions - coming soon)
						</p>
					</div>
				{/if}

				<!-- Module Attribution -->
				<div class="text-xs text-gray-500 pt-4 border-t border-sand-200">
					<p>
						{currentTab === 'hebrew'
							? 'Hebrew text from Westminster Leningrad Codex (WLC 4.20) via SWORD Project'
							: 'Greek text from SBL Greek New Testament (SBLGNT 1.0) via SWORD Project'}
					</p>
				</div>
			</div>
		{:else}
			<div class="flex items-center justify-center h-64">
				<p class="text-gray-500">Select a verse to view original language text</p>
			</div>
		{/if}
	</div>
</div>

<style>
	/* Hebrew text styling with proper Unicode support */
	:global(.hebrew-text) {
		font-family: 'Noto Serif Hebrew', 'SBL Hebrew', serif;
		direction: rtl;
		unicode-bidi: bidi-override;
	}

	/* Greek text styling */
	:global(.greek-text) {
		font-family: 'Noto Sans', 'SBL Greek', sans-serif;
	}
</style>
