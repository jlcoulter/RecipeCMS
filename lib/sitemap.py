"""Sitemap XML generation."""


def generate_sitemap(config, items, taxonomy_index, collections, index_pages, formatter):
    """Generate a sitemap.xml string from all site pages."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    def sitemap_entry(loc, lastmod):
        formatted_loc = formatter.format_link(loc)
        return f"""
    <url>
        <loc>{formatted_loc}</loc>
        <lastmod>{lastmod}</lastmod>
    </url>"""

    # Index pages
    for index_page_name in index_pages:
        loc = f"{config.site_url}/{index_page_name}"
        lines.append(sitemap_entry(loc, config.sitemap_static_dates.get('index', '2025-01-01')))

    # Static pages
    static_pages = [
        ["search.html", config.sitemap_static_dates.get('search', '2025-01-01')],
        ["about.html", config.sitemap_static_dates.get('about', '2025-01-01')],
        ["all_keywords.html", config.sitemap_static_dates.get('all_keywords', '2025-01-01')],
        ["all_items.html", config.sitemap_static_dates.get('all_items', '2025-01-01')],
        ["collections.html", config.sitemap_static_dates.get('collections', '2025-01-01')],
    ]
    for page in static_pages:
        loc = f"{config.site_url}/{page[0]}"
        lines.append(sitemap_entry(loc, page[1]))

    # Keyword/taxonomy pages
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        for value in taxonomy_index.maps.get(key, {}).keys():
            file_name = value.lower().replace(" ", "_") + ".html"
            loc = f"{config.site_url}/keywords/{file_name}"
            lines.append(sitemap_entry(loc, taxonomy_index.get_keyword_lastmod(key, value)))

    # Item pages
    for item in items:
        lastmod_date = item.get('lastMod', item['datePublished'])
        item_file = item['folder'] + ".html"
        loc = f"{config.site_url}/{item['folder']}/{item_file}"
        lines.append(sitemap_entry(loc, lastmod_date))

    # Collection pages
    for collection in collections:
        lastmod_date = collection.get('lastMod', collection.get('datePublished', '2025-01-01'))
        collection_file = collection['folder'] + ".html"
        loc = f"{config.site_url}/collections/{collection_file}"
        lines.append(sitemap_entry(loc, lastmod_date))

    lines.append('\n</urlset>')
    return '\n'.join(lines)