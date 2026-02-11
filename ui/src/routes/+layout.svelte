<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { Scroll, MapPin, Search, Map, Languages, Info } from 'lucide-svelte';
</script>

<div class="app h-screen flex flex-col">
	<!-- Top navigation bar -->
	<nav class="bg-primary-700 text-sand-50 px-6 py-3 flex items-center justify-between shadow-md">
		<a href="/" class="flex items-center gap-3 hover:opacity-80 transition-opacity">
			<div class="relative">
				<Scroll class="h-6 w-6" />
				<MapPin class="h-3 w-3 absolute -bottom-1 -right-1 text-olive-300" />
			</div>
			<div class="flex flex-col">
				<h1 class="text-xl font-bold font-heading">Prism Religious Studies</h1>
				<span class="text-xs text-sand-100 font-body">Academic Research Platform for Religious Texts</span>
			</div>
			<span class="text-xs bg-indigo-700 px-3 py-1 rounded-full ml-2 font-medium">Christianity</span>
		</a>

		<div class="flex items-center gap-6">
			<a
				href="/search"
				class="flex items-center gap-2 text-sm hover:text-sand-100 transition-colors {$page.url.pathname.startsWith('/search') ? 'text-sand-50 font-semibold border-b-2 border-sand-50 pb-1' : ''}"
			>
				<Search class="h-4 w-4" />
				<span>Search</span>
			</a>
			<a
				href="/geography"
				class="flex items-center gap-2 text-sm hover:text-sand-100 transition-colors {$page.url.pathname.startsWith('/geography') ? 'text-sand-50 font-semibold border-b-2 border-sand-50 pb-1' : ''}"
			>
				<Map class="h-4 w-4" />
				<span>Geography</span>
			</a>
			<a
				href="/languages"
				class="flex items-center gap-2 text-sm hover:text-sand-100 transition-colors {$page.url.pathname.startsWith('/languages') ? 'text-sand-50 font-semibold border-b-2 border-sand-50 pb-1' : ''}"
			>
				<Languages class="h-4 w-4" />
				<span>Languages</span>
			</a>
			<a
				href="/about"
				class="flex items-center gap-2 text-sm hover:text-sand-100 transition-colors {$page.url.pathname.startsWith('/about') ? 'text-sand-50 font-semibold border-b-2 border-sand-50 pb-1' : ''}"
			>
				<Info class="h-4 w-4" />
				<span>About</span>
			</a>
		</div>
	</nav>

	<!-- Page content -->
	<slot />

	<!-- Footer status bar -->
	<footer class="bg-indigo-900 text-sand-200 px-6 py-2 text-xs flex items-center justify-between">
		<div class="flex items-center gap-4">
			<span>Powered by Prism + Ollama</span>
			<span class="text-indigo-600">|</span>
			<span>5 translations • 18,069 verses • 1,342 places • Hebrew/Greek texts</span>
		</div>
		<div>
			<a href="https://github.com/anthropics/claude-code" target="_blank" class="hover:text-sand-50 transition-colors">
				Built with Claude Code
			</a>
		</div>
	</footer>
</div>

<style>
	.app {
		min-width: 1280px; /* Desktop-only design */
	}
</style>
