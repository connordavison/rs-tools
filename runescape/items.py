#!/usr/bin/env python

import cli.app
import json
import requests
import time

from . import config

CATEGORIES = {
    "Ammo": 1,
    "Arrows": 2,
    "Bolts": 3,
    "Construction materials": 4,
    "Construction projects": 5,
    "Cooking ingredients": 6,
    "Costumes": 7,
    "Crafting materials": 8,
    "Familiars": 9,
    "Farming produce": 10,
    "Fletching materials": 11,
    "Food and drink": 12,
    "Herblore materials": 13,
    "Hunting equipment": 14,
    "Hunting produce": 15,
    "Jewellery": 16,
    "Mage armour": 17,
    "Mage weapons": 18,
    "Melee armour - high level": 21,
    "Melee armour - low level": 19,
    "Melee armour - mid level": 20,
    "Melee weapons - high level": 24,
    "Melee weapons - low level": 22,
    "Melee weapons - mid level": 23,
    "Mining and smithing": 25,
    "Miscellaneous": 0,
    "Pocket items": 37,
    "Potions": 26,
    "Prayer armour": 27,
    "Prayer materials": 28,
    "Range armour": 29,
    "Range weapons": 30,
    "Runecrafting": 31,
    "Runes, Spells and Teleports": 32,
    "Seeds": 33,
    "Summoning scrolls": 34,
    "Tools and containers": 35,
    "Woodcutting product": 36,
}


def get_category_stats(id):
    """
    Retrieves a summary of the number of items in the given category in the
    following format:

        [{"letter":"#", "items": 0}, {"letter": "a", "items": 10}, ... ]

    A hash (#) indicates the group of items beginning with a number or other
    symbol.

    :param id: The category ID.
    """
    response = requests.get(
        config.get('runescape.com', 'ItemCategoryMetadata'),
        {'category': id}
    )

    response.raise_for_status()

    response = response.json()

    return response['alpha']


def get_category(id, letter, page):
    """
    Get the items in a category by its initial letter.

    :param id: The category ID.
    :param letter: The initial letter to search by.
    :param page: The page to retrieve. A page contains 12 items.
    """
    response = requests.get(
        config.get('runescape.com', 'ItemCategoryData'),
        {'category': id, 'alpha': letter, 'page': page}
    )

    response.raise_for_status()

    response = response.json()

    return response['items']


def get_item_data(id):
    """
    Get information about an item by its ID. To get price data, use
    :meth:`get_item_price_data`. 

    :param id: The item ID.
    """
    response = requests.get(
        config.get('runescape.com', 'ItemData'),
        {'item': id}
    )

    response.raise_for_status()

    response = response.json()

    return response['item']


def get_item_price_data(id):
    """
    Get price data about an item by its ID.

    :param id: The item ID.
    """
    response = requests.get(
        config.get('runescape.com', 'ItemPriceData') + str(id) + ".json"
    )

    response.raise_for_status()

    return response.json()


def generate_item_id_list(stream):
    """
    Generate an item list dump by querying RuneScape's APIs multiple times.
    This function takes a while.

    :param stream: An object implementing write().
    """
    items = []

    print("category;letter;name")

    for name, id in CATEGORIES.items():
        print("# Category: " + name + " (" + str(id) + ")")

        stats = get_category_stats(id)
        time.sleep(5)

        for stat in stats:
            letter = stat['letter']
            count = stat['items']

            print("## Letter: " + letter)

            if count is 0:
                continue

            # The number of pages in this category-letter group
            pages = int(count / 12) + 1

            for page in range(1, pages):
                print("### Page: " + str(page))
                items += get_category(id, letter, page)
                time.sleep(5)

    stream.write(json.dumps(items))

    return items

class ItemIDDumpApp(cli.app.CommandLineApp):
    """
    A CommandLineApp to create a JSON dump of items on RuneScape's Grand
    Exchange.
    """
    def main(self):
        with open(self.params.output_file, 'w') as f:
            generate_item_id_list(f)

    def setup(self):
        cli.app.CommandLineApp.setup(self)
        self.add_param('output_file', help="where to put the output", type=str)

class PriceApp(cli.app.CommandLineApp):
    """
    A CommandLineApp to access information about RuneScape items.
    """
    def main(self):
        print(get_item_price_data(self.params.item_id))

    def setup(self):
        cli.app.CommandLineApp.setup(self)
        
        self.add_param('item_id', help="the item to fetch", type=int)

        self.add_param(
            '-m', '--more',
            default=False, help="show entry summaries", action='store_true'
        )
