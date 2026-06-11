from collections.abc import Callable
from copy import deepcopy
from functools import partial

from BaseClasses import CollectionRule, CollectionState, MultiWorld
from worlds.AutoWorld import LogicMixin
from rule_builder.rules import Has

from .names import Buddy, ItemName, EventName
from .options import BittyBuddiesOptions, CartridgeGoalScores, LogicDifficulty

GenericCollectionRule = Callable[[int, BittyBuddiesOptions], CollectionRule]
InclusionRule = Callable[[BittyBuddiesOptions], bool]

# A dictionary of cartridge goal scores by difficulty
CARTRIDGE_GOAL_SCORES: dict[int, dict[int, int]] = {
    CartridgeGoalScores.option_low:     {1: 3,  2: 8,  3: 15, 4: 30,  5: 50},
    CartridgeGoalScores.option_regular: {1: 5,  2: 15, 3: 30, 4: 60,  5: 100},
    CartridgeGoalScores.option_high:    {1: 10, 2: 25, 3: 50, 4: 100, 5: 150},
}


DEFAULT_OPTIMAL_BUDDY_SCORES: dict[int, int] = {
    LogicDifficulty.option_easy:   {1: 5,  2: 10, 3: 20, 4: 35, 5: 50},
    LogicDifficulty.option_normal: {1: 10, 2: 20, 3: 35, 4: 50, 5: 75},
    LogicDifficulty.option_hard:   {1: 15, 2: 30, 3: 45, 4: 70, 5: 100},
}
DEFAULT_HOME_BUDDY_SCORES: dict[int, int] = {
    LogicDifficulty.option_easy:   {1: 3,  2: 8, 3: 14, 4: 24, 5: 35},
    LogicDifficulty.option_normal: {1: 5, 2: 12, 3: 20, 4: 30, 5: 45},
    LogicDifficulty.option_hard:   {1: 6, 2: 15, 3: 30, 4: 45, 5: 60},
}
DEFAULT_SUB_OPTIMAL_BUDDY_SCORES: dict[int, int] = {
    LogicDifficulty.option_easy:   {1: 0, 2: 3, 3: 6, 4: 10, 5: 15},
    LogicDifficulty.option_normal: {1: 3, 2: 6, 3: 10, 4: 15, 5: 20},
    LogicDifficulty.option_hard:   {1: 5, 2: 10, 3: 15, 4: 22, 5: 30},
}

