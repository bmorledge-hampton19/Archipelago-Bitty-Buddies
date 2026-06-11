from .bases import BittyBuddiesTestBase
from ..options import CartridgeGoalScores, LogicDifficulty
from ..names import ItemName, LocationName, LEVEL_UP_NAMES, EventName
from ..rules import get_total_score_in_logic, are_all_buddies_maxed

class TestEasyDifficulty(BittyBuddiesTestBase):
    """Tests some logic specific to the easy difficulty preset"""

    # Easy difficulty
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_low,
        "logic_difficulty": LogicDifficulty.option_easy,
        "final_goal_score": 499,
        "randomize_buddy_power": True
    }


    def test_easy_difficulty(self):

        with self.subTest("Test the first few checks with Brie as the starting buddy"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Brie!
            self.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP))

            # The first checks should be available in all cartridges except Have At Thee and Bazz's Big Day.
            # Importantly, the first BBD check is only available to Brie on the normal preset, not easy.
            self.assertTrue(all([
                self.can_reach_location(LocationName.TRASH_DASH_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.ACROBIRD_1),
            ]))
            self.assertFalse(self.can_reach_location(LocationName.HAVE_AT_THEE_1))
            self.assertFalse(self.can_reach_location(LocationName.BAZZS_BIG_DAY_1))

        with self.subTest("Level up Brie to make the BBD check available."):
            self.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP))
            self.assertTrue(self.can_reach_location(LocationName.BAZZS_BIG_DAY_1))

        with self.subTest("Maximize Brie's level to make all the first goal score locations available."):
            # This also tests for out-of-bounds buddy levels.
            for _ in range(999): self.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP))
            self.assertTrue(all([
                self.can_reach_location(LocationName.TRASH_DASH_1),
                self.can_reach_location(LocationName.HAVE_AT_THEE_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.ACROBIRD_1),
                self.can_reach_location(LocationName.BAZZS_BIG_DAY_1),
                self.can_reach_location(LocationName.ALL_BUDDIES_LEVEL_1)
            ]))


class TestHardDifficulty(BittyBuddiesTestBase):
    """Tests some logic specific to the hard difficulty preset"""

    # Hard difficulty
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_high,
        "logic_difficulty": LogicDifficulty.option_hard,
        "final_goal_score": 1499,
        "randomize_buddy_power": True
    }


    def test_hard_difficulty(self):

        with self.subTest("Test the first few checks with Bazz as the starting buddy"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bazz!
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))

            # The first checks should be available in all cartridges except Trash Dash.
            # Importantly, the first Trash Dash check is only available to Bazz on the normal preset, not hard.
            self.assertTrue(all([
                self.can_reach_location(LocationName.HAVE_AT_THEE_1),
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.ACROBIRD_1),
                self.can_reach_location(LocationName.BAZZS_BIG_DAY_1)
            ]))
            self.assertFalse(self.can_reach_location(LocationName.TRASH_DASH_1))

        with self.subTest("Level up Bazz a few times to make the Trash Dash check available."):
            # Even a level 3 Bazz can't reach the first check in hard difficulty,
            # even though the check is obtainable in the easy and normal difficulties.
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
            self.assertFalse(self.can_reach_location(LocationName.TRASH_DASH_1))

            # One more level should do the trick!
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
            self.assertTrue(self.can_reach_location(LocationName.TRASH_DASH_1))

        with self.subTest("Test the heightened final goal score using bonus score checks."):
            # Given 1000 points of bonus score, the final goal score would be achievable in
            # easy and normal, but not hard.
            for _ in range(101): self.collect(self.world.create_item(ItemName.TRASH_DASH_SCORE))
            self.assertFalse(self.can_reach_location(EventName.VICTORY))

            # Another 1000 bonus points should do it though!
            for _ in range(100): self.collect(self.world.create_item(ItemName.TRASH_DASH_SCORE))
            self.assertTrue(self.can_reach_location(EventName.VICTORY))


class TestHighGoalScoresEasyLogic(BittyBuddiesTestBase):
    """Tests the minimum score logic that makes high goal scores completable with easy logic"""

    # High goal scores with easy logic
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_high,
        "logic_difficulty": LogicDifficulty.option_easy,
        "final_goal_score": 1499,
        "randomize_buddy_power": True
    }

    def test_high_goal_scores_easy_logic(self):

        with self.subTest("Test the first few checks with Bud as the starting buddy"):
            # Remove the random starting buddy.
            for level_up_name in LEVEL_UP_NAMES: self.remove_by_name(level_up_name)

            # Add in Bud!
            self.collect(self.world.create_item(ItemName.BUD_LEVEL_UP))

            # With the default easy logic and high goal scores, no locations would normally be accessible
            # to level 1 Bud. However, the minimum logic score should kick in to make the first locations
            # for his optimal cartridges accessible.
            self.assertTrue(all([
                self.can_reach_location(LocationName.TREATMENT_TO_GO_1),
                self.can_reach_location(LocationName.ACROBIRD_1)
            ]))
            self.assertFalse(self.can_reach_location(LocationName.TRASH_DASH_1))
            self.assertFalse(self.can_reach_location(LocationName.HAVE_AT_THEE_1))
            self.assertFalse(self.can_reach_location(LocationName.BAZZS_BIG_DAY_1))

        with self.subTest("Test minimum logic scores across multiple buddies"):
            # Make sure the second Trash Dash location is inaccessible.
            self.assertFalse(self.can_reach_location(LocationName.TRASH_DASH_2))

            # Add in a couple more buddies and the buddy power to make sure they can all be used.
            self.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP))
            self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
            self.collect(self.world.create_item(ItemName.BUDDY_POWER))
            self.collect(self.world.create_item(ItemName.BUDDY_POWER))

            # With the minimum score logic, these 3 buddies should exactly meet the score threshold for Trash Dash 2!
            self.assertFalse(self.can_reach_location(LocationName.TRASH_DASH_2))


        with self.subTest("Test final goal score maxed buddies check"):
            # Make sure the goal score isn't already achievable.
            self.assertFalse(self.can_reach_location(EventName.VICTORY))

            # Max out all the buddies!
            for _ in range(5):
                self.collect(self.world.create_item(ItemName.BUD_LEVEL_UP))
                self.collect(self.world.create_item(ItemName.BIFF_LEVEL_UP))
                self.collect(self.world.create_item(ItemName.BENSON_LEVEL_UP))
                self.collect(self.world.create_item(ItemName.BRIE_LEVEL_UP))
                self.collect(self.world.create_item(ItemName.BAZZ_LEVEL_UP))
                self.collect(self.world.create_item(ItemName.BUDDY_POWER))

            # Even with maxed buddies and the minimum score logic, the total score in logic should be too low to
            # access the final goal score location...
            total_score_in_logic = get_total_score_in_logic(self.multiworld.state, self.player, self.world.options)
            self.assertFalse(total_score_in_logic >= self.world.options.final_goal_score)

            # ...But the location is still available since all buddies are maxed!
            self.assertTrue(are_all_buddies_maxed(self.multiworld.state, self.player))
            self.assertTrue(self.can_reach_location(EventName.VICTORY))


class TestRegularGoalScoresEasyLogic(BittyBuddiesTestBase):
    """Runs the basic tests to make sure that regular goal scores are achievable with easy logic"""

    # Regular goal scores with easy logic
    options = {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_easy,
        "final_goal_score": 999,
        "randomize_buddy_power": True
    }

    # Just runs the default tests. (test_fill is most important here.)
