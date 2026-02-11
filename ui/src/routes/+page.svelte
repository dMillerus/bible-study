<script lang="ts">
	import { Search, Map, Languages, BookOpen, Scroll } from 'lucide-svelte';
</script>

<svelte:head>
	<title>Prism Religious Studies - Academic Research Platform</title>
</svelte:head>

<div class="flex-1 bg-sand-50 overflow-y-auto">
	<!-- Hero section -->
	<div class="max-w-7xl mx-auto px-8 py-16">
		<div class="text-center mb-16">
			<div class="flex items-center justify-center gap-4 mb-6">
				<div class="relative">
					<Scroll class="h-16 w-16 text-primary-600" />
					<Map class="h-8 w-8 absolute -bottom-2 -right-2 text-olive-600" />
				</div>
			</div>
			<h1 class="text-5xl font-heading font-bold text-indigo-900 mb-4">
				Prism Religious Studies
			</h1>
			<p class="text-xl text-gray-700 mb-2">Academic Research Platform for Religious Texts</p>
			<p class="text-md text-gray-600 max-w-2xl mx-auto">
				Semantic search, original languages, biblical geography, and AI-powered textual analysis for scholarly research.
			</p>
			<div class="mt-4 inline-block">
				<span class="bg-indigo-100 text-indigo-800 px-4 py-2 rounded-full text-sm font-medium">
					Currently: Christianity Module
				</span>
			</div>
		</div>

		<!-- Feature cards -->
		<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
			<a
				href="/search"
				class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border border-sand-200"
			>
				<Search class="h-10 w-10 text-primary-600 mb-4" />
				<h3 class="text-lg font-heading font-semibold text-indigo-900 mb-2">Semantic Search</h3>
				<p class="text-sm text-gray-600">
					Search across 5 translations (18,069 verses) using vector similarity. AI-powered commentary and cross-references.
				</p>
			</a>

			<a
				href="/geography"
				class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border border-sand-200"
			>
				<Map class="h-10 w-10 text-olive-600 mb-4" />
				<h3 class="text-lg font-heading font-semibold text-indigo-900 mb-2">Biblical Geography</h3>
				<p class="text-sm text-gray-600">
					Interactive map of 1,342 biblical places with coordinates, confidence scores, and verse references.
				</p>
			</a>

			<a
				href="/languages"
				class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border border-sand-200"
			>
				<Languages class="h-10 w-10 text-primary-600 mb-4" />
				<h3 class="text-lg font-heading font-semibold text-indigo-900 mb-2">Original Languages</h3>
				<p class="text-sm text-gray-600">
					Hebrew (WLC) and Greek (SBLGNT) texts with interlinear display. Explore texts in their original form.
				</p>
			</a>

			<a
				href="/about"
				class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border border-sand-200"
			>
				<BookOpen class="h-10 w-10 text-indigo-600 mb-4" />
				<h3 class="text-lg font-heading font-semibold text-indigo-900 mb-2">Methodology</h3>
				<p class="text-sm text-gray-600">
					Learn about our semantic search algorithms, AI models, data sources, and research approach.
				</p>
			</a>
		</div>

		<!-- Quick stats -->
		<div class="bg-gradient-to-r from-primary-100 to-olive-100 rounded-lg p-8 border border-primary-200">
			<h2 class="text-2xl font-heading font-semibold text-indigo-900 mb-6 text-center">
				Current Corpus (Christianity)
			</h2>
			<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
				<div class="text-center">
					<div class="text-3xl font-bold text-primary-700">5</div>
					<div class="text-sm text-gray-700 mt-1">English Translations</div>
					<div class="text-xs text-gray-500 mt-1">KJV, ASV, BBE, YLT, Webster</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-olive-700">1,342</div>
					<div class="text-sm text-gray-700 mt-1">Biblical Places</div>
					<div class="text-xs text-gray-500 mt-1">With coordinates & references</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-primary-700">18,069</div>
					<div class="text-sm text-gray-700 mt-1">Indexed Verses</div>
					<div class="text-xs text-gray-500 mt-1">Semantic embeddings</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-olive-700">2</div>
					<div class="text-sm text-gray-700 mt-1">Original Languages</div>
					<div class="text-xs text-gray-500 mt-1">Hebrew WLC, Greek SBLGNT</div>
				</div>
			</div>
		</div>

		<!-- Future expansion note -->
		<div class="mt-12 text-center">
			<p class="text-sm text-gray-600">
				<span class="font-semibold">Future Expansion:</span> Islam, Judaism, and other religious traditions
			</p>
		</div>
	</div>
</div>
