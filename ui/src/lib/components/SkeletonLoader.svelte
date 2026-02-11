<script lang="ts">
	export let type: 'text' | 'card' | 'map' | 'grid' = 'text';
	export let count: number = 1;
</script>

<div class="skeleton-container">
	{#if type === 'text'}
		{#each Array(count) as _}
			<div class="skeleton skeleton-text mb-2"></div>
		{/each}
	{:else if type === 'card'}
		{#each Array(count) as _}
			<div class="skeleton skeleton-card mb-4 p-4 rounded-lg">
				<div class="skeleton skeleton-title mb-2"></div>
				<div class="skeleton skeleton-text mb-2"></div>
				<div class="skeleton skeleton-text w-3/4"></div>
			</div>
		{/each}
	{:else if type === 'map'}
		<div class="skeleton skeleton-map rounded-lg"></div>
	{:else if type === 'grid'}
		<div class="grid grid-cols-2 gap-4">
			{#each Array(count) as _}
				<div class="skeleton skeleton-card p-4 rounded-lg">
					<div class="skeleton skeleton-text mb-2"></div>
					<div class="skeleton skeleton-text"></div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.skeleton {
		background: linear-gradient(
			90deg,
			#f0f0f0 0%,
			#e0e0e0 50%,
			#f0f0f0 100%
		);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
	}

	.skeleton-text {
		height: 1rem;
		border-radius: 0.25rem;
	}

	.skeleton-title {
		height: 1.5rem;
		width: 60%;
		border-radius: 0.25rem;
	}

	.skeleton-card {
		background: white;
		border: 1px solid #e5e7eb;
	}

	.skeleton-map {
		height: 400px;
		width: 100%;
	}

	@keyframes shimmer {
		0% {
			background-position: -200% 0;
		}
		100% {
			background-position: 200% 0;
		}
	}
</style>
