"""Statistics computation for the about page."""

import math
from .date_helpers import iso8601_to_seconds


def compute_stats(items, taxonomy_index, config):
    """Compute various statistics about the items for the about page.
    Returns a dict of stat categories."""
    if not items:
        return {}

    stats = {}

    # Item stats
    most_ingredient_item = ["", 0]
    least_ingredient_item = ["", 20]
    most_step_item = ["", 0]
    least_step_item = ["", 20]
    most_equipment_item = ["", 0]
    shortest_item = ["", 999999999]
    longest_item = ["", 0]
    total_ingredients = 0
    total_steps = 0
    total_seconds = 0

    for item in items:
        total_ingredients += len(item.get('recipeIngredient', []))
        total_steps += len(item.get('recipeInstructions', []))
        total_seconds += iso8601_to_seconds(item.get('totalTime', 'PT0S'))

        if len(item.get('recipeIngredient', [])) > most_ingredient_item[1]:
            most_ingredient_item = [item['name'], len(item['recipeIngredient'])]
        if len(item.get('recipeIngredient', [])) < least_ingredient_item[1]:
            least_ingredient_item = [item['name'], len(item['recipeIngredient'])]
        if len(item.get('recipeInstructions', [])) > most_step_item[1]:
            most_step_item = [item['name'], len(item['recipeInstructions'])]
        if len(item.get('recipeInstructions', [])) < least_step_item[1]:
            least_step_item = [item['name'], len(item['recipeInstructions'])]
        if 'equipment' in item:
            if len(item['equipment']) > most_equipment_item[1]:
                most_equipment_item = [item['name'], len(item['equipment'])]
        if iso8601_to_seconds(item.get('totalTime', 'PT0S')) < shortest_item[1]:
            shortest_item = [item['name'], iso8601_to_seconds(item.get('totalTime', 'PT0S'))]
        if iso8601_to_seconds(item.get('totalTime', 'PT0S')) > longest_item[1]:
            longest_item = [item['name'], iso8601_to_seconds(item.get('totalTime', 'PT0S'))]

    stats['item_stats'] = {
        'total': len(items),
        'most_ingredients': most_ingredient_item,
        'least_ingredients': least_ingredient_item,
        'avg_ingredients': math.floor(total_ingredients / len(items)),
        'most_steps': most_step_item,
        'least_steps': least_step_item,
        'avg_steps': math.floor(total_steps / len(items)),
        'most_equipment': most_equipment_item,
        'longest_duration': longest_item,
        'shortest_duration': shortest_item,
        'avg_duration_minutes': math.floor((total_seconds / 60) / len(items)),
    }

    # Per-taxonomy stats (replaces return_basic_stats for each map)
    stats['taxonomy_stats'] = {}
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        stat_map = taxonomy_index.maps.get(key, {})
        if not stat_map:
            continue

        single_items = 0
        shortest_name = "aaaaaaaaaaaaaaa"
        longest_name = "a"
        most_common = ["", 0]
        for k, v in stat_map.items():
            if len(v) < 2:
                single_items += 1
            if len(k) < len(shortest_name):
                shortest_name = k
            if len(k) > len(longest_name):
                longest_name = k
            if len(v) > most_common[1]:
                most_common = [k, len(v)]

        stats['taxonomy_stats'][key] = {
            'total': len(stat_map),
            'single_items': single_items,
            'shortest_name': shortest_name,
            'longest_name': longest_name,
            'most_common': most_common,
        }

    return stats