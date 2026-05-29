from typing import List, NamedTuple, Dict, Callable
from enum import Enum

from BaseClasses import Region, CollectionRule
from worlds.AutoWorld import World
from . import rules


class Name(Enum):
    """Static region names to prevent string mismatches."""
    MENU = "Menu"

class Connection(NamedTuple):
    """Describes a connection to another region and the rule necessary to traverse that connection"""
    to: str
    rule: CollectionRule = None

class RegionData(NamedTuple):
    """Data needed to create the region and its connections (besides name)"""
    connections: List[Connection] = []
    hint: str | None = None

# Create a dictionary of RegionData with names (as strings) as the keys.
region_data_dict: Dict[str, RegionData] = {
    Name.MENU.value : RegionData()
}


def create_regions(world: World):
    """Creates (and connects) all the regions for the bitty buddies archipelago."""
    # Initialize all the regions.
    regions: Dict[str,Region] = {}
    for region_name in region_data_dict:
        regions[region_name] = Region(region_name, world.player, world.multiworld, region_data_dict[region_name].hint)
    
    # Establish connections.
    for region in regions.values():
        for connection in region_data_dict[region.name].connections:
            region.connect(regions[connection.to], f"{region.name} to {connection.to}", connection.rule)

    world.multiworld.regions += regions.values()
