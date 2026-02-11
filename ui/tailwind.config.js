/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// Mediterranean tones - academic research aesthetic
				primary: {
					50: '#fef5f1',
					100: '#fde9e1',
					200: '#fbd3c3',
					300: '#f8b89f',
					400: '#f39876',
					500: '#e2725b', // Terracotta (warm, archaeological)
					600: '#d05a43',
					700: '#b04838',
					800: '#8f3b30',
					900: '#733229',
				},
				olive: {
					50: '#f7f8f4',
					100: '#eff1e8',
					200: '#dde3cd',
					300: '#c4cfaa',
					400: '#a7b884',
					500: '#6b8e23', // Olive green (ancient landscape)
					600: '#5a761d',
					700: '#4a5f18',
					800: '#3c4d14',
					900: '#2f3d10',
				},
				sand: {
					50: '#fdfcfa',
					100: '#faf8f4',
					200: '#f5f1e8',
					300: '#ede6d8',
					400: '#e2d7c3',
					500: '#c2b280', // Sand (parchment background)
					600: '#a89764',
					700: '#8a7b52',
					800: '#6e6342',
					900: '#585035',
				},
				indigo: {
					50: '#eef2f8',
					100: '#d9e3f0',
					200: '#b4c8e1',
					300: '#8aa9d0',
					400: '#5f85b7',
					500: '#1e3a5f', // Deep indigo (scholarly depth)
					600: '#192f4e',
					700: '#14253f',
					800: '#101c31',
					900: '#0c1526',
				}
			},
			fontFamily: {
				heading: ['Crimson Text', 'Georgia', 'serif'], // Scholarly headings
				body: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'], // Modern readable body
				hebrew: ['Noto Serif Hebrew', 'serif'], // Hebrew text
				greek: ['Noto Sans', 'sans-serif'], // Greek text
				mono: ['JetBrains Mono', 'monospace'], // Code/interlinear
			}
		}
	},
	plugins: []
};