# A big ugly 4-layer dictionary for retrieving in-logic scores when given:
# - Cartridge
#   - Buddy
#     - Buddy Level
#       - Logic Difficulty
LOGIC_SCORES: dict[Buddy, dict[Buddy, dict[int, dict[int, int]]]] = {
    # Trash Dash
    Buddy.BUD: {
        Buddy.BUD: {
            LogicDifficulty.option_easy:   {1: 3, 2: 6,  3: 14, 4: 25, 5: 35},
            LogicDifficulty.option_normal: {1: 6, 2: 10, 3: 14, 4: 30, 5: 45},
            LogicDifficulty.option_hard:   {1: 6, 2: 14, 3: 14, 4: 40, 5: 60},
        },
        Buddy.BIFF: {
            LogicDifficulty.option_easy:   {1: 6, 2: 14,  3: 25, 4: 35, 5: 45},
            LogicDifficulty.option_normal: {1: 10, 2: 20, 3: 35, 4: 55, 5: 75},
            LogicDifficulty.option_hard:   {1: 10, 2: 30, 3: 50, 4: 75, 5: 100},
        },
        Buddy.BENSON: {
            LogicDifficulty.option_easy:   {1: 0, 2: 3, 3: 6,  4: 6,  5: 14},
            LogicDifficulty.option_normal: {1: 6, 2: 6, 3: 6,  4: 14, 5: 14},
            LogicDifficulty.option_hard:   {1: 6, 2: 6, 3: 14, 4: 14, 5: 30},
        },
        Buddy.BRIE: {
            LogicDifficulty.option_easy:   {1: 6,  2: 14, 3: 25, 4: 40, 5: 50},
            LogicDifficulty.option_normal: {1: 10, 2: 25, 3: 40, 4: 60, 5: 80},
            LogicDifficulty.option_hard:   {1: 14, 2: 35, 3: 55, 4: 80, 5: 100},
        },
        Buddy.BAZZ: {
            LogicDifficulty.option_easy:   {1: 0, 2: 3, 3: 6, 4: 6,  5: 6},
            LogicDifficulty.option_normal: {1: 6, 2: 6, 3: 6, 4: 6,  5: 14},
            LogicDifficulty.option_hard:   {1: 6, 2: 6, 3: 6, 4: 14, 5: 14},
        },
    },

    # Have at Thee
    Buddy.BIFF: {
        Buddy.BUD: {
            LogicDifficulty.option_easy:   {1: 0, 2: 2, 3: 4, 4: 6, 5: 12},
            LogicDifficulty.option_normal: {1: 2, 2: 4, 3: 6, 4: 10, 5: 17},
            LogicDifficulty.option_hard:   {1: 4, 2: 6, 3: 8, 4: 17, 5: 24},
        },
        Buddy.BIFF: {
            LogicDifficulty.option_easy:   {1: 6, 2: 12, 3: 19, 4: 24, 5: 34},
            LogicDifficulty.option_normal: {1: 12, 2: 19, 3: 28, 4: 34, 5: 50},
            LogicDifficulty.option_hard:   {1: 17, 2: 24, 3: 38, 4: 50, 5: 65},
        },
        Buddy.BENSON: {
            LogicDifficulty.option_easy:   {1: 6,  2: 12, 3: 19, 4: 34, 5: 50},
            LogicDifficulty.option_normal: {1: 12, 2: 19, 3: 34, 4: 50, 5: 75},
            LogicDifficulty.option_hard:   {1: 17, 2: 28, 3: 45, 4: 75, 5: 100},
        },
        Buddy.BRIE: {
            LogicDifficulty.option_easy:   {1: 0, 2: 0, 3: 2, 4: 4, 5: 6},
            LogicDifficulty.option_normal: {1: 0, 2: 2, 3: 4, 4: 8, 5: 12},
            LogicDifficulty.option_hard:   {1: 2, 2: 4, 3: 6, 4: 12, 5: 17},
        },
        Buddy.BAZZ: {
            LogicDifficulty.option_easy:   {1: 6,  2: 12, 3: 19, 4: 34, 5: 50},
            LogicDifficulty.option_normal: {1: 12, 2: 19, 3: 34, 4: 50, 5: 75},
            LogicDifficulty.option_hard:   {1: 19, 2: 28, 3: 45, 4: 75, 5: 100},
        },
    },

    # Treatment To-Go
    Buddy.BENSON: {
        Buddy.BUD: {
            LogicDifficulty.option_easy:   {1: 6,  2: 12, 3: 20, 4: 35, 5: 50},
            LogicDifficulty.option_normal: {1: 12, 2: 20, 3: 35, 4: 50, 5: 75},
            LogicDifficulty.option_hard:   {1: 20, 2: 30, 3: 45, 4: 70, 5: 100},
        },
        Buddy.BIFF: {
            LogicDifficulty.option_easy:   {1: 3, 2: 5, 3: 7, 4: 10, 5: 15},
            LogicDifficulty.option_normal: {1: 6, 2: 8, 3: 10, 4: 15, 5: 20},
            LogicDifficulty.option_hard:   {1: 10, 2: 12, 3: 14, 4: 20, 5: 30},
        },
        Buddy.BENSON: {
            LogicDifficulty.option_easy:   {1: 4, 2: 8, 3: 14, 4: 24, 5: 35},
            LogicDifficulty.option_normal: {1: 8, 2: 13, 3: 20, 4: 30, 5: 45},
            LogicDifficulty.option_hard:   {1: 13, 2: 18, 3: 30, 4: 45, 5: 60},
        },
        Buddy.BRIE: {
            LogicDifficulty.option_easy:   {1: 5,  2: 11, 3: 16, 4: 32, 5: 48},
            LogicDifficulty.option_normal: {1: 10, 2: 16, 3: 25, 4: 46, 5: 70},
            LogicDifficulty.option_hard:   {1: 15, 2: 24, 3: 36, 4: 65, 5: 100},
        },
        Buddy.BAZZ: {
            LogicDifficulty.option_easy:   {1: 2, 2: 4, 3: 6, 4: 8, 5: 13},
            LogicDifficulty.option_normal: {1: 5, 2: 6, 3: 8, 4: 13, 5: 18},
            LogicDifficulty.option_hard:   {1: 10, 2: 12, 3: 14, 4: 20, 5: 30},
        },
    },

    # Acrobird
    Buddy.BRIE: {
        Buddy.BUD: {
            LogicDifficulty.option_easy:   {1: 5,  2: 10, 3: 18, 4: 30, 5: 45},
            LogicDifficulty.option_normal: {1: 10, 2: 18, 3: 30, 4: 45, 5: 70},
            LogicDifficulty.option_hard:   {1: 15, 2: 28, 3: 45, 4: 70, 5: 100},
        },
        Buddy.BIFF: {
            LogicDifficulty.option_easy:   {1: 0, 2: 0, 3: 2, 4: 5, 5: 8},
            LogicDifficulty.option_normal: {1: 0, 2: 1, 3: 4, 4: 8, 5: 12},
            LogicDifficulty.option_hard:   {1: 1, 2: 2, 3: 8, 4: 14, 5: 20},
        },
        Buddy.BENSON: {
            LogicDifficulty.option_easy:   {1: 0, 2: 3,  3: 6,  4: 10, 5: 15},
            LogicDifficulty.option_normal: {1: 3, 2: 6,  3: 10, 4: 15, 5: 20},
            LogicDifficulty.option_hard:   {1: 6, 2: 10, 3: 15, 4: 20, 5: 28},
        },
        Buddy.BRIE: {
            LogicDifficulty.option_easy:   {1: 3,  2: 8, 3: 14, 4: 21, 5: 30},
            LogicDifficulty.option_normal: {1: 8, 2: 12, 3: 20, 4: 28, 5: 40},
            LogicDifficulty.option_hard:   {1: 12, 2: 20, 3: 30, 4: 45, 5: 60},
        },
        Buddy.BAZZ: {
            LogicDifficulty.option_easy:   {1: 5,  2: 10, 3: 20, 4: 35, 5: 50},
            LogicDifficulty.option_normal: {1: 10, 2: 20, 3: 35, 4: 50, 5: 75},
            LogicDifficulty.option_hard:   {1: 15, 2: 30, 3: 45, 4: 70, 5: 100},
        },
    },

    # Bazz's Big Day
    Buddy.BAZZ: {
        Buddy.BUD: {
            LogicDifficulty.option_easy:   {1: 2, 2: 3, 3: 6, 4: 10, 5: 15},
            LogicDifficulty.option_normal: {1: 5, 2: 7, 3: 9, 4: 15, 5: 21},
            LogicDifficulty.option_hard:   {1: 7, 2: 11, 3: 14, 4: 22, 5: 30},
        },
        Buddy.BIFF: {
            LogicDifficulty.option_easy:   {1: 4,  2: 10, 3: 20, 4: 32, 5: 50},
            LogicDifficulty.option_normal: {1: 8, 2: 20, 3: 32, 4: 50, 5: 75},
            LogicDifficulty.option_hard:   {1: 15, 2: 30, 3: 45, 4: 70, 5: 100},
        },
        Buddy.BENSON: {
            LogicDifficulty.option_easy:   {1: 5,  2: 10, 3: 20, 4: 32, 5: 50},
            LogicDifficulty.option_normal: {1: 10, 2: 20, 3: 35, 4: 48, 5: 75},
            LogicDifficulty.option_hard:   {1: 15, 2: 30, 3: 45, 4: 65, 5: 100},
        },
        Buddy.BRIE: {
            LogicDifficulty.option_easy:   {1: 2, 2: 3, 3: 7, 4: 10, 5: 16},
            LogicDifficulty.option_normal: {1: 5, 2: 7, 3: 10, 4: 15, 5: 22},
            LogicDifficulty.option_hard:   {1: 8, 2: 11, 3: 15, 4: 21, 5: 30},
        },
        Buddy.BAZZ: {
            LogicDifficulty.option_easy:   {1: 3,  2: 8, 3: 16, 4: 25, 5: 35},
            LogicDifficulty.option_normal: {1: 6,  2: 12, 3: 22, 4: 35, 5: 50},
            LogicDifficulty.option_hard:   {1: 10, 2: 18, 3: 35, 4: 50, 5: 75},
        },
    },
}


