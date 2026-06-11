from dataclasses import dataclass

from Options import Choice, NamedRange, Toggle, PerGameCommonOptions, DeathLink


class CartridgeGoalScores(Choice):
    """
    How high the goal scores are in each cartridge. There are three options:

    Low (For shorter games):
    - Checks are obtained at scores of 3, 8, 15, 30, and 50

    Regular (The standard Bitty Buddies experience):
    - Checks are obtained at scores of 5, 15, 30, 60, and 100

    High (For longer games):
    - Checks are obtained at scores of 10, 25, 50, 100, and 150
    """

    display_name = "Cartridge Goal Scores"

    option_low = 0
    option_regular = 1
    option_high = 2

    default = option_regular


class LogicDifficulty(Choice):
    """
    How high each buddy is expected to score, based on the level and cartridge.

    For example, at normal difficulty a level 1 Bud is only expected to score 6 points in Trash Dash,
    but at hard difficulty, a level 1 Bud is expected to score 14 points in Trash Dash (by clearing trash cans).

    The following logic difficulties are recommended based on the value of the Level Up Scores option:
    - Low Scores: Easy logic
    - Regular Scores: Normal logic
    - High Scores: Hard Logic

    *Note:* Choosing easy/normal logic with high level up scores may force more difficult logic in some cases.
    """

    display_name = "Logic Difficulty"

    option_easy = 0
    option_normal = 1
    option_hard = 2

    default = option_normal


class FinalGoalScore(NamedRange):
    """
    The score (totaled across all cartridges) that is required to beat the game.

    The following goal scores are recommended based on the value of the Level Up Scores option:
    - Low Scores: 499
    - Regular Scores: 999
    - High Scores: 1499
    """

    display_name = "Final Goal Score"

    range_start = 1
    range_end = 2000
    default = 999

    special_range_names = {"low": 499, "regular": 999, "high": 1499}


class RandomizeBuddyPower(Toggle):
    """
    Randomizes Buddy Power increases.

    Buddy Power checks are received when the goal scores for a given threshold are achieved across all cartridges.
    (I.e., when the 1st checks have been received in all cartridges.)
    If Buddy Power increases are not randomized, these checks will always increase buddy power, like the base game.
    """

    display_name = "Randomize Buddy Power Increases"


class FlatTireCheck(Toggle):
    """
    Adds a single check for popping a customer's tires with Bazz in Treatment To-Go.
    """

    display_name = "Flat Tire Check"


class BittyBuddiesDeathLink(DeathLink):
    """
    Enables Death Link.

    Death links are sent on game over if a new high score was not achieved,
    provided that no death links were received during the attempt.
    """
    display_name = "Death Link"


class DeathLinkReceiveBehavior(Choice):
    """
    Determines the effect of received death links.
    - Game Over: Death links trigger a game over.
    - Next Buddy: Death links trigger a transition to the next available buddy (as if the current buddy just failed).
    If there are no buddies remaining for the current game, a game over is triggered.
    """

    display_name = "Death Link Behavior"

    option_game_over = 0
    option_next_buddy = 1

    default = option_game_over


@dataclass
class BittyBuddiesOptions(PerGameCommonOptions):
    cartridge_goal_scores: CartridgeGoalScores
    logic_difficulty: LogicDifficulty
    final_goal_score: FinalGoalScore
    randomize_buddy_power: RandomizeBuddyPower
    flat_tire_check: FlatTireCheck
    death_link: BittyBuddiesDeathLink
    death_link_receive_behavior: DeathLinkReceiveBehavior


# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "easy": {
        "cartridge_goal_scores": CartridgeGoalScores.option_low,
        "logic_difficulty": LogicDifficulty.option_easy,
        "final_goal_score": 500,
        "randomize_buddy_power": True
    },
    "normal": {
        "cartridge_goal_scores": CartridgeGoalScores.option_regular,
        "logic_difficulty": LogicDifficulty.option_normal,
        "final_goal_score": 999,
        "randomize_buddy_power": True
    },
    "hard": {
        "cartridge_goal_scores": CartridgeGoalScores.option_high,
        "logic_difficulty": LogicDifficulty.option_hard,
        "final_goal_score": 1999,
        "randomize_buddy_power": True
    },
}
