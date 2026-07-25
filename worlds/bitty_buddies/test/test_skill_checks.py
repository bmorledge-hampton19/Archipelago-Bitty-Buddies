from .bases import BittyBuddiesTestBase
from ..options import CartridgeGoalScores, LogicDifficulty
from ..names import ItemName, LocationName, LEVEL_UP_NAMES, SKILL_CHECK_NAMES

class TestSkillChecksDisabled(BittyBuddiesTestBase):
    """Make sure the skill check locations are excluded when the option is disabled."""

    # Normal difficulty with skill checks disabled
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True,
        "skill_checks": False
    }

    def test_skill_checks_disabled(self):
        for location in SKILL_CHECK_NAMES:
            self.assertRaises(KeyError, self.world.get_location, location)


class TestSkillChecksEnabled(BittyBuddiesTestBase):
    """Make sure the skill check locations are present and reachable when enabled."""

    # Normal difficulty with skill checks enabled
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True,
        "skill_checks": True
    }

    def test_skill_checks_enabled(self):
        for location in SKILL_CHECK_NAMES:
            try: self.world.get_location(location)
            except KeyError: self.fail()

    def test_fast_pharma_accessibility(self):

        with self.subTest("Test Fast Pharma accessibility for a level 5 Biff, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Biff!
            for _ in range(5):
                self.multiworld.state.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP), True)

            # Fast Pharma should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.FAST_PHARMA))

        with self.subTest("Now add in Bud. The location should still be inaccessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BUD_LEVEL_UP), True)
            self.assertFalse(self.can_reach_location(LocationName.FAST_PHARMA))

        with self.subTest("Level up Bud to 4 so that the location becomes accessible."):
            for _ in range(3):
                self.multiworld.state.collect(self.world.create_item(ItemName.BUD_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.FAST_PHARMA))

    def test_parry_king_accessibility(self):

        with self.subTest("Test Parry King accessibility for a level 5 Benson, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Benson!
            for _ in range(5):
                self.multiworld.state.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP), True)

            # Parry King should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.PARRY_KING))

        with self.subTest("Now add in Biff. The location should still be inaccessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP), True)
            self.assertFalse(self.can_reach_location(LocationName.PARRY_KING))

        with self.subTest("Level up Biff to 4 so that the location becomes accessible."):
            for _ in range(3):
                self.multiworld.state.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.PARRY_KING))

    def test_miracle_cure_accessibility(self):

        with self.subTest("Test Miracle Cure accessibility for a level 5 Brie, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Brie!
            for _ in range(5):
                self.multiworld.state.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP), True)

            # Miracle Cure should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.MIRACLE_CURE))

        with self.subTest("Now add in Benson to make the location accessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.MIRACLE_CURE))

    def test_high_flyer_accessibility(self):

        with self.subTest("Test High Flyer accessibility for a level 5 Bazz, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bazz!
            for _ in range(5):
                self.multiworld.state.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP), True)

            # High Flyer should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.HIGH_FLYER))

        with self.subTest("Now add in Brie. The location should still be inaccessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP), True)
            self.assertFalse(self.can_reach_location(LocationName.HIGH_FLYER))

        with self.subTest("Level up Brie to 4 so that the location becomes accessible."):
            for _ in range(3):
                self.multiworld.state.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.HIGH_FLYER))

    def test_sharpshooter_accessibility(self):

        with self.subTest("Test Sharpshooter accessibility for a level 5 Bud, who can't access it."):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bud!
            for _ in range(5):
                self.multiworld.state.collect(self.world.create_item(ItemName.BUD_LEVEL_UP), True)

            # Sharpshooter should be inaccessible
            self.assertFalse(self.can_reach_location(LocationName.SHARPSHOOTER))

        with self.subTest("Now add in Bazz. The location should still be inaccessible."):
            self.multiworld.state.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP), True)
            self.assertFalse(self.can_reach_location(LocationName.SHARPSHOOTER))

        with self.subTest("Level up Bazz to 3 so that the location becomes accessible."):
            for _ in range(2):
                self.multiworld.state.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP), True)
            self.assertTrue(self.can_reach_location(LocationName.SHARPSHOOTER))
