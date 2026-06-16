"""Index page templates with pagination."""

import math
from .page_layout import get_opener, get_header, get_footer
from .tiles import render_item_tile, render_keyword_section, render_page_numbers


def generate_index_pages(items, config, taxonomy_index, formatter, schema_gen):
    """Generate paginated index pages. Returns list of generated page filenames."""
    sorted_items = sorted(items, key=lambda x: x['datePublished'], reverse=True)
    index_pages = []
    chunk_size = config.items_per_page
    num_chunks = math.ceil(len(sorted_items) / chunk_size)

    for i in range(num_chunks):
        chunk = sorted_items[i * chunk_size:(i + 1) * chunk_size]
        html_name = "index.html" if i == 0 else f"index{i}.html"
        index_pages.append(html_name)

        html = ""
        html += get_opener(config, formatter)
        html += f'<title>{config.site_name}</title>'
        html += f'<meta name="description" content="{config.site_description}">'

        item_list_json = schema_gen.generate_item_list_schema(chunk, formatter)
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

        html += f'<h1 class="offset" style="margin-bottom:0rem;">Latest {config.item_name_plural}</h1>'
        html += '<div class="recipeContainer">'
        for item in chunk:
            html += render_item_tile(item, config, formatter)
        html += '</div>'

        html += render_page_numbers(i, num_chunks - 1, config, formatter)
        html += render_keyword_section(taxonomy_index, config, formatter, "", 20)
        html += get_footer(config, formatter)

        # Write the file
        import os
        html_path = os.path.join(config.output_dir, html_name)
        with open(html_path, 'w') as f:
            f.write(html)

    return index_pages


def generate_all_items_page(items, config, formatter, schema_gen):
    """Generate the all-items A-Z listing page."""
    html = ""
    html += get_opener(config, formatter)
    html += f'<title>All {config.item_name_plural} - {config.site_name}</title>'
    html += f'<meta name="description" content="All of the {config.item_name_plural.lower()} on {config.site_name}">'

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

    html += f'<h1 class="offset" style="margin-bottom:0rem;">All {config.item_name_plural} (A-Z)</h1>'
    html += '<div class="recipeContainer">'

    for item in items:
        html += render_item_tile(item, config, formatter)
    html += '</div>'
    html += get_footer(config, formatter)

    return html