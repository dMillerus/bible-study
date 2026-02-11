<script lang="ts">
	import { MapPin, Layers, Target, BookOpen, X } from 'lucide-svelte';
	import type { BiblicalPlace } from '$lib/api/geography';

	export let place: BiblicalPlace | null = null;
	export let onClose: () => void = () => {};
	export let onSearchVerses: (placeName: string) => void = () => {};

	function getConfidenceBadgeColor(level: 'high' | 'moderate' | 'low'): string {
		switch (level) {
			case 'high':
				return 'bg-green-100 text-green-800 border-green-300';
			case 'moderate':
				return 'bg-yellow-100 text-yellow-800 border-yellow-300';
			case 'low':
				return 'bg-red-100 text-red-800 border-red-300';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-300';
		}
	}

	function formatCoordinates(lat: number, lon: number): string {
		const latDir = lat >= 0 ? 'N' : 'S';
		const lonDir = lon >= 0 ? 'E' : 'W';
		return `${Math.abs(lat).toFixed(4)}°${latDir}, ${Math.abs(lon).toFixed(4)}°${lonDir}`;
	}
</script>

{#if place}
	<div class="place-detail bg-white rounded-lg shadow-xl border border-sand-200 overflow-hidden">
		<!-- Header -->
		<div class="bg-gradient-to-r from-olive-600 to-primary-600 text-white px-6 py-4 flex items-start justify-between">
			<div class="flex-1">
				<h2 class="text-2xl font-heading font-bold mb-1">{place.name}</h2>
				<div class="flex items-center gap-2 text-sm text-sand-100">
					<MapPin class="h-4 w-4" />
					<span>{formatCoordinates(place.latitude, place.longitude)}</span>
				</div>
			</div>
			<button
				on:click={onClose}
				class="text-white hover:text-sand-200 transition-colors p-1"
				title="Close"
			>
				<X class="h-5 w-5" />
			</button>
		</div>

		<!-- Content -->
		<div class="p-6 space-y-6 max-h-[600px] overflow-y-auto">
			<!-- Place Type & Confidence -->
			<div class="grid grid-cols-2 gap-4">
				<div>
					<div class="flex items-center gap-2 text-sm text-gray-600 mb-1">
						<Layers class="h-4 w-4" />
						<span class="font-medium">Place Type</span>
					</div>
					<p class="text-lg text-gray-900 capitalize">{place.place_type}</p>
				</div>
				<div>
					<div class="flex items-center gap-2 text-sm text-gray-600 mb-1">
						<Target class="h-4 w-4" />
						<span class="font-medium">Confidence</span>
					</div>
					<div class="flex items-center gap-2">
						<span class={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${getConfidenceBadgeColor(place.confidence_level)}`}>
							{place.confidence_level}
						</span>
						<span class="text-sm text-gray-500">({place.confidence_score})</span>
					</div>
				</div>
			</div>

			<!-- Alternate Names -->
			{#if place.alternate_names && place.alternate_names.length > 0}
				<div>
					<h3 class="text-sm font-heading font-semibold text-gray-900 mb-2">Also Known As</h3>
					<div class="flex flex-wrap gap-2">
						{#each place.alternate_names as altName}
							<span class="bg-sand-100 text-gray-700 px-3 py-1 rounded-full text-sm">
								{altName}
							</span>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Verse References -->
			{#if place.verse_references && place.verse_references.length > 0}
				<div>
					<div class="flex items-center gap-2 mb-3">
						<BookOpen class="h-4 w-4 text-primary-600" />
						<h3 class="text-sm font-heading font-semibold text-gray-900">
							Biblical References ({place.verse_references.length})
						</h3>
					</div>
					<div class="bg-sand-50 rounded-lg p-4 max-h-48 overflow-y-auto">
						<div class="grid grid-cols-2 gap-2">
							{#each place.verse_references.slice(0, 20) as ref}
								<button
									on:click={() => onSearchVerses(ref)}
									class="text-left text-sm text-primary-700 hover:text-primary-900 hover:underline transition-colors"
								>
									{ref}
								</button>
							{/each}
						</div>
						{#if place.verse_references.length > 20}
							<p class="text-xs text-gray-500 mt-3 text-center">
								...and {place.verse_references.length - 20} more references
							</p>
						{/if}
					</div>
				</div>
			{/if}

			<!-- Description/Content -->
			{#if place.content}
				<div>
					<h3 class="text-sm font-heading font-semibold text-gray-900 mb-2">Description</h3>
					<div class="text-sm text-gray-700 leading-relaxed bg-sand-50 rounded-lg p-4">
						{place.content}
					</div>
				</div>
			{/if}

			<!-- Action Buttons -->
			<div class="flex gap-3 pt-4 border-t border-sand-200">
				<button
					on:click={() => onSearchVerses(place.name)}
					class="flex-1 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors text-sm font-medium flex items-center justify-center gap-2"
				>
					<BookOpen class="h-4 w-4" />
					Search Verses About This Place
				</button>
			</div>

			<!-- Data Attribution -->
			<div class="text-xs text-gray-500 pt-4 border-t border-sand-200">
				<p>
					Geography data from <a href="https://www.openbible.info/" target="_blank" class="text-primary-600 hover:underline">OpenBible.info</a> (CC-BY 4.0)
				</p>
			</div>
		</div>
	</div>
{/if}

<style>
	.place-detail {
		max-width: 500px;
	}

	/* Custom scrollbar for verse references */
	.place-detail :global(*::-webkit-scrollbar) {
		width: 6px;
		height: 6px;
	}

	.place-detail :global(*::-webkit-scrollbar-track) {
		background: #f5f1e8;
		border-radius: 3px;
	}

	.place-detail :global(*::-webkit-scrollbar-thumb) {
		background: #c2b280;
		border-radius: 3px;
	}

	.place-detail :global(*::-webkit-scrollbar-thumb:hover) {
		background: #a89764;
	}
</style>
