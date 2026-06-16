"""Collection (listacle) page templates."""

from .page_layout import get_opener, get_header, get_footer
from .tiles import render_item_tile, render_collection_tile, render_keyword_section


def generate_collection_page(collection, config, formatter, get_item_func, schema_gen):
    """Generate HTML for a single collection page."""
    html = ""
    html += get_opener(config, formatter)
    html += f'<title>{collection["name"]} - {config.site_name}</title>'
    html += f'<meta name="description" content="{collection["description"]}">'

    item_list_json = schema_gen.generate_collection_item_list_schema(collection, formatter)
    html += f"""
        <script type="application/ld+json">
        {{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": {item_list_json}
        }}
        </script>
    """
    html += get_header(config, formatter)

    html += f'<h1 class="offset" style="margin-bottom:0rem;">{collection["name"]}</h1>'
    html += f'<p class="offset" style="margin-bottom:0rem;">{collection["description"]}</p>'
    html += '<div class="recipeContainer">'

    for recipe in collection.get('recipes', []):
        item = get_item_func(recipe['folder'])
        if item:
            html += render_item_tile(item, config, formatter, recipe.get('description', ''))
    html += '</div>'
    html += get_footer(config, formatter)

    return html


def generate_collections_index(collections, config, formatter, taxonomy_index, schema_gen):
    """Generate HTML for the collections index page."""
    html = ""
    html += get_opener(config, formatter)
    html += f'<title>Collections - {config.site_name}</title>'
    html += f'<meta name="description" content="Meaningful groupings of {config.item_name_plural.lower()} on this site.">'

    item_list_json = schema_gen.generate_collection_index_schema(collections, formatter)
    html += f"""
        <script type="application/ld+json">
        {{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": {item_list_json}
        }}
        </script>
    """
    html += get_header(config, formatter)

    html += f'<h1 class="offset" style="margin-bottom:0rem;">Collections</h1>'
    html += f'<p class="offset" style="margin-bottom:0rem;">Meaningful groupings of {config.item_name_plural.lower()} on this site.</p>'
    html += '<div class="recipeContainer">'
    for collection in collections:
        html += render_collection_tile(collection, config, formatter, _dummy_get_item)
    html += '</div>'

    html += render_keyword_section(taxonomy_index, config, formatter, "", 20)
    html += get_footer(config, formatter)

    return html


def _dummy_get_item(folder):
    """Placeholder -- the real implementation needs access to all_items."""
    return None