# NOTE: A logic mixin like this would probably be more efficient for calculating which goal scores are in logic.
#       But... I'm not a huge fan of adding "invisible" members to CollectionState.
#       If the linter can't keep track of it, I don't want to either, lol.
#       If the efficiency of my current implementation ends up being a problem, I'll revisit this.
#       Until then, premature optimization is the root of all evil!
#
#       P.S. If I do end up using this, maybe the linting problem could be fixed by creating
#       a dummy BittyBuddiesCollectionState class that extends CollectionState with the
#       expected members and is used for type hints. It's hacky, but it should work, right?
class ScoreLogicMixin(LogicMixin):
    # A per-player dictionary that tracks the number of goal scores in logic for each cartridge.
    # I.e., if dict[player][Bud] == 3, the first three goal scores for Trash Dash are all in logic.
    bitty_buddies_achievable_goals: dict[int, dict[Buddy, int]]

    # A per-player dictionary that tracks the maximum scores in logic for each buddy in each cartridge.
    # I.e., dictionary is structured as dict[player][cartridge][buddy] = max score in logic
    bitty_buddies_individual_logic_scores: dict[int, dict[Buddy, dict[Buddy, int]]]

    def init_mixin(self, multiworld: MultiWorld):
        self.bitty_buddies_achievable_goals = {}
        self.bitty_buddies_individual_logic_scores = {}
        for player in multiworld.get_game_players("Bitty Buddies"):
            self.bitty_buddies_achievable_goals[player] = {
                Buddy.BUD: 0, Buddy.BIFF: 0, Buddy.BENSON: 0, Buddy.BRIE: 0, Buddy.BAZZ: 0
            }
            self.bitty_buddies_individual_logic_scores[player] = {}
            for buddy in Buddy:
                self.bitty_buddies_individual_logic_scores[player][buddy] = {}
                for cartridge in Buddy:
                    self.bitty_buddies_individual_logic_scores[player][buddy][cartridge] = 0


    def copy_mixin(self, new_state: CollectionState) -> CollectionState:
        new_state.bitty_buddies_achievable_goals = deepcopy(self.bitty_buddies_achievable_goals)
        new_state.bitty_buddies_individual_logic_scores = deepcopy(self.bitty_buddies_individual_logic_scores)
        return new_state

    # TODO: A function to pair with overrides for World.collect and World.remove which recalculates
    #       only the individual logic scores for the buddy who leveled up/down.
    #       *PLUS*
    #       A function to update the achievable goals dictionary based on individual buddy logic scores and
    #       buddy power. (Will need to be called after adjustments to either)


