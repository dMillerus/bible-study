<script lang="ts">
	import SearchBar from '$lib/components/SearchBar.svelte';
	import ResultsList from '$lib/components/ResultsList.svelte';
	import TranslationGrid from '$lib/components/TranslationGrid.svelte';
	import AIPanel from '$lib/components/AIPanel.svelte';
</script>

<svelte:head>
	<title>Search - Prism Religious Studies</title>
</svelte:head>

<!-- Search bar -->
<SearchBar />

<!-- Main content area with responsive 3-panel layout -->
<div class="flex-1 flex flex-col md:flex-row overflow-hidden">
	<!-- Left panel: Results list -->
	<aside class="w-full md:w-80 md:flex-shrink-0 h-64 md:h-auto border-b md:border-b-0 md:border-r border-gray-200">
		<ResultsList />
	</aside>

	<!-- Center panel: Translation comparison -->
	<main class="flex-1 overflow-hidden">
		<TranslationGrid />
	</main>

	<!-- Right panel: AI insights (hidden on tablet, shown on desktop) -->
	<aside class="hidden lg:block w-96 flex-shrink-0">
		<AIPanel />
	</aside>
</div>

<style>
	/* Responsive breakpoints:
	   - Mobile (<768px): Stack vertically, results scrollable
	   - Tablet (768px-1024px): Two columns (results + translations)
	   - Desktop (1024px+): Full three columns
	*/
	@media (max-width: 767px) {
		/* Mobile: Vertical stack with scrollable sections */
	}
</style>
