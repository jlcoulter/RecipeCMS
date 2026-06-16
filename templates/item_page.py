"""Item detail page template - the largest extraction from main.py."""

import random
from .page_layout import get_opener, get_header, get_footer
from .tiles import render_item_tile, render_keyword_section, render_shared_note_html
from lib.date_helpers import iso8601_to_human_readable


def generate_item_page(item, config, taxonomy_index, shared_notes, all_items, formatter, schema_gen):
    """Generate the full HTML for an item detail page."""
    html = ""

    # JSON-LD Schema
    html += get_opener(config, formatter)
    html += f'<script type="application/ld+json">{schema_gen.generate_item_schema(item, formatter)}</script>'
    html += f'<title>{item["name"]} - {config.site_name}</title>'
    html += f'<meta name="description" content="{item["description"]}">'
    html += get_header(config, formatter)

    html += '<div id="recipePage">'
    html += '<div id="recipe">'
    html += f'<h1 class="offset offsetHeight">{item["name"]}</h1>'

    html += f'<div id="recipeImg" class="border"><img alt="{item["name"]}" src="{config.site_url}/{item["folder"]}/{item["image"][0]}"></img></div>'

    html += '<div class="recipeContainer">'
    html += '<div style="min-width: fit-content;" class="recipeComponent border">'

    html += f'<p>{item["description"]}</p>'
    html += '<div class="keywordContainer">'
    html += '<div class="keywords border"><a onClick="sharePage();" href="#"><p>Share <i class="fa">&#xf1e0;</i></p></a></div>'
    html += f'<div class="keywords border" style="background-color: unset;"><p>Published: {item["datePublished"]}</p></div>'
    if item['datePublished'] != item['lastMod']:
        html += f'<div class="keywords border" style="background-color: unset;"><p>Last Modified: {item["lastMod"]}</p></div>'
    html += f'<div class="keywords border" style="background-color: unset;"><p>Creates: {item["recipeYield"]}</p></div>'
    html += '</div>'

    html += '</br>'
    html += '<div class="keywordContainer">'
    html += '<h3>Time:</h3>'

    if iso8601_to_human_readable(item['prepTime']) not in ("0 minutes", "0 hours"):
        html += f'<div class="keywords border" style="background-color: unset;"><p>Prep: {iso8601_to_human_readable(item["prepTime"])}</p></div>'
    if 'marinatingTime' in item:
        html += f'<div class="keywords border" style="background-color: unset;"><p>Marinate: {iso8601_to_human_readable(item["marinatingTime"])}</p></div>'
    if iso8601_to_human_readable(item['cookTime']) not in ("0 minutes", "0 hours"):
        html += f'<div class="keywords border" style="background-color: unset;"><p>Cook: {iso8601_to_human_readable(item["cookTime"])}</p></div>'
    html += f'<div class="keywords border" style="background-color: unset;"><p>Total: {iso8601_to_human_readable(item["totalTime"])}</p></div>'
    html += '</div>'

    # Dynamic taxonomy sections (equipment, diet, etc.)
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        if key in ('ingredientKeywords', 'recipeCuisine', 'recipeCategory'):
            continue  # These are handled in the notes/categorization area below
        raw_value = item.get(key)
        if raw_value is None:
            continue
        values = [raw_value] if not isinstance(raw_value, list) else raw_value
        if not values:
            continue
        html += '</br>'
        html += '<div class="keywordContainer">'
        html += f'<h3>{taxonomy["label"]}:</h3>'
        for value in values:
            link = formatter.format_link(f"{config.site_url}/keywords/{value.lower().replace(' ', '_')}.html")
            html += f'<div class="keywords border"><a href="{link}"><p>{value}</p></a></div>'
        html += '</div>'

    html += '</div>'

    # Ingredients Section (with cross-linking for ingredient taxonomy)
    ingredient_taxonomy = config.get_ingredient_taxonomy()
    ingredient_map = taxonomy_index.maps.get('ingredientKeywords', {}) if ingredient_taxonomy else {}

    html += '<div class="recipeComponent border">'
    html += '<h2 class="removeOffsetTop">Ingredients</h2>'
    html += '<ul>'
    for ingredient in item['recipeIngredient']:
        if ingredient == "":
            html += '</ul><ul>'
        elif ":" in ingredient:
            html += f'<p class="removeOffsetHeight">{ingredient}</p>'
        else:
            ingredient_linked = ingredient
            replacement = ""
            ingredient_text_to_replace = ""
            for ingre_name in ingredient_map:
                if ingre_name in ingredient_linked:
                    if len(ingre_name) > len(replacement):
                        replacement = ingre_name
                        ingredient_text_to_replace = ingre_name
                # Check for plurals
                if (ingre_name + "s") in ingredient_linked:
                    if len(ingre_name + "s") > len(replacement):
                        replacement = ingre_name
                        ingredient_text_to_replace = ingre_name + "s"
                if (ingre_name + "es") in ingredient_linked:
                    if len(ingre_name + "es") > len(replacement):
                        replacement = ingre_name
                        ingredient_text_to_replace = ingre_name + "es"
                if ingre_name.endswith("y"):
                    if (ingre_name[:-1] + "ies") in ingredient_linked:
                        if len(ingre_name[:-1] + "ies") > len(replacement):
                            replacement = ingre_name
                            ingredient_text_to_replace = ingre_name[:-1] + "ies"
                if "Leaf" in ingre_name:
                    leave_ingre_name = ingre_name.replace("Leaf", "Leaves")
                    if leave_ingre_name in ingredient_linked:
                        if len(leave_ingre_name) > len(replacement):
                            replacement = ingre_name
                            ingredient_text_to_replace = leave_ingre_name

            if replacement and ingredient_text_to_replace:
                link = formatter.format_link(f"{config.site_url}/keywords/{replacement.lower().replace(' ', '_')}.html")
                ingredient_linked = ingredient_linked.replace(ingredient_text_to_replace, f'<a href="{link}">{ingredient_text_to_replace}</a>')

            html += f'<li>{ingredient_linked}</li>'
    html += '</ul>'
    html += '</div>'

    # Steps Section
    html += '<div class="recipeComponent border">'
    html += '<h2 class="removeOffsetTop">Steps</h2>'
    html += '<ol>'
    for step in item['recipeInstructions']:
        html += f'<li><a href="#{str(step["url"])}"></a>{step["text"]}</li>'
    html += '</ol>'
    html += '</div>'

    # Notes Section with cuisine/category linking
    html += '<div style="min-width: fit-content;" class="recipeComponent border">'
    if 'sharedNotes' in item:
        html += f'<h2 class="removeOffsetTop">Notes for {item["name"]}</h2>'
    else:
        html += '<h2 class="removeOffsetTop">Notes</h2>'
    html += '<ul>'
    for note in item.get('notes', []):
        html += f'<li>{note}</li>'
    html += '</ul>'

    # Category linking
    cuisine_list = [item['recipeCuisine']] if not isinstance(item['recipeCuisine'], list) else item['recipeCuisine']
    category_list = [item['recipeCategory']] if not isinstance(item['recipeCategory'], list) else item['recipeCategory']

    html += '</br>'
    html += '<div class="keywordContainer">'
    html += '<h3>Categories:</h3>'
    category_map = taxonomy_index.maps.get('recipeCategory', {})
    for category_linked in category_list:
        category_to_replace = ""
        for category_name in category_map:
            if category_name in category_linked:
                if len(category_name) > len(category_to_replace):
                    category_to_replace = category_name
        link = formatter.format_link(f"{config.site_url}/keywords/{category_to_replace.lower().replace(' ', '_')}.html")
        category_linked = category_linked.replace(category_to_replace, f'<a href="{link}"><p>{category_to_replace}</p></a>')
        html += f'<div class="keywords border">{category_linked}</div>'
    html += '</div>'

    html += '</br>'
    html += '<div class="keywordContainer">'
    html += '<h3>Cuisines:</h3>'
    cuisine_map = taxonomy_index.maps.get('recipeCuisine', {})
    for cuisine_linked in cuisine_list:
        cuisine_to_replace = ""
        for cuisine_name in cuisine_map:
            if cuisine_name in cuisine_linked:
                if len(cuisine_name) > len(cuisine_to_replace):
                    cuisine_to_replace = cuisine_name
        link = formatter.format_link(f"{config.site_url}/keywords/{cuisine_to_replace.lower().replace(' ', '_')}.html")
        cuisine_linked = cuisine_linked.replace(cuisine_to_replace, f'<a href="{link}"><p>{cuisine_to_replace}</p></a>')
        html += f'<div class="keywords border">{cuisine_linked}</div>'
    html += '</div>'

    html += '</div>'

    # Shared notes
    if 'sharedNotes' in item:
        for note_name in item['sharedNotes']:
            html += render_shared_note_html(note_name, item['folder'], shared_notes, taxonomy_index.shared_note_map, config, formatter)

    html += '</div>'  # Close recipeContainer
    html += '</div>'  # Close recipe

    # Sidecar Section
    html += '<div id="recipeSidecar">'
    if 'relatedRecipes' in item:
        html += f'<h1 class="offset removeOffsetHeight">Related {config.item_name_plural}</h1>'
        html += '<div class="recipeContainer">'
        for related_recipe in item['relatedRecipes']:
            related_item = _get_item_by_folder(all_items, related_recipe)
            if related_item:
                html += render_item_tile(related_item, config, formatter)

        html += '</div>'

        if len(item['relatedRecipes']) < 3:
            html += f'<h1 class="offset">Other {config.item_name_plural}</h1>'
            html += '<div class="recipeContainer">'
            printed_items = {item['name']}
            for _ in range(4):
                random_item = random.choice(all_items)
                if random_item['name'] not in printed_items:
                    html += render_item_tile(random_item, config, formatter)
                    printed_items.add(random_item['name'])
            html += '</div>'
    else:
        html += f'<h1 class="offset removeOffsetHeight">Other {config.item_name_plural}</h1>'
        html += '<div class="recipeContainer">'
        printed_items = {item['name']}
        for _ in range(4):
            random_item = random.choice(all_items)
            if random_item['name'] not in printed_items:
                html += render_item_tile(random_item, config, formatter)
                printed_items.add(random_item['name'])
        html += '</div>'

    html += render_keyword_section(taxonomy_index, config, formatter, 'style="min-width: fit-content;"', 20)
    html += '</div>'
    html += '</div>'

    html += get_footer(config, formatter)

    return html


def _get_item_by_folder(all_items, folder):
    """Look up an item by its folder name."""
    for item in all_items:
        if item['folder'] == folder:
            return item
    return None