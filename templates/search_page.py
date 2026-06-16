"""Search page template."""

from .page_layout import get_opener, get_header, get_footer


def generate_search_page(config, taxonomy_index, formatter):
    """Generate the search page HTML."""
    html = ""
    html += get_opener(config, formatter)
    html += f'<title>Search - {config.site_name}</title>'
    html += f'<meta name="description" content="Search {config.item_name_plural.lower()} and find what you\'re looking for using keywords">'
    html += f'<script type="text/javascript" src="{config.site_url}/search.js"></script>'
    html += get_header(config, formatter)

    html += '<div class="offset offsetHeight border" id="searchHead">'
    html += '<h1>Search</h1>'
    html += f'<h3>Enter ingredients, {config.item_name_plural.lower()}, cuisines or categories below to start searching. You can combine search terms by clicking the + to add things as a filter.</h3>'
    html += '<input onkeyup="search()" class="keywords border offsetHeight" id="searchInput" type="text" placeholder="Search..."></input>'
    html += '<h3>Filters</h3>'
    html += '<div class="keywordContainer" id="filters">'
    html += '<div class="keywords border"><p>No Filters Selected</p></div>'
    html += '</div>'
    html += '</div>'

    html += '<div class="offset border" id="searchBase">'
    html += '<h1>Search Results</h1>'
    html += f'<h3>{config.item_name_plural}</h3>'
    html += '<div class="keywordContainer" id="itemResults">'
    html += '<div class="keywords border"><p>No Results</p></div>'
    html += '</div>'

    # Dynamic taxonomy result sections
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        label = taxonomy['label']
        section_id = f"{key}Results"
        html += f'<h3>{label}</h3>'
        html += f'<div class="keywordContainer" id="{section_id}">'
        html += '<div class="keywords border"><p>No Results</p></div>'
        html += '</div>'

    html += '</div>'

    html += get_footer(config, formatter)

    return html