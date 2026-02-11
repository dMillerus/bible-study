<script lang="ts">
	import { Info, Database, Cpu, BookOpen, Shield } from 'lucide-svelte';
</script>

<svelte:head>
	<title>About & Methodology - Prism Religious Studies</title>
</svelte:head>

<div class="flex-1 bg-sand-50 overflow-y-auto">
	<div class="max-w-5xl mx-auto px-8 py-16">
		<div class="text-center mb-12">
			<Info class="h-16 w-16 text-indigo-600 mx-auto mb-4" />
			<h1 class="text-4xl font-heading font-bold text-indigo-900 mb-4">About & Methodology</h1>
			<p class="text-lg text-gray-700 max-w-2xl mx-auto">
				Learn about our semantic search algorithms, AI models, data sources, and academic research approach.
			</p>
		</div>

		<!-- About Section -->
		<div class="bg-white rounded-lg shadow-lg p-8 mb-8 border border-sand-200">
			<h2 class="text-2xl font-heading font-semibold text-indigo-900 mb-4">About Prism Religious Studies</h2>
			<div class="prose prose-lg max-w-none text-gray-700 space-y-4">
				<p>
					<strong>Prism Religious Studies</strong> is an academic research platform for religious texts,
					starting with Christianity and designed to expand to other religious traditions including Islam, Judaism,
					and others.
				</p>
				<p>
					Our current <strong>Christianity Module</strong> provides researchers with semantic search across 5 Bible translations,
					original Hebrew and Greek texts, biblical geography data for 1,342 places, and AI-powered textual analysis
					for scholarly exploration.
				</p>
				<p>
					This platform is part of the <strong>Prism (Personal Semantic Data Layer)</strong> ecosystem, providing
					specialized tools for religious studies research while maintaining the same high-quality semantic search
					and knowledge retrieval capabilities used across all Prism applications.
				</p>
			</div>
		</div>

		<!-- Methodology Section -->
		<div class="bg-white rounded-lg shadow-lg p-8 mb-8 border border-sand-200">
			<h2 class="text-2xl font-heading font-semibold text-indigo-900 mb-6 flex items-center gap-2">
				<Cpu class="h-6 w-6" />
				Methodology
			</h2>
			<div class="space-y-6">
				<div>
					<h3 class="text-lg font-heading font-semibold text-gray-900 mb-2">Semantic Search Algorithm</h3>
					<p class="text-gray-700 mb-2">
						Queries are converted to vector embeddings using <code class="bg-sand-100 px-2 py-1 rounded text-sm">nomic-embed-text</code>
						(768 dimensions) and compared against indexed verse embeddings using cosine similarity.
					</p>
					<ul class="text-sm text-gray-600 space-y-1 ml-6">
						<li>• <strong>Index:</strong> HNSW (Hierarchical Navigable Small World)</li>
						<li>• <strong>Similarity range:</strong> 0.6-0.9 typical scores</li>
						<li>• <strong>Latency:</strong> ~400ms for semantic search</li>
					</ul>
				</div>

				<div>
					<h3 class="text-lg font-heading font-semibold text-gray-900 mb-2">AI Models</h3>
					<ul class="text-sm text-gray-700 space-y-2">
						<li>
							<strong>Commentary Generation:</strong> Qwen 2.5 14B via Ollama
							<span class="text-gray-600">(temperature=0.7 for creative insights)</span>
						</li>
						<li>
							<strong>Embeddings:</strong> nomic-embed-text
							<span class="text-gray-600">(768-dimensional vectors)</span>
						</li>
						<li>
							<strong>Response Time:</strong> 3-5s first generation, <100ms cached
						</li>
					</ul>
				</div>

				<div>
					<h3 class="text-lg font-heading font-semibold text-gray-900 mb-2">Chunking Strategy</h3>
					<p class="text-gray-700 text-sm">
						Biblical verses are indexed as individual semantic units with metadata (book, chapter, verse, translation).
						This approach preserves verse boundaries while enabling cross-translation search and comparison.
					</p>
				</div>
			</div>
		</div>

		<!-- Data Sources Section -->
		<div class="bg-white rounded-lg shadow-lg p-8 mb-8 border border-sand-200">
			<h2 class="text-2xl font-heading font-semibold text-indigo-900 mb-6 flex items-center gap-2">
				<Database class="h-6 w-6" />
				Data Sources & Attribution
			</h2>
			<div class="space-y-4">
				<div class="border-l-4 border-primary-500 pl-4">
					<h3 class="font-heading font-semibold text-gray-900">Hebrew Text</h3>
					<p class="text-sm text-gray-700">
						Westminster Leningrad Codex (WLC 4.20) • Public Domain
					</p>
				</div>
				<div class="border-l-4 border-primary-500 pl-4">
					<h3 class="font-heading font-semibold text-gray-900">Greek Text</h3>
					<p class="text-sm text-gray-700">
						Society of Biblical Literature Greek New Testament (SBLGNT 1.0) • CC-BY 4.0
					</p>
				</div>
				<div class="border-l-4 border-olive-500 pl-4">
					<h3 class="font-heading font-semibold text-gray-900">Biblical Geography</h3>
					<p class="text-sm text-gray-700">
						OpenBible.info (1,342 places) • CC-BY 4.0
					</p>
				</div>
				<div class="border-l-4 border-indigo-500 pl-4">
					<h3 class="font-heading font-semibold text-gray-900">English Translations</h3>
					<p class="text-sm text-gray-700">
						SWORD Project modules (KJV, ASV, BBE, YLT, Webster) • Public Domain
					</p>
				</div>
			</div>
		</div>

		<!-- Limitations Section -->
		<div class="bg-amber-50 border border-amber-200 rounded-lg p-6 mb-8">
			<h2 class="text-xl font-heading font-semibold text-amber-900 mb-4 flex items-center gap-2">
				<Shield class="h-5 w-5" />
				Known Limitations
			</h2>
			<ul class="text-sm text-gray-700 space-y-2">
				<li>
					<strong>Geography Search:</strong> Works best with descriptive queries (e.g., "capital city David")
					rather than specific place names. Use place types and descriptions for better results.
				</li>
				<li>
					<strong>AI Commentary:</strong> Generated insights are for research exploration, not definitive interpretation.
					Always consult scholarly commentaries for authoritative analysis.
				</li>
				<li>
					<strong>Textual Variants:</strong> Critical apparatus and manuscript variants not yet included.
					Consult critical editions (NA28, BHS) for detailed textual scholarship.
				</li>
			</ul>
		</div>

		<!-- Credits Section -->
		<div class="bg-white rounded-lg shadow-lg p-8 border border-sand-200">
			<h2 class="text-2xl font-heading font-semibold text-indigo-900 mb-6 flex items-center gap-2">
				<BookOpen class="h-6 w-6" />
				Credits
			</h2>
			<div class="grid md:grid-cols-2 gap-6 text-sm text-gray-700">
				<div>
					<h3 class="font-heading font-semibold text-gray-900 mb-2">Development</h3>
					<ul class="space-y-1">
						<li>• Built with Claude Code</li>
						<li>• LLM: Anthropic Claude Sonnet 4.5</li>
						<li>• Framework: SvelteKit + TypeScript</li>
					</ul>
				</div>
				<div>
					<h3 class="font-heading font-semibold text-gray-900 mb-2">Infrastructure</h3>
					<ul class="space-y-1">
						<li>• Search Engine: Prism (PSDL)</li>
						<li>• Database: PostgreSQL + pgvector</li>
						<li>• AI Backend: Ollama (local inference)</li>
					</ul>
				</div>
			</div>

			<div class="mt-6 pt-6 border-t border-sand-200 text-center">
				<p class="text-xs text-gray-500">
					This is an academic research tool. For questions or feedback, please consult the project documentation.
				</p>
			</div>
		</div>
	</div>
</div>
