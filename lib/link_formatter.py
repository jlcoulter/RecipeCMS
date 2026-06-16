"""URL formatting logic, replacing link_helpers.py."""


class LinkFormatter:
    """Formats URLs based on site config. Replaces global-dependent link_helpers."""

    def __init__(self, config):
        self.config = config

    def format_link(self, link):
        """Remove .html extension when config says so."""
        if self.config.remove_html_extension:
            root_index_link = f"{self.config.site_url}/index.html"
            if link == root_index_link:
                return self.config.site_url
            if link.endswith('/index.html'):
                if link.split('/')[-1] == 'index.html':
                    return link[:-10]
            if link.endswith('.html'):
                return link[:-5]
        return link

    def get_keyword_link(self, keyword):
        """Get the URL for a keyword/taxonomy value page."""
        keyword_slug = keyword.lower().replace(' ', '_')
        keyword_link = self.format_link(f"{self.config.site_url}/keywords/{keyword_slug}.html")
        return keyword_link

    def get_item_link(self, item_folder):
        """Get the URL for an item detail page by folder name."""
        item_link = self.format_link(f"{self.config.site_url}/{item_folder}/{item_folder}.html")
        return item_link

    def get_item_link_by_name(self, item_name):
        """Get the URL for an item detail page by display name (slugified)."""
        slug = item_name.lower().replace(' ', '_')
        return self.format_link(f"{self.config.site_url}/{slug}/{slug}.html")