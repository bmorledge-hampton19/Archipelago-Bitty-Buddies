from typing import List
from . import items
from .options import MyGameOptions  # the options we defined earlier
from .items import BittyBuddiesItem, item_data_dict
from .locations import mygame_locations  # same as above
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification


class BittyBuddiesLocation(Location):
    game = "Bitty Buddies"


class BittyBuddiesWorld(World):
    """Help the Bitty Buddies reach their full potential as they work together to discover strengths they never knew they had!"""
    game = "Bitty Buddies"
    options_dataclass = MyGameOptions
    options: MyGameOptions 




    item_name_to_id = {name: data.id for name, data in item_data_dict.items()}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, base_id)}
    item_name_groups = {
        "Level Ups": {name.value for name in items.LEVEL_UP_NAMES},
        "Score Bonuses": {name.value for name in items.SCORE_NAMES},
    }

    def create_item(self, name: str) -> BittyBuddiesItem:
        return items.create_item(self, name)

    def create_filler(self) -> BittyBuddiesItem:
        return items.create_filler(self)

    def create_items(self) -> None:
        items.create_items(self)
