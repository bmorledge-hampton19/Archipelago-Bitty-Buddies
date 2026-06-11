from typing import NamedTuple

from worlds.AutoWorld import World
from .names import EventName, RegionName
from .locations import BittyBuddiesLocation
from .items import BittyBuddiesItem
from .rules import GenericCollectionRule, create_generic_final_goal_rule


class EventData(NamedTuple):
    """Data needed to create the event and its rules (besides name)"""
    region_name: RegionName | None = None
    rule: GenericCollectionRule | None = None


# Create a dictionary of EventData with names (as strings) as the keys.
event_data_dict: dict[EventName, EventData] = {
    EventName.VICTORY : EventData(
        RegionName.MENU,
        rule = create_generic_final_goal_rule()
    )
}


def create_events(world: World):
    """Creates all the events for the Bitty Buddies Archipelago, including setting their collection rules.
    (Right now, this is only the Victory event.)"""

    for name in event_data_dict:
        event_data = event_data_dict[name]
        region = world.get_region(event_data.region_name)

        region.add_event(
            name, name, location_type=BittyBuddiesLocation, item_type=BittyBuddiesItem
        )

        if event_data.rule:
            world.set_rule(world.get_location(name), event_data.rule(world.player, world.options))
