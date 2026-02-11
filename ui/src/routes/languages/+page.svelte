<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Languages } from 'lucide-svelte';
	import LanguageViewer from '$lib/components/LanguageViewer.svelte';
	import InterlinearView from '$lib/components/InterlinearView.svelte';

	type ViewType = 'original' | 'interlinear';

	let currentView: ViewType = 'original';

	// Default starting verse (can be overridden by URL params)
	let initialBook = 'Genesis';
	let initialChapter = 1;
	let initialVerse = 1;

	// Check URL parameters on mount
	onMount(() => {
		const params = $page.url.searchParams;
		const bookParam = params.get('book');
		const chapterParam = params.get('chapter');
		const verseParam = params.get('verse');
		const viewParam = params.get('view');

		if (bookParam) initialBook = bookParam;
		if (chapterParam) initialChapter = parseInt(chapterParam, 10);
		if (verseParam) initialVerse = parseInt(verseParam, 10);
		if (viewParam === 'interlinear') currentView = 'interlinear';
	});
</script>

<svelte:head>
	<title>Original Languages - Prism Religious Studies</title>
</svelte:head>

<div class="flex-1 bg-sand-50 flex flex-col overflow-hidden">
	<!-- Header -->
	<div class="bg-white border-b border-sand-200 px-6 py-4">
		<div class="max-w-7xl mx-auto">
			<div class="flex items-center justify-between mb-4">
				<div class="flex items-center gap-3">
					<Languages class="h-6 w-6 text-primary-600" />
					<div>
						<h1 class="text-2xl font-heading font-bold text-indigo-900">Original Languages</h1>
						<p class="text-sm text-gray-600">
							Hebrew (WLC) and Greek (SBLGNT) texts with interlinear analysis
						</p>
					</div>
				</div>

				<!-- View Toggle -->
				<div class="flex bg-sand-100 rounded-lg p-1">
					<button
						on:click={() => currentView = 'original'}
						class="px-4 py-2 rounded-md text-sm font-medium transition-colors {currentView === 'original'
							? 'bg-white text-primary-700 shadow-sm'
							: 'text-gray-600 hover:text-gray-900'}"
					>
						Original Text
					</button>
					<button
						on:click={() => currentView = 'interlinear'}
						class="px-4 py-2 rounded-md text-sm font-medium transition-colors {currentView === 'interlinear'
							? 'bg-white text-primary-700 shadow-sm'
							: 'text-gray-600 hover:text-gray-900'}"
					>
						Interlinear
					</button>
				</div>
			</div>

			<!-- Info Banner -->
			<div class="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
				<div class="flex items-start gap-3">
					<Languages class="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
					<div class="text-sm text-blue-900">
						<p class="font-medium mb-1">Academic Original Language Resources</p>
						<p class="text-blue-800">
							Explore biblical texts in Hebrew (Westminster Leningrad Codex) and Greek (SBL Greek New Testament).
							{#if currentView === 'original'}
								Switch between Old Testament Hebrew and New Testament Greek with full Unicode rendering.
							{:else}
								View word-by-word breakdowns with transliteration and English glosses for detailed study.
							{/if}
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Content Area -->
	<div class="flex-1 overflow-y-auto">
		<div class="max-w-7xl mx-auto px-6 py-8">
			{#if currentView === 'original'}
				<LanguageViewer {initialBook} {initialChapter} {initialVerse} />
			{:else}
				<InterlinearView {initialBook} {initialChapter} {initialVerse} />
			{/if}

			<!-- Data Sources -->
			<div class="mt-8 bg-white rounded-lg shadow-md border border-sand-200 p-6">
				<h2 class="text-lg font-heading font-semibold text-indigo-900 mb-4">Data Sources</h2>
				<div class="grid md:grid-cols-2 gap-6">
					<div class="border-l-4 border-primary-500 pl-4">
						<h3 class="font-heading font-semibold text-gray-900 mb-1">Hebrew Text</h3>
						<p class="text-sm text-gray-700 mb-2">
							Westminster Leningrad Codex (WLC 4.20)
						</p>
						<p class="text-xs text-gray-600">
							Based on the Leningrad Codex (the oldest complete Hebrew Bible manuscript, dated 1008 CE).
							Includes vowel points (niqqud) and cantillation marks (te'amim).
						</p>
						<p class="text-xs text-gray-500 mt-2">
							License: Public Domain • Via SWORD Project
						</p>
					</div>

					<div class="border-l-4 border-primary-500 pl-4">
						<h3 class="font-heading font-semibold text-gray-900 mb-1">Greek Text</h3>
						<p class="text-sm text-gray-700 mb-2">
							Society of Biblical Literature Greek New Testament (SBLGNT 1.0)
						</p>
						<p class="text-xs text-gray-600">
							Critical edition of the Greek New Testament published by SBL.
							Includes full diacritics (accents, breathing marks, iota subscript).
						</p>
						<p class="text-xs text-gray-500 mt-2">
							License: CC-BY 4.0 • Via SWORD Project
						</p>
					</div>
				</div>

				<!-- Technical Notes -->
				<div class="mt-6 pt-6 border-t border-sand-200">
					<h3 class="text-sm font-heading font-semibold text-gray-900 mb-2">Technical Implementation</h3>
					<ul class="text-xs text-gray-600 space-y-1">
						<li>• <strong>SWORD Project:</strong> Cross-platform Bible study library for text parsing</li>
						<li>• <strong>Unicode rendering:</strong> Noto Serif Hebrew, Noto Sans for proper glyph display</li>
						<li>• <strong>Strong's numbers:</strong> Optional morphological and lexical data (where available)</li>
						<li>• <strong>Interlinear:</strong> Word-level alignment with transliteration (scholarly romanization)</li>
					</ul>
				</div>
			</div>

			<!-- Usage Guide -->
			<div class="mt-6 bg-sand-50 border border-sand-200 rounded-lg p-6">
				<h2 class="text-lg font-heading font-semibold text-indigo-900 mb-4">Usage Guide</h2>
				<div class="grid md:grid-cols-2 gap-6 text-sm text-gray-700">
					<div>
						<h3 class="font-semibold text-gray-900 mb-2">Original Text View</h3>
						<ul class="space-y-1">
							<li>• Switch between Hebrew (OT) and Greek (NT) tabs</li>
							<li>• Select book, chapter, and verse from dropdowns</li>
							<li>• Navigate with Previous/Next buttons</li>
							<li>• Hebrew displays right-to-left with proper Unicode</li>
							<li>• Strong's numbers shown when available</li>
						</ul>
					</div>
					<div>
						<h3 class="font-semibold text-gray-900 mb-2">Interlinear View</h3>
						<ul class="space-y-1">
							<li>• Each column = one word in original language</li>
							<li>• Row 1: Original script (Hebrew/Greek)</li>
							<li>• Row 2: Transliteration (pronunciation guide)</li>
							<li>• Row 3: English gloss (basic meaning)</li>
							<li>• Row 4: Strong's numbers (lexical reference)</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
