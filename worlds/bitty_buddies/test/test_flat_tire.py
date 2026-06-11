from .bases import BittyBuddiesTestBase
from ..options import CartridgeGoalScores, LogicDifficulty
from ..names import ItemName, LocationName, LEVEL_UP_NAMES

class TestFlatTireDisabled(BittyBuddiesTestBase):
    """Make sure the flat tire location is excluded when the option is disabled."""

    # Normal difficulty with flat tire disabled
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True,
        "flat_tire_check": False
    }

    def test_flat_tire_disabled(self):
        self.assertRaises(KeyError, self.world.get_location, LocationName.FLAT_TIRE)


class TestFlatTireEnabled(BittyBuddiesTestBase):
    """Make sure the flat tire location is present and reachable when enabled."""

    # Normal difficulty with flat tire enabled
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True,
        "flat_tire_check": True
    }

    def test_flat_tire_enabled(self):
        try: self.world.get_location(LocationName.FLAT_TIRE)
        except KeyError: self.fail()

    def test_flat_tire_accessibility(self):

        with self.subTest("Test flat tire accessibility for just Benson"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Benson!
            self.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP))

            # Flat tire should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.FLAT_TIRE))

        with self.subTest("Now add in Bazz to make the flat tire check accessible."):
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
            self.assertTrue(self.can_reach_location(LocationName.FLAT_TIRE))