def is_buddy_optimal(cartridge: Buddy, buddy: Buddy) -> bool:
    """Returns whether or not the given buddy is one of the two optimal buddies for the given cartridge."""
    if cartridge == Buddy.BUD: return buddy == Buddy.BIFF or buddy == Buddy.BRIE
    elif cartridge == Buddy.BIFF: return buddy == Buddy.BENSON or buddy == Buddy.BAZZ
    elif cartridge == Buddy.BENSON: return buddy == Buddy.BUD or buddy == Buddy.BRIE
    elif cartridge == Buddy.BRIE: return buddy == Buddy.BUD or buddy == Buddy.BAZZ
    elif cartridge == Buddy.BAZZ: return buddy == Buddy.BIFF or buddy == Buddy.BENSON
    return False

def is_buddy_home(cartridge: Buddy, buddy: Buddy) -> bool:
    """Returns whether or not the given buddy is in their home cartridge."""
    return cartridge == buddy


def get_minimum_logic_score_for_high_goal_scores(cartridge: Buddy, buddy: Buddy, buddy_level: int) -> int:
    """Returns a minimum logic score to potentially adjust easy/normal logic for high goal scores"""
    if is_buddy_optimal(cartridge, buddy):
        return [0, 10, 20, 35, 50, 80][buddy_level]
    elif is_buddy_home(cartridge, buddy):
        return [0, 5, 12, 20, 30, 40][buddy_level]
    else: return 0


