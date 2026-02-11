<script lang="ts">
	import { onMount } from 'svelte';
	import { ChevronLeft, ChevronRight, Loader, Info } from 'lucide-svelte';
	import { getInterlinear, getTestament, OT_BOOKS, NT_BOOKS, type InterlinearVerse } from '$lib/api/sword';

	export let initialBook: string = 'Genesis';
	export let initialChapter: number = 1;
	export let initialVerse: number = 1;

	let selectedBook = initialBook;
	let selectedChapter = initialChapter;
	let selectedVerse = initialVerse;

	let interlinearData: InterlinearVerse | null = null;
	let loading = false;
	let error: string | null = null;

	// Determine available books based on testament
	$: testament = getTestament(selectedBook);
	$: availableBooks = testament === 'OT' ? OT_BOOKS : NT_BOOKS;

	onMount(() => {
		loadInterlinear();
	});

	async function loadInterlinear() {
		loading = true;
		error = null;

		try {
			interlinearData = await getInterlinear(selectedBook, selectedChapter, selectedVerse);

			if (!interlinearData) {
				error = 'Interlinear data not available for this verse';
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load interlinear';
		} finally {
			loading = false;
		}
	}

	function previousVerse() {
		if (selectedVerse > 1) {
			selectedVerse--;
			loadInterlinear();
		} else if (selectedChapter > 1) {
			selectedChapter--;
			selectedVerse = 1;
			loadInterlinear();
		}
	}

	function nextVerse() {
		selectedVerse++;
		loadInterlinear();
	}

	// Reload when book/chapter/verse changes
	$: if (selectedBook || selectedChapter || selectedVerse) {
		loadInterlinear();
	}
</script>

<div class="interlinear-viewer bg-white rounded-lg shadow-lg border border-sand-200 overflow-hidden">
	<!-- Header -->
	<div class="bg-gradient-to-r from-primary-600 to-olive-600 text-white px-6 py-4">
		<div class="flex items-center justify-between">
			<div>
				<h2 class="text-xl font-heading font-bold">Interlinear View</h2>
				<p class="text-sm text-sand-100">Word-by-word alignment with transliteration and glosses</p>
			</div>
			<div class="bg-white/20 rounded-lg px-4 py-2">
				<span class="text-sm font-mono">
					{selectedBook} {selectedChapter}:{selectedVerse}
				</span>
			</div>
		</div>
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

			<div class="flex items-center gap-2 text-sm text-gray-600">
				<Info class="h-4 w-4" />
				<span>{interlinearData ? `${interlinearData.words.length} words` : 'Select a verse'}</span>
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
	<div class="p-8 min-h-[500px]">
		{#if loading}
			<div class="flex flex-col items-center justify-center h-64">
				<Loader class="h-12 w-12 text-primary-600 animate-spin mb-4" />
				<p class="text-gray-600">Loading interlinear data...</p>
			</div>
		{:else if error}
			<div class="flex items-center justify-center h-64">
				<div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
					<h3 class="text-lg font-heading font-semibold text-red-900 mb-2">Error</h3>
					<p class="text-sm text-red-700">{error}</p>
				</div>
			</div>
		{:else if interlinearData}
			<!-- Interlinear Display -->
			<div class="space-y-6">
				<!-- Language Badge -->
				<div class="flex items-center justify-center">
					<span class="bg-indigo-100 text-indigo-800 px-4 py-2 rounded-full text-sm font-medium">
						{interlinearData.language === 'hebrew' ? 'Hebrew (Right-to-Left)' : 'Greek (Left-to-Right)'}
					</span>
				</div>

				<!-- Interlinear Grid -->
				<div class="bg-gradient-to-br from-sand-50 to-primary-50 rounded-lg p-6 border border-sand-200 overflow-x-auto">
					<div class="inline-grid gap-4" style="grid-template-columns: repeat({interlinearData.words.length}, minmax(80px, auto));">
						<!-- Row 1: Original Script -->
						{#each interlinearData.words as word}
							<div class="text-center">
								<div class="{interlinearData.language === 'hebrew' ? 'hebrew-text' : 'greek-text'} text-2xl font-bold text-gray-900 mb-2"
									 dir={interlinearData.language === 'hebrew' ? 'rtl' : 'ltr'}
								>
									{word.original}
								</div>
							</div>
						{/each}

						<!-- Row 2: Transliteration -->
						{#each interlinearData.words as word}
							<div class="text-center">
								<div class="text-sm italic text-gray-600 mb-2 font-mono">
									{word.transliteration}
								</div>
							</div>
						{/each}

						<!-- Row 3: English Gloss -->
						{#each interlinearData.words as word}
							<div class="text-center">
								<div class="text-sm text-gray-800 font-medium mb-2">
									{word.gloss}
								</div>
							</div>
						{/each}

						<!-- Row 4: Strong's Numbers (if available) -->
						{#if interlinearData.words.some(w => w.strongs)}
							{#each interlinearData.words as word}
								<div class="text-center">
									{#if word.strongs}
										<div class="text-xs text-indigo-600 font-mono bg-indigo-50 rounded px-2 py-1 inline-block">
											{word.strongs}
										</div>
									{:else}
										<div class="h-6"></div>
									{/if}
								</div>
							{/each}
						{/if}
					</div>
				</div>

				<!-- Reading Guide -->
				<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
					<div class="flex items-start gap-2">
						<Info class="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
						<div class="text-sm text-blue-900">
							<p class="font-medium mb-1">How to Read</p>
							<p class="text-blue-800">
								{#if interlinearData.language === 'hebrew'}
									Hebrew text reads right-to-left. Each column represents one Hebrew word with its transliteration
									(English pronunciation) and gloss (basic meaning).
								{:else}
									Greek text reads left-to-right. Each column represents one Greek word with its transliteration
									(English pronunciation) and gloss (basic meaning).
								{/if}
								{#if interlinearData.words.some(w => w.strongs)}
									Strong's numbers at the bottom link to lexical entries for detailed word studies.
								{/if}
							</p>
						</div>
					</div>
				</div>

				<!-- Module Attribution -->
				<div class="text-xs text-gray-500 pt-4 border-t border-sand-200">
					<p>
						{interlinearData.language === 'hebrew'
							? 'Hebrew text and morphology from Westminster Leningrad Codex (WLC 4.20) via SWORD Project'
							: 'Greek text and morphology from SBL Greek New Testament (SBLGNT 1.0) via SWORD Project'}
					</p>
				</div>
			</div>
		{:else}
			<div class="flex items-center justify-center h-64">
				<p class="text-gray-500">Select a verse to view interlinear breakdown</p>
			</div>
		{/if}
	</div>
</div>

<style>
	/* Hebrew text styling */
	:global(.hebrew-text) {
		font-family: 'Noto Serif Hebrew', 'SBL Hebrew', serif;
	}

	/* Greek text styling */
	:global(.greek-text) {
		font-family: 'Noto Sans', 'SBL Greek', sans-serif;
	}

	/* Grid layout for interlinear */
	.inline-grid {
		display: inline-grid;
		min-width: 100%;
	}

	/* Prevent text wrapping in cells */
	.inline-grid > div {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>
