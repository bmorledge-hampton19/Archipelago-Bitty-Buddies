from dataclasses import dataclass

from Options import Choice, Range, NamedRange, Toggle, FreeText, PerGameCommonOptions, DeathLink, OptionGroup


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
    range_end = 1999
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

    default = True


class SillyChecks(Toggle):
    """
    Adds a check for the "silly interaction" that each buddy has in one of their sub-optimal cartridges.
    (E.g., Bazz popping the tires on the cars in Treatment To-Go.
    See the Bitty Buddies Archipelago game page for more detailed information on each check.)
    """

    display_name = "Silly Checks"


class SkillChecks(Toggle):
    """
    Adds a tricky check that each buddy has in one of their optimal cartridges.
    (E.g., Fly over a paper airplane with Brie in Trash Dash.
    See the Bitty Buddies Archipelago game page for more detailed information on each check.)
    """

    display_name = "Skill Checks"


class BittyBuddiesDeathLink(DeathLink):
    """
    Enables Death Link.

    Death links are sent on game over if a new high score was not achieved,
    provided that no death links were received during the attempt.
    """
    display_name = "Death Link"


class DeathLinkBehavior(Choice):
    """
    Enable full (send and receive) or partial (send only; receive only) death link.
    """

    display_name = "Death Link Behavior"

    option_send_and_receive = 0
    option_send_only = 1
    option_receive_only = 2

    default = option_send_and_receive


class DeathLinkReceiveEffect(Choice):
    """
    Determines the effect of received death links.
    - Game Over: Death links trigger a game over.
    - Next Buddy: Death links trigger a transition to the next available buddy (as if the current buddy just failed).
      If there are no buddies remaining for the current game, a game over is triggered.
    """

    display_name = "Death Link Receive Effect"

    option_game_over = 0
    option_next_buddy = 1

    default = option_game_over


class DeathLinkReceiveChance(Range):
    """
    Percentage chance that any received death links will actually impact you.
    This can make death link in larger archipelagos much more manageable.
    """

    display_name = "Death Link Receive Chance"

    range_start = 0
    range_end = 100
    default = 100


class DeathLinkGroup(FreeText):
    """
    Restricts death link to players with the same group name.
    Leave blank to enable death link with all ungrouped players.
    """
    display_name = "Death Link Group"


@dataclass
class BittyBuddiesOptions(PerGameCommonOptions):
    cartridge_goal_scores: CartridgeGoalScores
    logic_difficulty: LogicDifficulty
    final_goal_score: FinalGoalScore
    randomize_buddy_power: RandomizeBuddyPower
    silly_checks: SillyChecks
    skill_checks: SkillChecks
    death_link: BittyBuddiesDeathLink
    death_link_behavior: DeathLinkBehavior
    death_link_receive_effect: DeathLinkReceiveEffect
    death_link_receive_chance: DeathLinkReceiveChance
    death_link_group: DeathLinkGroup


option_groups = [
    OptionGroup(
        "Death Link Options",
        [BittyBuddiesDeathLink, DeathLinkBehavior, DeathLinkReceiveEffect, DeathLinkReceiveChance, DeathLinkGroup],
    ),
]

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
