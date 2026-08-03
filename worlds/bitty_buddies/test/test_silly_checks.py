from .bases import BittyBuddiesTestBase
from ..options import CartridgeGoalScores, LogicDifficulty
from ..names import ItemName, LocationName, LEVEL_UP_NAMES, SILLY_CHECK_NAMES

class TestSillyChecksDisabled(BittyBuddiesTestBase):
    """Make sure the silly check locations are excluded when the option is disabled."""

    # Normal difficulty with silly checks disabled
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True,
        "silly_checks": False
    }

    def test_silly_checks_disabled(self) -> None:
        for location in SILLY_CHECK_NAMES:
            self.assertRaises(KeyError, self.world.get_location, location)


class TestSillyChecksEnabled(BittyBuddiesTestBase):
    """Make sure the silly check locations are present and reachable when enabled."""

    # Normal difficulty with silly checks enabled
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True,
        "silly_checks": True
    }

    def test_silly_checks_enabled(self) -> None:
        for location in SILLY_CHECK_NAMES:
            try: self.world.get_location(location)
            except KeyError: self.fail()

    def test_mean_mugging_accessibility(self) -> None:

        with self.subTest("Test Mean Mugging accessibility for just Biff, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Biff!
            self.multiworld.state.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP), True)

            # Mean Mugging should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.MEAN_MUGGING))

        with self.subTest("Now add in Bud to make the location accessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BUD_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.MEAN_MUGGING))

    def test_heavyweight_champion_accessibility(self) -> None:

        with self.subTest("Test Heavyweight Champion accessibility for just Benson, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Benson!
            self.multiworld.state.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP), True)

            # Heavyweight Champion should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.HEAVYWEIGHT_CHAMPION))

        with self.subTest("Now add in Biff to make the location accessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.HEAVYWEIGHT_CHAMPION))

    def test_frictionless_fruit_accessibility(self) -> None:

        with self.subTest("Test Frictionless Fruit accessibility for just Brie, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Brie!
            self.multiworld.state.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP), True)

            # Frictionless Fruit should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.FRICTIONLESS_FRUIT))

        with self.subTest("Now add in Benson to make the location accessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.FRICTIONLESS_FRUIT))

    def test_negative_jing_accessibility(self) -> None:

        with self.subTest("Test Negative Jing accessibility for just Bazz, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bazz!
            self.multiworld.state.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP), True)

            # Negative Jing should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.NEGATIVE_JING))

        with self.subTest("Now add in Brie to make the location accessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.NEGATIVE_JING))

    def test_zero_star_review_accessibility(self) -> None:

        with self.subTest("Test Zero Star Review accessibility for just Bud, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bud!
            self.multiworld.state.collect(self.world.create_item(ItemName.BUD_LEVEL_UP), True)

            # Zero Star Review should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.ZERO_STAR_REVIEW))

        with self.subTest("Now add in Bazz to make the location accessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.ZERO_STAR_REVIEW))
