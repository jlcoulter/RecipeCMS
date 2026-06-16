"""Dynamic taxonomy index builder - replaces all hardcoded maps."""

import os


class TaxonomyIndex:
    """Builds and holds taxonomy maps dynamically from config.

    Each taxonomy has:
      - map: {value_string: [item_dict, ...]}  -- items indexed by taxonomy value
      - values: [value_string, ...]            -- flat list of all values (for search JS)
    """

    def __init__(self, config):
        self.config = config
        self.maps = {}    # key -> {value -> [items]}
        self.values = {}  # key -> [value_strings]

    def build(self, items):
        """Build all taxonomy maps from the loaded items."""
        for taxonomy in self.config.taxonomies:
            key = taxonomy['key']
            self.maps[key] = {}
            self.values[key] = []

        for item in items:
            for taxonomy in self.config.taxonomies:
                key = taxonomy['key']
                raw_value = item.get(key)
                if raw_value is None:
                    continue

                # Normalize to list
                values = [raw_value] if not isinstance(raw_value, list) else raw_value

                for value in values:
                    if value not in self.maps[key]:
                        self.maps[key][value] = []
                        self.values[key].append(value)
                    self.maps[key][value].append(item)

        # Build shared note map from items
        self.shared_note_map = {}
        for item in items:
            if 'sharedNotes' in item:
                for note_folder in item['sharedNotes']:
                    if note_folder not in self.shared_note_map:
                        self.shared_note_map[note_folder] = []
                    self.shared_note_map[note_folder].append(item)

    def get_sorted_map(self, key):
        """Return map for a taxonomy key, sorted by item count descending."""
        if key not in self.maps:
            return {}
        return dict(sorted(self.maps[key].items(), key=lambda x: len(x[1]), reverse=True))

    def get_keyword_lastmod(self, key, value):
        """Get the most recent datePublished for items in a taxonomy value."""
        items = self.maps.get(key, {}).get(value, [])
        latest = "19900101"
        result = ""
        for item in items:
            date = item['datePublished'].replace("-", "")
            if int(date) > int(latest):
                latest = date
                result = item['datePublished']
        return result

    def get_all_keyword_links(self, formatter, limit=99999):
        """Generate keyword link data for all taxonomies.
        Returns a dict of taxonomy_key -> list of (value, count, link) tuples."""
        result = {}
        for taxonomy in self.config.taxonomies:
            key = taxonomy['key']
            sorted_map = self.get_sorted_map(key)
            links = []
            count = 0
            for value, items in sorted_map.items():
                slug = value.lower().replace(' ', '_')
                link = formatter.format_link(f"{self.config.site_url}/keywords/{slug}.html")
                links.append((value, len(items), link))
                count += 1
                if count >= limit:
                    break
            result[key] = links
        return result

    def get_small_values(self, key):
        """Get flat list of taxonomy values for search JS (replaces small_*_map)."""
        return self.values.get(key, [])