def get_bonus_points(state: CollectionState, player: int, cartridge: Buddy) -> int:
    """Returns the player's number of bonus points for the given cartridge and collection state"""
    bonus_point_item_name = ""
    if cartridge == Buddy.BUD: bonus_point_item_name = ItemName.TRASH_DASH_SCORE
    elif cartridge == Buddy.BIFF: bonus_point_item_name = ItemName.HAVE_AT_THEE_SCORE
    elif cartridge == Buddy.BENSON: bonus_point_item_name = ItemName.TREATMENT_TO_GO_SCORE
    elif cartridge == Buddy.BRIE: bonus_point_item_name = ItemName.ACROBIRD_SCORE
    elif cartridge == Buddy.BAZZ: bonus_point_item_name = ItemName.BAZZS_BIG_DAY_SCORE

    bonus_points = 0
    for i in range(state.count(bonus_point_item_name, player)):
        if i < 2: bonus_points += 5
        else: bonus_points += 10

    return bonus_points


def get_cartridge_logic_score(state: CollectionState, player: int, options: BittyBuddiesOptions, cartridge: Buddy):
    """Calculates the maximum score in logic for a given cartridge."""
    potential_buddy_scores: dict[Buddy,int] = {}
    for buddy in Buddy:
        buddy_level_item_name = ""
        if buddy == Buddy.BUD: buddy_level_item_name = ItemName.BUD_LEVEL_UP
        elif buddy == Buddy.BIFF: buddy_level_item_name = ItemName.BIFF_LEVEL_UP
        elif buddy == Buddy.BENSON: buddy_level_item_name = ItemName.BENSON_LEVEL_UP
        elif buddy == Buddy.BRIE: buddy_level_item_name = ItemName.BRIE_LEVEL_UP
        elif buddy == Buddy.BAZZ: buddy_level_item_name = ItemName.BAZZ_LEVEL_UP
        buddy_level = min(state.count(buddy_level_item_name,player),5)

        if not buddy_level:
            potential_buddy_scores[buddy] = 0
        else:
            potential_buddy_scores[buddy] = LOGIC_SCORES[cartridge][buddy][options.logic_difficulty][buddy_level]
            if options.cartridge_goal_scores.value == CartridgeGoalScores.option_high:
                min_logic_score = get_minimum_logic_score_for_high_goal_scores(cartridge, buddy, buddy_level)
                if min_logic_score > potential_buddy_scores[buddy]: potential_buddy_scores[buddy] = min_logic_score

    buddy_power = min(max(state.count(ItemName.BUDDY_POWER,player),1),5)
    top_buddies = sorted(potential_buddy_scores.values())[-buddy_power:]
    return sum(top_buddies) + get_bonus_points(state, player, cartridge)


