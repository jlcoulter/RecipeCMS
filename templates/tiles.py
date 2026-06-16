"""Reusable tile components - replaces html_recipe_blocks.py."""

from .page_layout import get_footer
from ..lib.date_helpers import iso8601_to_human_readable


def render_item_tile(item, config, formatter, description=""):
    """Render an item tile card (replaces return_recipe_tile)."""
    item_link = formatter.format_link(f"{config.site_url}/{item['folder']}/{item['folder']}.html")
    image_link = f"{config.site_url}/{item['folder']}/{item['image'][0]}"

    extra = ""
    if description != "":
        extra = f'<p class="subtitle">{description}</p>'

    cuisine = item['recipeCuisine'] if not isinstance(item['recipeCuisine'], list) else item['recipeCuisine'][0]
    category = item['recipeCategory'] if not isinstance(item['recipeCategory'], list) else item['recipeCategory'][0]

    return f"""
        <div class="recipeTile border">
            <a href="{item_link}">
                <div class="innerTile">
                    <img alt="{item['name']}" src="{image_link}"></img>
                    <p class="title">{item['name']}</p>
                    <p class="subtitle">{cuisine} {category}</p>
                    <p class="subtitle">Time: {iso8601_to_human_readable(item['totalTime'])}</p>
                    {extra}
                </div>
            </a>
        </div>
        """


def render_collection_tile(collection, config, formatter, get_item_func):
    """Render a collection tile card (replaces return_listacle_tile)."""
    collection_link = formatter.format_link(f"{config.site_url}/collections/{collection['folder']}.html")
    image_link = f"{config.site_url}/{collection['image']}/{collection['image']}_0.jpg"

    collection_items = ""
    for recipe in collection.get('recipes', []):
        item = get_item_func(recipe['folder'])
        if item:
            collection_items += f'<div class="keywords border" style="background-color: unset;"><p>{item["name"]}</p></div>'

    return f"""
        <div class="recipeTile border">
            <a href="{collection_link}">
                <div class="innerTile">
                    <img alt="{collection['name']}" src="{image_link}"></img>
                    <p class="title">{collection['name']}</p>
                    <p class="subtitle">{collection['description']}</p>
                    <div class="keywordContainer" style="padding: 1rem 1rem 0 1rem;">
                    {collection_items}
                    </div>
                </div>
            </a>
        </div>
        """


def render_keyword_section(taxonomy_index, config, formatter, style_attr="", limit=20):
    """Render keyword sections for all taxonomies (replaces return_keyword_setion)."""
    keyword_section = ""
    keyword_section += '<div class="keywordSection">'

    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        label = taxonomy['label']
        sorted_map = taxonomy_index.get_sorted_map(key)
        if not sorted_map:
            continue

        keyword_section += f'<div {style_attr} class="keywordBlock border">'
        keyword_section += f'<h1>{config.item_name_plural} by {label}</h1>'
        keyword_section += '<div class="keywordContainer">'
        outputs = 0
        for value, items in sorted_map.items():
            file_name = value.lower().replace(' ', '_')
            link = formatter.format_link(f"{config.site_url}/keywords/{file_name}.html")
            keyword_section += f'<div class="keywords border"><a href="{link}"><p>{value} ({len(items)})</p></a></div>'
            outputs += 1
            if outputs == limit:
                break
        keyword_section += '</div>'
        keyword_section += '</div>'

    keyword_section += '</div>'
    return keyword_section


