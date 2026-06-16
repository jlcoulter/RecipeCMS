"""Keyword/taxonomy listing page templates."""

from .page_layout import get_opener, get_header, get_footer
from .tiles import render_item_tile, render_keyword_section


def generate_keyword_page(taxonomy_key, value, items, config, formatter, taxonomy_index, schema_gen):
    """Generate HTML for a single keyword/taxonomy value page."""
    taxonomy = config.get_taxonomy_by_key(taxonomy_key)
    prefix_text = taxonomy.get('link_prefix_text', '') if taxonomy else ''
    suffix_text = taxonomy.get('link_suffix_text', '') if taxonomy else ''

    html = ""
    html += get_opener(config, formatter)
    html += f'<title>{value} {config.item_name_plural} - {config.site_name}</title>'
    html += f'<meta name="description" content="{prefix_text} {value} {suffix_text} - {config.site_name}">'

    item_list_json = schema_gen.generate_item_list_schema(items, formatter)
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
    html += f'<h1 class="offset removeOffsetHeight">{prefix_text} {value} {suffix_text}</h1>'
    html += '<div class="recipeContainer">'
    for item in items:
        html += render_item_tile(item, config, formatter)
    html += '</div>'
    html += render_keyword_section(taxonomy_index, config, formatter, "", 20)
    html += get_footer(config, formatter)

    return html


def generate_all_keywords_page(config, taxonomy_index, formatter):
    """Generate HTML for the all-keywords overview page."""
    html = ""
    html += get_opener(config, formatter)
    html += f'<title>All Keywords - {config.site_name}</title>'
    html += f'<meta name="description" content="Listing out and linking to all keyword pages">'
    html += get_header(config, formatter)
    html += '<h1 class="offset removeOffsetHeight">All Keyword Pages</h1>'
    html += render_keyword_section(taxonomy_index, config, formatter, 'style="min-width: fit-content;"', 99999)
    html += get_footer(config, formatter)

    return html