"""Content loader - walks content directories and loads JSON data."""

import json
import os


class ContentLoader:
    """Loads items, collections, and shared notes from the content directory."""

    def __init__(self, config):
        self.config = config

    def load_items(self):
        """Walk content/items/ and load all item JSON files.
        Returns list of item dicts."""
        items = []
        if not os.path.exists(self.config.items_path):
            return items
        for root, _, files in os.walk(self.config.items_path):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        items.append(json.load(f))
        return items

    def load_collections(self):
        """Walk content/collections/ and load all collection JSON files.
        Returns list of collection dicts."""
        collections = []
        if not os.path.exists(self.config.collections_path):
            return collections
        for root, _, files in os.walk(self.config.collections_path):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        collections.append(json.load(f))
        return collections

    def load_shared_notes(self):
        """Walk content/shared_notes/ and load all shared notes JSON files.
        Returns dict keyed by folder name."""
        notes = {}
        if not os.path.exists(self.config.shared_notes_path):
            return notes
        for root, _, files in os.walk(self.config.shared_notes_path):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        notes[data['folder']] = data
        return notes