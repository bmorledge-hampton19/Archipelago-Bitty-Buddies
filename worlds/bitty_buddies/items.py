from typing import NamedTuple

from BaseClasses import Item, ItemClassification
from .names import ItemName, LEVEL_UP_NAMES, BONUS_SCORE_NAMES


class BittyBuddiesItem(Item):
    game = "Bitty Buddies"

class ItemData(NamedTuple):
    """Data needed to create the archipelago items (besides name)"""
    id: int | None = None
    classification: ItemClassification = ItemClassification.filler

# Create a dictionary of ItemData with names as the keys.
item_data_dict: dict[ItemName, ItemData] = {}
base_id = 1
for name in ItemName:
    id = len(item_data_dict) + base_id
    classification: ItemClassification
    if name in LEVEL_UP_NAMES: classification = ItemClassification.progression
    elif name == ItemName.BUDDY_POWER: classification = ItemClassification.progression | ItemClassification.useful
    elif name in BONUS_SCORE_NAMES: classification = ItemClassification.progression_deprioritized_skip_balancing
    else: classification = ItemClassification.filler
    item_data_dict[name] = ItemData(id, classification)
