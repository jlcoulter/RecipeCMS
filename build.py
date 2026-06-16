#!/usr/bin/env python3
"""StaticCMS - A general-purpose static site generator.

Reads site_config.json, loads content from the content/ directory,
builds taxonomy indexes, and generates a complete static site in output/.
"""

import os
import sys
import json
import random
import shutil

from lib.config import SiteConfig
from lib.content_loader import ContentLoader
from lib.taxonomy import TaxonomyIndex
from lib.link_formatter import LinkFormatter
from lib.schema_generator import SchemaGenerator
from lib.stats import compute_stats
from lib.sitemap import generate_sitemap

from templates.page_layout import get_opener, get_header, get_footer
from templates.item_page import generate_item_page
from templates.collection_page import generate_collection_page, generate_collections_index
from templates.keyword_pages import generate_keyword_page, generate_all_keywords_page
from templates.index_page import generate_index_pages, generate_all_items_page
from templates.search_page import generate_search_page
from templates.about_page import generate_about_page
from templates.js_templates import generate_search_js, generate_random_js
from default_style import generate_css


def get_item_by_folder(all_items, folder):
    """Look up an item by its folder name."""
    for item in all_items:
        if item['folder'] == folder:
            return item
    return None


def main():
    # 1. Load config
    config_path = sys.argv[1] if len(sys.argv) > 1 else "site_config.json"
    config = SiteConfig(config_path)
    formatter = LinkFormatter(config)
    schema_gen = SchemaGenerator(config)

    # 2. Load content
    loader = ContentLoader(config)
    items = loader.load_items()
    collections = loader.load_collections()
    shared_notes = loader.load_shared_notes()

    # 3. Build taxonomy index
    taxonomy = TaxonomyIndex(config)
    taxonomy.build(items)

    # 4. Create output directories
    os.makedirs(config.output_dir, exist_ok=True)
    os.makedirs(config.keywords_path, exist_ok=True)
    os.makedirs(os.path.join(config.output_dir, 'items'), exist_ok=True)
    os.makedirs(os.path.join(config.output_dir, 'collections'), exist_ok=True)

    # 5. Copy static assets
    if os.path.exists(config.static_path):
        for file in os.listdir(config.static_path):
            src = os.path.join(config.static_path, file)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(config.output_dir, file))

    # 6. Generate CSS
    css = generate_css(config)
    with open(os.path.join(config.output_dir, 'style.css'), 'w') as f:
        f.write(css)

    # 7. Copy custom.css if present
    has_custom_css = os.path.exists('custom.css')
    if has_custom_css:
        shutil.copy('custom.css', os.path.join(config.output_dir, 'custom.css'))
    config.set_runtime_flag('has_custom_css', has_custom_css)

    # 8. Generate item pages
    for item in items:
        html = generate_item_page(item, config, taxonomy, shared_notes, items, formatter, schema_gen)
        item_output_dir = os.path.join(config.output_dir, 'items', item['folder'])
        os.makedirs(item_output_dir, exist_ok=True)
        with open(os.path.join(item_output_dir, item['folder'] + '.html'), 'w') as f:
            f.write(html)

        # Copy item images
        item_src_dir = os.path.join(config.items_path, item['folder'])
        if os.path.exists(item_src_dir):
            for img_file in os.listdir(item_src_dir):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    shutil.copy2(
                        os.path.join(item_src_dir, img_file),
                        os.path.join(item_output_dir, img_file)
                    )

    # 9. Generate collection pages
    for collection in collections:
        get_item_func = lambda folder: get_item_by_folder(items, folder)
        html = generate_collection_page(collection, config, formatter, get_item_func, schema_gen)
        with open(os.path.join(config.output_dir, 'collections', collection['folder'] + '.html'), 'w') as f:
            f.write(html)

    # 10. Generate keyword pages for all taxonomies
    for taxonomy_def in config.taxonomies:
        key = taxonomy_def['key']
        for value, value_items in taxonomy.maps.get(key, {}).items():
            html = generate_keyword_page(key, value, value_items, config, formatter, taxonomy, schema_gen)
            slug = value.lower().replace(' ', '_')
            with open(os.path.join(config.keywords_path, slug + '.html'), 'w') as f:
                f.write(html)

    # 11. Generate index pages (writes files itself, returns list of filenames)
    index_pages = generate_index_pages(items, config, taxonomy, formatter, schema_gen)

    # 12. Generate search JS
    # Build small_items for search JS
    small_items = []
    for item in items:
        cuisine_list = [item['recipeCuisine']] if not isinstance(item['recipeCuisine'], list) else item['recipeCuisine']
        category_list = [item['recipeCategory']] if not isinstance(item['recipeCategory'], list) else item['recipeCategory']
        small_items.append({
            "name": item['name'],
            "folder": item['folder'],
            "ingredientKeywords": item.get('ingredientKeywords', []),
            "recipeCategory": ", ".join(category_list),
            "recipeCuisine": ", ".join(cuisine_list)
        })

    search_js = generate_search_js(config, taxonomy, small_items)
    with open(os.path.join(config.output_dir, 'search.js'), 'w') as f:
        f.write(search_js)

    # 13. Generate random JS
    item_folders = [item['folder'] for item in items]
    random_js = generate_random_js(config, item_folders)
    with open(os.path.join(config.output_dir, 'random.js'), 'w') as f:
        f.write(random_js)

    # 14. Generate search page
    search_html = generate_search_page(config, taxonomy, formatter)
    with open(os.path.join(config.output_dir, 'search.html'), 'w') as f:
        f.write(search_html)

    # 15. Generate about page
    stats = compute_stats(items, taxonomy, config)
    about_html = generate_about_page(config, stats, taxonomy, formatter)
    with open(os.path.join(config.output_dir, 'about.html'), 'w') as f:
        f.write(about_html)

    # 16. Generate all-items page
    all_items_html = generate_all_items_page(items, config, formatter, schema_gen)
    with open(os.path.join(config.output_dir, 'all_items.html'), 'w') as f:
        f.write(all_items_html)

    # 17. Generate all-keywords page
    all_keywords_html = generate_all_keywords_page(config, taxonomy, formatter)
    with open(os.path.join(config.output_dir, 'all_keywords.html'), 'w') as f:
        f.write(all_keywords_html)

    # 18. Generate collections index page
    get_item_func = lambda folder: get_item_by_folder(items, folder)
    collections_html = generate_collections_index(collections, config, formatter, taxonomy, schema_gen)
    with open(os.path.join(config.output_dir, 'collections.html'), 'w') as f:
        f.write(collections_html)

    # 19. Generate sitemap
    sitemap_xml = generate_sitemap(config, items, taxonomy, collections, index_pages, formatter)
    with open(os.path.join(config.output_dir, 'sitemap.xml'), 'w') as f:
        f.write(sitemap_xml)

    # 20. Print summary
    for taxonomy_def in config.taxonomies:
        key = taxonomy_def['key']
        count = len(taxonomy.maps.get(key, {}))
        print(f"{count} {taxonomy_def['label'].lower()}")

    print(f"{len(collections)} collections")
    print(f"{len(items)} {config.item_name_plural.lower()}")
    print("Build complete.")


if __name__ == '__main__':
    main()