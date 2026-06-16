"""About page template."""

import math
from .page_layout import get_opener, get_header, get_footer
from .tiles import render_keyword_section, render_basic_stats


def generate_about_page(config, stats, taxonomy_index, formatter):
    """Generate the about page HTML."""
    html = ""
    html += get_opener(config, formatter)
    html += f'<title>About - {config.site_name}</title>'
    html += f'<meta name="description" content="The obligatory about page for {config.site_name}">'
    html += get_header(config, formatter)

    html += '<div id="about" class="">'
    html += '<h1 class="removeOffsetHeight offset">About</h1>'
    html += '<p class="removeOffsetTop offset">That obligatory about page</p>'

    # About text from config
    if config.about_text:
        html += config.about_text

    html += '<h1 class="removeOffsetTop removeOffsetHeight offset">Stats</h1>'
    html += '<p class="removeOffsetTop offset">Just some stats I wanted</p>'

    html += '<div class="keywordSection">'

    # Item stats
    item_stats = stats.get('item_stats', {})
    if item_stats:
        html += '<div class="keywordBlock border">'
        html += f'<h1 class="">{config.item_name} Stats</h1>'
        html += '<div class="keywordContainer">'
        html += f'<div class="keywords border"><p>{item_stats["total"]} {config.item_name_plural}</p></div>'

        if item_stats.get('most_ingredients'):
            name, count = item_stats['most_ingredients']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Min Ingredients: {name} ({count})</p></a></div>'
        html += f'<div class="keywords border"><p>AVG Ingredients: {item_stats.get("avg_ingredients", 0)}</p></div>'
        if item_stats.get('least_ingredients'):
            name, count = item_stats['least_ingredients']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Max Ingredients: {name} ({count})</p></a></div>'
        if item_stats.get('most_steps'):
            name, count = item_stats['most_steps']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Max Steps: {name} ({count})</p></a></div>'
        html += f'<div class="keywords border"><p>AVG Steps: {item_stats.get("avg_steps", 0)}</p></div>'
        if item_stats.get('least_steps'):
            name, count = item_stats['least_steps']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Min Steps: {name} ({count})</p></a></div>'
        if item_stats.get('most_equipment'):
            name, count = item_stats['most_equipment']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Most Equipment: {name} ({count})</p></a></div>'
        if item_stats.get('longest_duration'):
            name, seconds = item_stats['longest_duration']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Max Duration: {name} ({math.floor(seconds / 60)} Minutes)</p></a></div>'
        html += f'<div class="keywords border"><p>AVG Duration: {item_stats.get("avg_duration_minutes", 0)} Minutes</p></div>'
        if item_stats.get('shortest_duration'):
            name, seconds = item_stats['shortest_duration']
            html += f'<div class="keywords border"><a href="{formatter.get_item_link_by_name(name)}"><p>Min Duration: {name} ({math.floor(seconds / 60)} Minutes)</p></a></div>'

        html += '</div>'
        html += '</div>'

    # Per-taxonomy stats
    taxonomy_stats = stats.get('taxonomy_stats', {})
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        if key in taxonomy_stats:
            ts = taxonomy_stats[key]
            stat_map = taxonomy_index.maps.get(key, {})
            html += render_basic_stats(stat_map, taxonomy['label'], f'{taxonomy["label"]} Stats', config, formatter)

    html += '</div>'
    html += '</div>'

    html += render_keyword_section(taxonomy_index, config, formatter, "", 20)
    html += get_footer(config, formatter)

    return html