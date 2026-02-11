<script lang="ts">
	import { AlertTriangle, RefreshCw } from 'lucide-svelte';

	export let error: string;
	export let onRetry: (() => void) | null = null;
	export let context: string = 'this feature';
</script>

<div class="error-boundary bg-red-50 border-2 border-red-200 rounded-lg p-6 max-w-2xl mx-auto">
	<div class="flex items-start gap-4">
		<AlertTriangle class="h-8 w-8 text-red-600 flex-shrink-0" />
		<div class="flex-1">
			<h3 class="text-lg font-heading font-semibold text-red-900 mb-2">
				Error Loading {context}
			</h3>
			<p class="text-sm text-red-700 mb-4">{error}</p>

			<div class="space-y-2 text-sm text-red-800">
				<p class="font-medium">Possible solutions:</p>
				<ul class="list-disc list-inside space-y-1 ml-2">
					<li>Check that the Prism API is running at <code class="bg-red-100 px-1 rounded">http://localhost:8100</code></li>
					<li>Verify your internet connection</li>
					<li>Try refreshing the page</li>
					{#if onRetry}
						<li>Click the retry button below</li>
					{/if}
				</ul>
			</div>

			{#if onRetry}
				<button
					on:click={onRetry}
					class="mt-4 flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
				>
					<RefreshCw class="h-4 w-4" />
					Retry
				</button>
			{/if}
		</div>
	</div>
</div>

<style>
	code {
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.875rem;
	}
</style>
