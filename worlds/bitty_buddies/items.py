from enum import Enum
from typing import List, Dict, NamedTuple

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World


class BittyBuddiesItem(Item):
    game = "Bitty Buddies"

class Name(Enum):
    """Static item names to prevent string mismatches."""
    BUD_LEVEL_UP = "Bud Progressive Level"
    BIFF_LEVEL_UP = "Biff Progressive Level"
    BENSON_LEVEL_UP = "Benson Progressive Level"
    BRIE_LEVEL_UP = "Brie Progressive Level"
    BAZZ_LEVEL_UP = "Bazz Progressive Level"

    BUDDY_POWER = "Buddy Power Progressive"

    BUD_SCORE = "Bud Score Bonus"
    BIFF_SCORE = "Biff Score Bonus"
    BENSON_SCORE = "Benson Score Bonus"
    BRIE_SCORE = "Brie Score Bonus"
    BAZZ_SCORE = "Bazz Score Bonus"

# Group together related item names.
LEVEL_UP_NAMES: List[Name] = [
    Name.BUD_LEVEL_UP, Name.BIFF_LEVEL_UP, Name.BENSON_LEVEL_UP, Name.BRIE_LEVEL_UP, Name.BAZZ_LEVEL_UP
]
SCORE_NAMES: List[Name] = [
    Name.BUD_SCORE, Name.BIFF_SCORE, Name.BENSON_SCORE, Name.BRIE_SCORE, Name.BAZZ_SCORE
]

class ItemData(NamedTuple):
    """Data needed to create the archipelago items (besides name)"""
    id: int | None = None
    classification: ItemClassification

# Create a dictionary of ItemData with names (as strings) as the keys.
item_data_dict: Dict[str, ItemData] = {}
for name in Name:
    id = len(item_data_dict) + 1
    classification: ItemClassification
    if name in LEVEL_UP_NAMES: classification = ItemClassification.progression
    elif name == Name.BUDDY_POWER: classification = ItemClassification.progression | ItemClassification.useful
    elif name in SCORE_NAMES: classification = ItemClassification.filler
    else: classification = ItemClassification.filler
    item_data_dict[name.value] = ItemData(id, classification)


def create_item(world: World, name: Name | str) -> BittyBuddiesItem:
    """Returns a BittyBuddiesItem for the given world and item name (either as an enum or string)"""
    item_data = item_data_dict[name.value] if isinstance(name, Name) else item_data_dict[name]
    return BittyBuddiesItem(name.value, item_data.classification, item_data.id, world.player)

def create_progression_items(world: World) -> List[BittyBuddiesItem]:
    """Returns the necessary progression items for a given world, including a precollected starting buddy."""
    progression_items: List[BittyBuddiesItem] = []

    starting_buddy = world.random.choice(LEVEL_UP_NAMES)
    world.push_precollected(create_item(world,starting_buddy))
    for level_up in LEVEL_UP_NAMES:
        quantity = 4 if level_up == starting_buddy else 5
        progression_items += [create_item(world, level_up) for _ in range(quantity)]

    world.push_precollected(create_item(world,Name.BUDDY_POWER))
    progression_items += [create_item(world, Name.BUDDY_POWER) for _ in range(4)]

    return progression_items

def get_filler_item_name(world: World) -> str:
    """Returns a random filler name for the given world."""
    return world.random.choice(SCORE_NAMES).value

def create_filler(world: World) -> BittyBuddiesItem:
    """Returns a random filler BittyBuddiesItem (a score bonus) for the given world."""
    return create_item(world, get_filler_item_name(world))

def create_items(world: World):
    """Combines the above methods to populate the world with the necessary items."""
    progression_items: List[BittyBuddiesItem] = create_progression_items(world)

    filler_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(progression_items)
    filler_items = [world.create_filler() for _ in range(filler_count)]

    world.multiworld.itempool += progression_items + filler_items