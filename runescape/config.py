"""
Configuration helper for rs-tools.
"""

__config__ = {
    "runescape.com": {
        "AdventurersLog": "http://services.runescape.com/m=adventurers-log/a=13/rssfeed",
        "Highscores": "http://hiscore.runescape.com/index_lite.ws",
        "News": "http://services.runescape.com/m=news/latest_news.rss",
        "ItemCategoryData": "http://services.runescape.com/m=itemdb_rs/api/catalogue/items.json",
        "ItemCategoryMetadata": "http://services.runescape.com/m=itemdb_rs/api/catalogue/category.json",
        "ItemData": "http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json",
        "ItemPriceData": "http://services.runescape.com/m=itemdb_rs/api/graph/"
    },

    "runetracker.org": { "Update": "http://runetracker.org/updateUserJS.php" }
}

def get(*keys):
    """
    Get the configuration value for the given key list. If the list doesn't
    point to a particular value, the configuration for that section will be
    returned.

    :param *keys: A variable amount of keys to follow.
    """
    value = __config__

    for key in keys:
        value = value[key]

    return value
