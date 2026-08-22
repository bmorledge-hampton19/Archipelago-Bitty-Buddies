from typing import Any

from BaseClasses import Region
from worlds.AutoWorld import World
from .names import BUDDY_POWER_LOCATION_NAMES, ItemName, LEVEL_UP_NAMES, BONUS_SCORE_NAMES
from .regions import region_data_dict
from .locations import BittyBuddiesLocation, location_data_dict
from .events import event_data_dict
from .items import BittyBuddiesItem, item_data_dict
from .rules import completion_rule
from .options import BittyBuddiesOptions
from .web_world import BittyBuddiesWebWorld


class BittyBuddiesWorld(World):
    """Help the Bitty Buddies reach their full potential as they work together to
    discover strengths they never knew they had!"""

    game = "Bitty Buddies"
    web = BittyBuddiesWebWorld()
    options_dataclass = BittyBuddiesOptions
    options: BittyBuddiesOptions


    location_name_to_id = {name.value: data.id for name, data in location_data_dict.items()}
    item_name_to_id = {name.value: data.id for name, data in item_data_dict.items()}
    item_name_groups = {
        "Level Ups": {name.value for name in LEVEL_UP_NAMES},
        "Score Bonuses": {name.value for name in BONUS_SCORE_NAMES},
    }

    starter_buddy: ItemName
    early_buddies: list[ItemName]


    def create_item(self, name: ItemName) -> BittyBuddiesItem:
        item_data = item_data_dict[name]
        return BittyBuddiesItem(name, item_data.classification, item_data.id, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(BONUS_SCORE_NAMES)

    def create_filler(self) -> BittyBuddiesItem:
        """Returns a random filler BittyBuddiesItem (a score bonus) for the given world."""
        return self.create_item(self.get_filler_item_name())


    def generate_early(self) -> None:
        # Set up some initial checks with more concrete logic for a less restrictive start.

        # Roll a random starter buddy.
        self.starter_buddy = self.random.choice(LEVEL_UP_NAMES)

        # Choose two other buddies to place in sphere 1.
        self.early_buddies = []
        for _ in range(2):
            early_buddy = self.random.choice(LEVEL_UP_NAMES)
            while early_buddy == self.starter_buddy or early_buddy in self.early_buddies:
                early_buddy = self.random.choice(LEVEL_UP_NAMES)
            self.early_buddies.append(early_buddy)


    def create_regions(self) -> None:
        # Initialize all the regions.
        regions: list[Region] = []
        for region_name in region_data_dict:
            regions.append(Region(region_name, self.player, self.multiworld, region_data_dict[region_name].hint))

        # Establish connections between regions, including entrance rules.
        for region in regions:
            for connection in region_data_dict[region.name].connections:
                connection_rule = connection.rule(self.player, self.options) if connection.rule else None
                region.connect(regions[connection.to], f"{region.name} to {connection.to}", connection_rule)

        # Add regions.
        self.multiworld.regions += regions

        # Create all the locations, and set their collection rules
        for name in location_data_dict:
            location_data = location_data_dict[name]

            # Exclude locations with inclusion rules that are not satisfied.
            if location_data.inclusion_rule and not location_data.inclusion_rule(self.options): continue

            region = self.get_region(location_data.region_name)
            location = BittyBuddiesLocation(self.player, name, location_data.id, region)
            region.locations.append(location)
            if location_data.collection_rule:
                self.set_rule(location, location_data.collection_rule(self.player, self.options))


        # Create all the events, and set their collection rules.
        # (Right now, this is only the Victory event.)
        for name in event_data_dict:
            event_data = event_data_dict[name]
            region = self.get_region(event_data.region_name)

            region.add_event(
                name, name, location_type=BittyBuddiesLocation, item_type=BittyBuddiesItem
            )

            if event_data.rule:
                self.set_rule(self.get_location(name), event_data.rule(self.player, self.options))


    def create_items(self) -> None:
        # Create the core progression items.
        progression_items: list[BittyBuddiesItem] = []
        waiting_on_prefill = 0

        for level_up in LEVEL_UP_NAMES:
            quantity: int
            if level_up == self.starter_buddy:
                quantity = 4
                self.push_precollected(self.create_item(self.starter_buddy))
            else:
                quantity = 5
            progression_items += [self.create_item(level_up) for _ in range(quantity)]

        self.push_precollected(self.create_item(ItemName.BUDDY_POWER))
        if self.options.randomize_buddy_power:
            progression_items += [self.create_item(ItemName.BUDDY_POWER) for _ in range(4)]
        else:
            waiting_on_prefill += 4

        # Add filler based on the number of remaining locations.
        filler_count = (
            len(self.multiworld.get_unfilled_locations(self.player)) - len(progression_items) - waiting_on_prefill
        )
        filler_items = [self.create_filler() for _ in range(filler_count)]

        self.multiworld.itempool += progression_items + filler_items

        # Make sure that the two other early buddies will be found in sphere 1.
        for early_buddy in self.early_buddies:
            self.multiworld.local_early_items[self.player][early_buddy.value] = 1


    def set_rules(self) -> None:
        # Entrance and location rules were already set in create_regions. We just need to set the completion rule.
        self.set_completion_rule(completion_rule)


    def get_pre_fill_items(self) -> list[BittyBuddiesItem]:
        # Returns items placed in pre_fill.
        pre_fill_items = []

        if not self.options.randomize_buddy_power:
            for _ in range(4): pre_fill_items.append(self.create_item(ItemName.BUDDY_POWER))

        return pre_fill_items

    def pre_fill(self) -> None:
        # If buddy power is not randomized, pre-fill the buddy power increases to the usual locations.
        if not self.options.randomize_buddy_power:
            for location_name in BUDDY_POWER_LOCATION_NAMES:
                buddy_power_item = self.create_item(ItemName.BUDDY_POWER)
                self.get_location(location_name).place_locked_item(buddy_power_item)


    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "cartridge_goal_scores" : self.options.cartridge_goal_scores.value,
            "logic_difficulty" : self.options.logic_difficulty.value,
            "final_goal_score" : self.options.final_goal_score.value,
            "silly_checks" : self.options.silly_checks.value,
            "skill_checks" : self.options.skill_checks.value,
            "death_link" : self.options.death_link.value,
            "death_link_behavior" : self.options.death_link_behavior.value,
            "death_link_receive_effect" : self.options.death_link_receive_effect.value,
            "death_link_receive_chance" : self.options.death_link_receive_chance.value,
            "death_link_group" : self.options.death_link_group.value
        }