def render_basic_stats(stat_map, name, title, config, formatter):
    """Render a stats block for a taxonomy map (replaces return_basic_stats)."""
    return_string = ""

    single_items = 0
    shortest_item = "aaaaaaaaaaaaaaa"
    longest_item = "a"
    most_common_item = ["", 0]
    for k, v in stat_map.items():
        if len(v) < 2:
            single_items += 1
        if len(k) < len(shortest_item):
            shortest_item = k
        if len(k) > len(longest_item):
            longest_item = k
        if len(v) > most_common_item[1]:
            most_common_item[0] = k
            most_common_item[1] = len(v)

    return_string += f'<div class="keywordBlock border">'
    return_string += f'<h1 class="">{title}</h1>'
    return_string += f'<div class="keywordContainer">'
    return_string += f'<div class="keywords border"><p>{len(stat_map)} {name}</p></div>'
    return_string += f'<div class="keywords border"><p>{single_items} {name} With 1 {config.item_name}</p></div>'
    return_string += f'<div class="keywords border"><a href="{formatter.get_keyword_link(shortest_item)}"><p>Min Name: {shortest_item}</p></a></div>'
    return_string += f'<div class="keywords border"><a href="{formatter.get_keyword_link(longest_item)}"><p>Max Name: {longest_item}</p></a></div>'
    return_string += f'<div class="keywords border"><a href="{formatter.get_keyword_link(most_common_item[0])}"><p>Most Common: {most_common_item[0]} ({most_common_item[1]})</p></a></div>'
    return_string += f'</div>'
    return_string += f'</div>'

    return return_string


def render_shared_note_html(note_folder, item_folder, shared_notes, shared_note_map, config, formatter):
    """Render shared notes HTML (replaces return_shared_note_html)."""
    note_data = shared_notes.get(note_folder)
    if not note_data:
        return ""

    html = ""
    html += f'<div style="min-width: fit-content;" class="recipeComponent border">'
    html += f'<h2 class="removeOffsetTop">{note_data["description"]}</h2>'
    html += '<ul>'
    for note in note_data.get('notes', []):
        html += f'<li>{note}</li>'
    html += '</ul>'

    html += f'<p class="removeOffsetHeight">Other {config.item_name_plural.lower()} sharing these notes:</p>'
    html += '<div class="keywordContainer">'
    for item in shared_note_map.get(note_folder, []):
        if item_folder != item['folder']:
            html += f'<div class="keywords border"><a href="{formatter.get_item_link(item["folder"])}"><p>{item["name"]}</p></a></div>'
    html += '</div>'
    html += '</div>'

    return html


def render_page_numbers(index, num_chunks_minus_1, config, formatter):
    """Render pagination controls (replaces return_page_numbers)."""
    page_string = ""
    pages = ""
    num_chunks = num_chunks_minus_1 + 1

    for i in range(num_chunks):
        is_current_page = (i == index)
        style = ' style="text-decoration: underline; background-color: light-dark(var(--light-recipe-background), var(--dark-recipe-background));"' if is_current_page else ""
        page_num_display = str(i + 1)

        if i == 0:
            link = formatter.format_link(f"{config.site_url}/index.html")
        else:
            link = formatter.format_link(f"{config.site_url}/index{str(i)}.html")
        pages += f'<div class="keywords border"><a href="{link}"><p{style}>{page_num_display}</p></a></div>'

    prev_link_html = ""
    next_link_html = ""
    if index > 0:
        prev_page_index = index - 1
    else:
        prev_page_index = str(index) + "#"
    prev_link = formatter.format_link(f"{config.site_url}/index.html" if prev_page_index == 0 else f"{config.site_url}/index{prev_page_index}.html")
    prev_link_html = f'<div class="keywords border"><a href="{prev_link}"><p>&lt;--</p></a></div>'
    if index < num_chunks_minus_1:
        next_page_index = index + 1
    else:
        next_page_index = str(index) + "#"
    next_link = formatter.format_link(f"{config.site_url}/index{next_page_index}.html")
    next_link_html = f'<div class="keywords border"><a href="{next_link}"><p>--&gt;</p></a></div>'

    page_string += '<div class="keywordContainer offsetLeftEight">'
    page_string += prev_link_html
    page_string += pages
    page_string += next_link_html
    page_string += '</div>'

    return page_string