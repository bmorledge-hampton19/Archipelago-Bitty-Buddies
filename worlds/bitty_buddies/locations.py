from typing import NamedTuple

from BaseClasses import Location
from .names import LocationName, CARTRIDGE_GOAL_SCORE_NAMES, RegionName
from .rules import (
    GenericCollectionRule, InclusionRule,
    create_generic_goal_score_rule, create_generic_buddy_power_rule,
    flat_tire_generic_collection_rule, flat_tire_inclusion_rule
)


class BittyBuddiesLocation(Location):
    game = "BittyBuddies"


class LocationData(NamedTuple):
    """Data needed to create the location and its rules (besides name)"""
    id: int | None = None
    region_name: RegionName | None = None
    collection_rule: GenericCollectionRule | None = None
    inclusion_rule: InclusionRule | None = None


# Create a dictionary of LocationData with names as the keys.
location_data_dict: dict[LocationName, LocationData] = {}
base_id = 1
def add_location_data(
    name: LocationName, region: RegionName = RegionName.MENU,
    collection_rule: GenericCollectionRule = None, inclusion_rule: InclusionRule = None
):
    location_data_dict[name] = LocationData(
        base_id+len(location_data_dict), region, collection_rule, inclusion_rule
    )

# Initialize each of the buddy level locations
for buddy in CARTRIDGE_GOAL_SCORE_NAMES:
    for i, name in enumerate(CARTRIDGE_GOAL_SCORE_NAMES[buddy]):
        add_location_data(name, collection_rule = create_generic_goal_score_rule(buddy, i+1))

# Initialize each of the buddy power locations
for i, name in enumerate([
    LocationName.ALL_BUDDIES_LEVEL_1, LocationName.ALL_BUDDIES_LEVEL_2, LocationName.ALL_BUDDIES_LEVEL_3,
    LocationName.ALL_BUDDIES_LEVEL_4
]):
    add_location_data(name, collection_rule = create_generic_buddy_power_rule(i+1))

# Initialize the flat tire location
add_location_data(
    LocationName.FLAT_TIRE, collection_rule = flat_tire_generic_collection_rule,
    inclusion_rule = flat_tire_inclusion_rule
)
