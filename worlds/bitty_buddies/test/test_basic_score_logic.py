from .bases import BittyBuddiesTestBase
from ..options import CartridgeGoalScores, LogicDifficulty
from ..names import ItemName, LocationName, LEVEL_UP_NAMES, EventName

class TestBasicScoreLogic(BittyBuddiesTestBase):
    """Tests the basic logic for the goal score checks (which are most of the checks in the game.)"""

    # Normal difficulty
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True
    }


    def test_initial_items(self):

        with self.subTest("Test checks that the initial buddy has been collected."):
            self.assertTrue(any(
                self.multiworld.state.has(level_up_name, self.player) for level_up_name in LEVEL_UP_NAMES
            ))

        with self.subTest("Test checks that the initial buddy power has been collected."):
            self.assertTrue(self.multiworld.state.has(ItemName.BUDDY_POWER, self.player))


    def test_adding_buddies(self):

        with self.subTest("Test the starting checks for Bud"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bud!
            self.collect(self.world.create_item(ItemName.BUD_LEVEL_UP))

            # The first checks should be available in all cartridges except Have At Thee.
            self.assertTrue(all([
                self.can_reach_location(LocationName.TRASH_DASH_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.ACROBIRD_1),
                self.can_reach_location(LocationName.BAZZS_BIG_DAY_1),
            ]))
            self.assertFalse(self.can_reach_location(LocationName.HAVE_AT_THEE_1))

            # Consequently, the first "buddy power" check should also be inaccessible.
            self.assertFalse(self.can_reach_location(LocationName.ALL_BUDDIES_LEVEL_1))

        with self.subTest("Add in Bazz and check that all of the first checks are now accessible"):
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
            self.assertTrue(all([
                self.can_reach_location(LocationName.TRASH_DASH_1),
                self.can_reach_location(LocationName.HAVE_AT_THEE_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.ACROBIRD_1),
                self.can_reach_location(LocationName.BAZZS_BIG_DAY_1),
                self.can_reach_location(LocationName.ALL_BUDDIES_LEVEL_1)
            ]))

        with self.subTest(
            "Check that increasing buddy power allows Bud and Bazz to collect a check that was" \
            "inaccessible to either buddy on their own."
        ):
            self.assertFalse(self.can_reach_location(LocationName.ACROBIRD_2))
            self.collect(self.world.create_item(ItemName.BUDDY_POWER))
            self.assertTrue(self.can_reach_location(LocationName.ACROBIRD_2))


    def test_buddy_levels(self):

        with self.subTest("Test the starting checks for Biff"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Biff!
            self.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP))

            # The first checks should be available in all cartridges except Acrobird.
            self.assertTrue(all([
                self.can_reach_location(LocationName.TRASH_DASH_1),
                self.can_reach_location(LocationName.HAVE_AT_THEE_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.BAZZS_BIG_DAY_1),
            ]))
            self.assertFalse(self.can_reach_location(LocationName.ACROBIRD_1))

        with self.subTest("Level up Biff and check the 2nd goal score locations for his optimal games."):
            # Ensure that the level 2 checks for Biff's optimal games aren't already accessible.
            self.assertFalse(self.can_reach_location(LocationName.TRASH_DASH_2))
            self.assertFalse(self.can_reach_location(LocationName.BAZZS_BIG_DAY_2))

            # Level up Biff!
            self.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP))

            # Now the checks should be accessible!
            self.assertTrue(self.can_reach_location(LocationName.TRASH_DASH_2))
            self.assertTrue(self.can_reach_location(LocationName.BAZZS_BIG_DAY_2))


    def test_bonus_score(self):

        with self.subTest("Test the starting checks for Biff"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Benson!
            self.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP))

            # The first checks should be available in all cartridges except Acrobird.
            self.assertTrue(all([
                self.can_reach_location(LocationName.TRASH_DASH_1),
                self.can_reach_location(LocationName.HAVE_AT_THEE_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.BAZZS_BIG_DAY_1),
            ]))
            self.assertFalse(self.can_reach_location(LocationName.ACROBIRD_1))

        with self.subTest("Add in some bonus score so that the first Acrobird check is now collectible"):
            self.collect(self.world.create_item(ItemName.ACROBIRD_SCORE))
            self.assertTrue(self.can_reach_location(LocationName.ACROBIRD_1))

        with self.subTest("Add in a BUNCH of bonus score so that Acrobird is fully completable"):
            # We need 97 bonus points to hit the 100-point goal.
            # 9 more bonus score checks gives us 10 in total, which should give:
            # 10 (5*2) points from the first two bonuses + 80 (10*8) points from the other 8 = 90 points.
            # So, we should be just short of the last check.
            for _ in range(9): self.collect(self.world.create_item(ItemName.ACROBIRD_SCORE))
            self.assertTrue(self.can_reach_location(LocationName.ACROBIRD_4))
            self.assertFalse(self.can_reach_location(LocationName.ACROBIRD_5))

            # Adding in one more bonus score item should make the last Acrobird location accessible.
            self.collect(self.world.create_item(ItemName.ACROBIRD_SCORE))
            self.assertTrue(self.can_reach_location(LocationName.ACROBIRD_5))

        with self.subTest("Add in a frankly ridiculous amount of bonus score to make the final goal accessible."):
            self.assertFalse(self.can_reach_location(EventName.VICTORY))
            for _ in range(999): self.collect(self.world.create_item(ItemName.ACROBIRD_SCORE))
            self.assertTrue(self.can_reach_location(EventName.VICTORY))
