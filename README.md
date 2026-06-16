# StaticCMS

A zero-dependency, general-purpose static site generator built with Python stdlib only. Turn a directory of JSON content files into a fully structured, SEO-optimized static website with taxonomy pages, search, and JSON-LD schema.

Originally built for [Just My Cooking](https://justmy.cooking) -- now generalized so you can use it for recipes, cocktails, books, or any content collection.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/static-cms.git
cd static-cms

# 2. Edit the config
# Copy and modify site_config.json for your site

# 3. Add your content
# Place JSON files in content/items/{item_name}/{item_name}.json
# Place images alongside the JSON

# 4. Build
python3 build.py [path/to/site_config.json]
```

Output goes to `output/`. Deploy it anywhere that serves static files.

## Configuration

All configuration lives in `site_config.json`. Here's the full schema:

```json
{
  "site_name": "My Site",
  "site_url": "https://example.com",
  "site_description": "A description of your site",
  "item_name": "Recipe",
  "item_name_plural": "Recipes",
  "content_dir": "content",
  "output_dir": "output",
  "remove_html_extension": true,
  "items_per_page": 15,
  "custom_header_html": "",
  "about_text": "<p>About this site...</p>",
  "search_result_limits": {
    "items": 9
  },
  "taxonomies": [
    {
      "key": "recipeCuisine",
      "label": "Cuisines",
      "link_prefix_text": "All",
      "link_suffix_text": "Recipes",
      "search_limit": 9
    }
  ],
  "style": {
    "light_bg": "#fffcf7",
    "light_text": "black",
    "light_subtitle": "rgb(56, 56, 56)",
    "light_border": "rgb(27, 27, 27)",
    "light_background": "#ffffff",
    "light_item_background": "#ffecdc",
    "dark_bg": "rgb(14 14 14)",
    "dark_text": "rgb(241, 241, 241)",
    "dark_subtitle": "rgb(210, 210, 210)",
    "dark_border": "rgb(41 41 41)",
    "dark_background": "#2d101f",
    "dark_item_background": "#1b1b1b",
    "font_family": "\"Ubuntu\", serif",
    "font_weight": "700",
    "border_radius": "1rem",
    "border_width": "0.2rem"
  },
  "fonts": [
    {
      "preconnect": "https://fonts.googleapis.com",
      "preconnect_crossorigin": "https://fonts.gstatic.com",
      "css_url": "https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;700&display=swap"
    }
  ],
  "schema": {
    "type": "Recipe",
    "diet_mapping": {
      "Gluten-Free": "https://schema.org/GlutenFreeDiet",
      "Vegan": "https://schema.org/VeganDiet"
    }
  },
  "sitemap_static_dates": {
    "about": "2025-06-01",
    "search": "2025-06-01",
    "all_items": "2025-06-01",
    "all_keywords": "2025-06-01",
    "collections": "2025-06-01"
  }
}
```

### Key Config Fields

| Field | Description |
|-------|-------------|
| `item_name` | Singular name for your content type (e.g. "Recipe", "Cocktail", "Book") |
| `item_name_plural` | Plural name (e.g. "Recipes", "Cocktails", "Books") |
| `remove_html_extension` | Strip `.html` from URLs (requires server config) |
| `items_per_page` | Number of items per index page |
| `about_text` | HTML string rendered on the about page |
| `custom_header_html` | Extra HTML injected into `<head>` |

## Content Structure

```
content/
  items/
    my_item/
      my_item.json       # Content data (schema.org compatible)
      my_item_0.jpg      # Primary image
      my_item_1.jpg      # Additional images (optional)
  collections/
    my_collection.json   # Grouped items (listacles)
  shared_notes/
    my_notes.json        # Reusable notes shared across items
```

### Item JSON Format

Items follow [schema.org/Recipe](https://schema.org/Recipe) conventions (adaptable via `schema.type`):

```json
{
  "name": "My Item",
  "folder": "my_item",
  "image": ["my_item_0.jpg"],
  "description": "A short description",
  "datePublished": "2025-01-01",
  "lastMod": "2025-01-15",
  "recipeCuisine": "Italian",
  "recipeCategory": "Main Course",
  "prepTime": "PT15M",
  "cookTime": "PT30M",
  "totalTime": "PT45M",
  "recipeYield": "4 servings",
  "recipeIngredient": ["Ingredient 1", "Ingredient 2"],
  "ingredientKeywords": ["Keyword1", "Keyword2"],
  "equipment": ["Pan"],
  "recipeInstructions": [
    {"@type": "HowToStep", "name": "Step 1", "url": "my_item#1", "text": "Do something"}
  ],
  "notes": ["Tip or note"],
  "relatedRecipes": ["other_item_folder"]
}
```

### Collection JSON Format

```json
{
  "name": "My Collection",
  "folder": "my_collection",
  "description": "A themed collection",
  "image": "representative_item_folder",
  "recipes": [
    {"folder": "item_one", "description": "Why it's here"},
    {"folder": "item_two", "description": "Another reason"}
  ]
}
```

### Shared Notes JSON Format

```json
{
  "description": "Notes about jerky",
  "notes": ["Note one", "Note two"]
}
```

## Taxonomy System

Taxonomies are fully user-defined in `site_config.json`. Each taxonomy entry creates:
- A keyword page for each value (e.g. `/keywords/italian.html`)
- Cross-links from item pages to keyword pages
- Search result sections
- Stats on the about page

```json
{
  "key": "recipeCuisine",
  "label": "Cuisines",
  "link_prefix_text": "All",
  "link_suffix_text": "Recipes",
  "search_limit": 9
}
```

### Ingredient Taxonomy

For the special ingredient cross-linking feature (where ingredients in the ingredient list get auto-linked to their keyword page), mark a taxonomy with `"type": "ingredient"`:

```json
{
  "key": "ingredientKeywords",
  "label": "Ingredients",
  "type": "ingredient",
  "link_prefix_text": "All",
  "link_suffix_text": "Dishes",
  "search_limit": 9
}
```

This enables the plural-matching logic that links "Tomatoes" in ingredient text to the "Tomato" keyword page.

## Custom Styling

### Config-Level Colors

Edit the `style` object in `site_config.json` to customize colors, fonts, border radius, and more. Values are injected as CSS custom properties in `:root`.

### Custom CSS Override

Place a `custom.css` file in the project root. It will be:
1. Copied to `output/custom.css`
2. Linked after `style.css` in every page's `<head>`

Use it to override any default styles or add new ones.

## Output Structure

```
output/
  index.html              # Paginated home (index.html, index1.html, ...)
  about.html               # About page with stats
  search.html + search.js  # Client-side search
  all_items.html           # A-Z listing
  all_keywords.html         # All taxonomy pages linked
  collections.html          # Collections index
  sitemap.xml              # XML sitemap
  style.css                # Generated CSS
  random.js                # Random item JS
  items/{folder}/           # Item detail pages + images
  keywords/{slug}.html     # Taxonomy value pages
  collections/{slug}.html  # Collection pages
  [favicons, webmanifest]  # Copied from static/
```

## Usage Examples

### Recipe Site (default)
```
item_name: "Recipe", item_name_plural: "Recipes"
schema.type: "Recipe"
```

### Cocktail Site
```
item_name: "Cocktail", item_name_plural: "Cocktails"
schema.type: "Recipe"  (schema.org doesn't have Cocktail)
site_url: "https://mybar.co"
```

### Book Collection
```
item_name: "Book", item_name_plural: "Books"
schema.type: "Book"
taxonomies: [{key: "genre", label: "Genres"}, {key: "author", label: "Authors"}]
```

## Project Structure

```
build.py              # Main build script
site_config.json      # Site configuration
default_style.py      # CSS generation from config
lib/
  config.py            # SiteConfig loader
  content_loader.py    # Walks content dirs, loads JSON
  taxonomy.py          # Dynamic taxonomy indexing
  link_formatter.py    # URL formatting
  date_helpers.py      # ISO 8601 duration parsing
  schema_generator.py  # JSON-LD structured data
  stats.py             # About page statistics
  sitemap.py           # Sitemap XML generation
templates/
  page_layout.py        # Opener, header, footer
  tiles.py             # Reusable tile components
  item_page.py          # Item detail page
  collection_page.py   # Collection pages
  keyword_pages.py     # Taxonomy keyword pages
  index_page.py        # Paginated index + A-Z
  search_page.py       # Search page
  about_page.py         # About page
  js_templates.py      # Search JS + random JS
content/
  items/               # Individual content items
  collections/         # Grouped collections
  shared_notes/        # Shared notes
static/                # Favicons, webmanifest
templates_json/        # Template JSONs for new items
```

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

## License

MIT. See [LICENSE](LICENSE).