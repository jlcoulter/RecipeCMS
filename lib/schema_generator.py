"""JSON-LD schema generation for structured data."""

import copy
import json


class SchemaGenerator:
    """Generates JSON-LD structured data for item pages, index pages, and keyword pages."""

    def __init__(self, config):
        self.config = config

    def generate_item_schema(self, item, formatter):
        """Generate JSON-LD schema for an item detail page."""
        schema = copy.deepcopy(item)
        schema_type = self.config.schema_config.get('type', 'Recipe')
        context = self.config.schema_config.get('context', 'https://schema.org/')

        schema['@context'] = context
        schema['@type'] = schema_type

        # Filter out empty ingredients
        schema['recipeIngredient'] = []
        for ingredient in item.get('recipeIngredient', []):
            if ingredient != "" and ":" not in ingredient:
                schema['recipeIngredient'].append(ingredient)

        # Format instructions as HowToStep
        schema['recipeInstructions'] = []
        for step in item.get('recipeInstructions', []):
            base_url = f"{self.config.site_url}/{item['folder']}/{item['folder']}.html"
            formatted_base_url = formatter.format_link(base_url)
            schema['recipeInstructions'].append({
                "@type": "HowToStep",
                "name": step['name'],
                "url": f"{formatted_base_url}#{step['url']}",
                "text": step['text']
            })

        # Format image URLs
        schema['image'] = []
        for image in item.get('image', []):
            schema['image'].append(f"{self.config.site_url}/{item['folder']}/{image}")

        # Normalize cuisine/category to single values for schema
        cuisine_list = [item['recipeCuisine']] if not isinstance(item['recipeCuisine'], list) else item['recipeCuisine']
        category_list = [item['recipeCategory']] if not isinstance(item['recipeCategory'], list) else item['recipeCategory']
        schema['recipeCuisine'] = cuisine_list[0]
        schema['recipeCategory'] = category_list[0]

        # Diet mapping
        if 'diet' in item:
            diet_mapping = self.config.schema_config.get('diet_mapping', {})
            schema['suitableForDiet'] = []
            for diet in item['diet']:
                mapped = diet_mapping.get(diet)
                if mapped:
                    schema['suitableForDiet'].append(mapped)
                elif diet in ["Diabetic", "Gluten Free", "Halal", "Hindu", "Kosher",
                              "Low Calorie", "Low Fat", "Low Lactose", "Low Salt",
                              "Vegan", "Vegetarian"]:
                    schema['suitableForDiet'].append(diet.replace(" ", "") + "Diet")

        return json.dumps(schema)

    def generate_item_list_schema(self, items, formatter):
        """Generate ItemList JSON-LD schema for index/collection pages."""
        item_list = []
        position = 1
        for item in items:
            base_url = f"{self.config.site_url}/{item['folder']}/{item['folder']}.html"
            formatted_url = formatter.format_link(base_url)
            item_list.append({
                "@type": "ListItem",
                "position": position,
                "url": formatted_url
            })
            position += 1

        return json.dumps(item_list)

    def generate_collection_item_list_schema(self, collection, formatter):
        """Generate ItemList JSON-LD schema for a collection page."""
        item_list = []
        position = 1
        for recipe in collection.get('recipes', []):
            base_url = f"{self.config.site_url}/{recipe['folder']}/{recipe['folder']}.html"
            formatted_url = formatter.format_link(base_url)
            item_list.append({
                "@type": "ListItem",
                "position": position,
                "url": formatted_url
            })
            position += 1

        return json.dumps(item_list)

    def generate_collection_index_schema(self, collections, formatter):
        """Generate ItemList JSON-LD schema for the collections index page."""
        item_list = []
        position = 1
        for collection in collections:
            base_url = f"{self.config.site_url}/collections/{collection['folder']}.html"
            formatted_url = formatter.format_link(base_url)
            item_list.append({
                "@type": "ListItem",
                "position": position,
                "url": formatted_url
            })
            position += 1

        return json.dumps(item_list)