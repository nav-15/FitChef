# Fit Chef Australia — Animated Landing Page

Single-page concept landing page for Fit Chef Australia (fitchefaus.com), inspired by the scroll-driven, playful interaction style of crazycreative.design.

## Files

```
fitchef-landing/
├── index.html           # the entire site — HTML, CSS, JS in one file
├── images/              # all photography (3.2 MB total, web-optimised)
└── README.md            # this file
```

## Quick start

Open `index.html` in any browser. No build step, no dependencies.

For live-reload while editing in VS Code, install the **Live Server** extension, then right-click `index.html` → "Open with Live Server".

## What's where in `index.html`

The file is organised top-to-bottom in this order:

1. **`<head>`** — fonts, brand colors as CSS variables (search `--brand-teal`)
2. **`.nav`** — fixed top nav with logo, links, CTA
3. **`.hero`** — headline + 6 floating product photos with parallax
4. **`.marquee`** — infinite scrolling tagline strip
5. **`.scene` / `.stage`** — sticky "Why Fit Chef" — 4 cards fly in from corners as you scroll
6. **`.how`** — How It Works, 4-step grid on dark background
7. **`.menu-section` / `.menu-stage`** — sticky menu showcase, 8 meal cards orbit a central title
8. **`.lifestyle-strip`** — full-bleed parallax band
9. **`.testimonials`** — 3 customer quotes
10. **`.final`** — closing CTA with floating product images
11. **`<script>`** — all scroll-driven animation logic (vanilla JS, no libraries)

## Brand tokens (CSS variables, defined at the top of `<style>`)

| Variable | Value | Usage |
|---|---|---|
| `--brand-teal` | `#159E80` | primary brand color, exact match to logo |
| `--brand-teal-d` | `#0F7D65` | hover/depth |
| `--brand-teal-l` | `#2DB89A` | lighter accent |
| `--brand-lime` | `#C4E94B` | the lime accent from the "Ready Fresh Meals" badge |
| `--cream` | `#F5F0E4` | warm off-white page background |
| `--ink` | `#0E2A23` | deep forest near-black, used for text and dark sections |
| `--font-display` | Manrope | display font (placeholder for paid Vera Pro) |

## Switching to Vera Pro (the actual brand font)

Vera Pro is a paid Adobe Fonts release, so I substituted Manrope (closest free match). To swap:

1. Sign in to Adobe Fonts, add Vera Pro to a web project, copy the `<link>` tag they give you
2. Paste it into `<head>` (replacing or alongside the Manrope `<link>`)
3. Find `--font-display: 'Manrope', system-ui, sans-serif;` and change it to `--font-display: 'vera-pro', system-ui, sans-serif;` (or whatever name Adobe assigns)

Everything else inherits automatically.

## Image inventory (`images/` folder)

**Product shots** (square, white background — used in meal cards & hero floats)
- `product-roast-chicken.jpg`, `product-roast-chicken-shred.jpg`
- `product-laksa-bowl.jpg`, `product-taco-bowl.jpg`, `product-burger-bowl.jpg`
- `product-biryani.jpg`, `product-garlic-prawns.jpg`
- `product-chicken-salad.jpg`, `product-cauliflower-quinoa.jpg`
- `product-tofu-curry.jpg`, `product-vegan-penne.jpg`, `product-chimichurri-steak.jpg`

**Lifestyle shots** (used in why-cards, how-it-works, lifestyle strip)
- `lifestyle-three-plates.jpg` — three dishes flat lay
- `lifestyle-spread.jpg` — packs + plated meals spread
- `lifestyle-vegan-spread.jpg` — vegan dishes spread
- `lifestyle-packs-flatlay.jpg` — multiple sealed packs
- `lifestyle-three-packs-green.jpg` — three packs on green
- `lifestyle-tofu-veg-spread.jpg` — tofu noodles + sides
- `hand-holding-stack.jpg` — iconic hand holding stacked meals on brand teal
- `kitchen-box.jpg` — delivery box on kitchen counter

**Brand**
- `logo-square.png` — the official Fit Chef logo
- `badge-ready-fresh.png` — "Ready Fresh Meals" lime badge
- `icon-chef.png` — chef silhouette icon

## Known placeholder

In **How It Works → Step 2** there's one clearly-marked placeholder:
```html
<div class="step-img"><div class="ph">📸 IMG SLOT:<br>chef cooking /<br>kitchen action shot</div></div>
```
Replace with `<img src="images/your-chef-photo.jpg" alt="...">` when you have a chef-at-work photo.

## Things you might want to do next

- Wire up the "Order Now" / "View the Menu" buttons to real shop URLs
- Swap testimonial text + names for real Google/Trustpilot reviews
- Add SEO `<meta>` tags (description, og:image, etc.)
- Add a real favicon
- Replace placeholder copy in step 2 of How It Works
