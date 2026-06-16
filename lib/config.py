"""Site configuration loader and validator."""

import json
import os


class SiteConfig:
    """Loads and validates site_config.json, replacing the old global_variables module."""

    def __init__(self, config_path="site_config.json"):
        with open(config_path, 'r') as f:
            data = json.load(f)

        self.site_name = data['site_name']
        self.site_url = data['site_url']
        self.site_description = data.get('site_description', '')
        self.item_name = data['item_name']
        self.item_name_plural = data['item_name_plural']
        self.content_dir = data.get('content_dir', 'content')
        self.output_dir = data.get('output_dir', 'output')
        self.remove_html_extension = data.get('remove_html_extension', True)
        self.custom_header_html = data.get('custom_header_html', '')
        self.about_text = data.get('about_text', '')
        self.items_per_page = data.get('items_per_page', 15)
        self.search_result_limits = data.get('search_result_limits', {})
        self.taxonomies = data.get('taxonomies', [])
        self.schema_config = data.get('schema', {})
        self.style = data.get('style', {})
        self.fonts = data.get('fonts', [])
        self.sitemap_static_dates = data.get('sitemap_static_dates', {})

        # Derived paths
        self.items_path = os.path.join(self.content_dir, 'items')
        self.collections_path = os.path.join(self.content_dir, 'collections')
        self.shared_notes_path = os.path.join(self.content_dir, 'shared_notes')
        self.keywords_path = os.path.join(self.output_dir, 'keywords')
        self.static_path = 'static'

    def get_taxonomy_by_key(self, key):
        """Look up a taxonomy definition by its key field."""
        for t in self.taxonomies:
            if t['key'] == key:
                return t
        return None

    def get_ingredient_taxonomy(self):
        """Find the taxonomy entry flagged as type 'ingredient'."""
        for t in self.taxonomies:
            if t.get('type') == 'ingredient':
                return t
        return None