def is_goal_score_in_logic(
    state: CollectionState, player: int, options: BittyBuddiesOptions, cartridge: Buddy, which_level: int
) -> bool:
    """
    Determine if a given level up is in logic by comparing the maximum score in logic
    for that cartridge to the level up score.
    """
    maximum_score_in_logic = get_cartridge_logic_score(state, player, options, cartridge)
    return maximum_score_in_logic >= CARTRIDGE_GOAL_SCORES[options.cartridge_goal_scores.value][which_level]

def create_goal_score_rule(
    player: int, options: BittyBuddiesOptions, cartridge: Buddy, which_level: int
) -> CollectionRule:
    """Returns a collection rule derived from `is_goal_score_in_logic`."""
    return partial(
        is_goal_score_in_logic,
        player = player, options = options, cartridge = cartridge, which_level = which_level
    )

def create_generic_goal_score_rule(cartridge: Buddy, which_level: int) -> GenericCollectionRule:
    """Generalizes the goal score rule so it can be created without specific player data."""
    return partial(
        create_goal_score_rule,
        cartridge = cartridge, which_level = which_level
    )


def is_buddy_power_check_in_logic(
    state: CollectionState, player: int, options: BittyBuddiesOptions, which_level: int
):
    """Determine if the buddy power check for the given level is in logic by
    checking each cartridge to see if the level is in logic."""
    for cartridge in Buddy:
        if not is_goal_score_in_logic(state, player, options, cartridge, which_level):
            return False
    return True

def create_buddy_power_rule(
    player: int, options: BittyBuddiesOptions, which_level: int
) -> CollectionRule:
    """Returns a collection rule derived from `is_buddy_power_check_in_logic`."""
    return partial( is_buddy_power_check_in_logic, player = player, options = options, which_level = which_level)

def create_generic_buddy_power_rule(which_level: int) -> GenericCollectionRule:
    """Generalizes the buddy power rule so it can be created without specific player data."""
    return partial(create_buddy_power_rule, which_level = which_level)


def are_all_buddies_maxed(state: CollectionState, player: int) -> bool:
    """Determine if all buddies and buddy power are at max level."""
    return all([
        state.has(ItemName.BUD_LEVEL_UP,player,5),
        state.has(ItemName.BIFF_LEVEL_UP,player,5),
        state.has(ItemName.BENSON_LEVEL_UP,player,5),
        state.has(ItemName.BRIE_LEVEL_UP,player,5),
        state.has(ItemName.BAZZ_LEVEL_UP,player,5),
        state.has(ItemName.BUDDY_POWER,player,5),
    ])

def get_total_score_in_logic(state: CollectionState, player: int, options: BittyBuddiesOptions) -> int:
    """Add up all the cartridge logic scores to get the total score in logic."""
    total_score_in_logic = 0
    for buddy in Buddy:
        total_score_in_logic += get_cartridge_logic_score(state, player, options, buddy)
    return total_score_in_logic


def is_final_goal_achievable(state: CollectionState, player: int, options: BittyBuddiesOptions) -> bool:
    """
    Determines if the final goal score is achievable based on the sum of each cartridge's maximum score in logic.
    Additionally, this rule returns True automatically if all buddies and buddy power are already level 5.
    """
    if are_all_buddies_maxed(state, player):
        return True
    else:
        if get_total_score_in_logic(state, player, options) >= options.final_goal_score: return True
        else: return False

def create_final_goal_rule(player: int, options: BittyBuddiesOptions) -> CollectionRule:
    """Returns a collection rule derived from `is_final_goal_achievable`."""
    return partial(is_final_goal_achievable, player = player, options = options)

def create_generic_final_goal_rule() -> GenericCollectionRule:
    """Generalizes the all buddies maxed rule so it can be created without specific player data."""
    return partial(create_final_goal_rule)


flat_tire_generic_collection_rule: GenericCollectionRule = (
    lambda _player, _options: Has(ItemName.BAZZ_LEVEL_UP)
)
flat_tire_inclusion_rule: InclusionRule = lambda options: options.flat_tire_check


completion_rule = Has(EventName.VICTORY)
