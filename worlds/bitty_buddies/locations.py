from typing import NamedTuple

from BaseClasses import Location
from .names import (
    LocationName, RegionName, Buddy,
    CARTRIDGE_GOAL_SCORE_NAMES, SILLY_CHECK_NAMES, SKILL_CHECK_NAMES
)
from .rules import (
    GenericCollectionRule, InclusionRule,
    create_generic_goal_score_rule, create_generic_buddy_power_rule,
    create_generic_buddy_level_rule, silly_check_inclusion_rule, skill_check_inclusion_rule
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
) -> None:
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

# Initialize the silly check locations
for buddy in Buddy:
    add_location_data(
        SILLY_CHECK_NAMES[buddy], collection_rule = create_generic_buddy_level_rule(buddy),
        inclusion_rule = silly_check_inclusion_rule
    )

# Initialize the skill check locations
for buddy in Buddy:
    if buddy == Buddy.BUD: required_level = 4
    elif buddy == Buddy.BIFF: required_level = 4
    elif buddy == Buddy.BENSON: required_level = 1
    elif buddy == Buddy.BRIE: required_level = 4
    elif buddy == Buddy.BAZZ: required_level = 3
    add_location_data(
        SKILL_CHECK_NAMES[buddy],
        collection_rule = create_generic_buddy_level_rule(buddy, required_level),
        inclusion_rule = skill_check_inclusion_rule
    )
