from .bases import BittyBuddiesTestBase
from ..options import CartridgeGoalScores, LogicDifficulty
from ..names import ItemName, BUDDY_POWER_LOCATION_NAMES

class TestFixedBuddyPower(BittyBuddiesTestBase):
    """
    Make sure that turning off buddy power randomization assigns the buddy power increases
    to the expected locations.
    """

    # Normal difficulty with fixed buddy power locations
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": False
    }

    def test_fixed_buddy_power(self):
        buddy_power_locations = set(
            location.name for location in self.multiworld.find_item_locations(ItemName.BUDDY_POWER, self.player)
        )
        self.assertTrue(buddy_power_locations == set(BUDDY_POWER_LOCATION_NAMES))
