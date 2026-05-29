from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class LevelUpScores(Choice):
    """
    How high the level up scores are throughout the game. There are three options:

    Low (For shorter games):
    - Buddies level up at scores of 3, 8, 15, 30, and 50

    Regular (The standard Bitty Buddies experience):
    - Buddies level up at scores of 5, 15, 30, 60, and 100

    High (For longer games):
    - Buddies level up at scores of 10, 30, 60, 120, and 200
    """

    display_name = "Goal Scores"

    option_low = 0
    option_regular = 1
    option_high = 2

    default = option_regular


class GoalScore(Range):
    """
    The score (totaled across all cartridges) that is required to beat the game.

    The following goal scores are recommended based on the value of the Level Up Scores option:
    Low: 500
    Regular: 999
    High: 1999
    """

    display_name = "Goal Score"

    range_start = 1
    range_end = 2000

    default = 999


class LogicDifficulty(Choice):
    """
    How high each buddy is expected to score, based on the level and cartridge.

    For example, at normal difficulty a level 1 Bud is only expected to score 6 points in Trash Dash, 
    but at hard difficulty, a level 1 Bud is expected to score 14 points in Trash Dash (by clearing trash cans).
    """

    display_name = "Logic Difficulty"

    option_easy = 0
    option_normal = 1
    option_hard = 2

    # Choice options must define an explicit default value.
    default = option_normal


class RandomizeBuddyPower(Toggle):
    """
    Whether or not Buddy Power increases are randomized.

    Buddy Power checks are received when the goal scores for a given level are achieved across all cartridges.
    (I.e., when the level 1 checks have been received in all cartridges.)
    If Buddy Power increases are not randomized, these checks will always increase buddy power, like the base game.
    """

    display_name = "Randomize Buddy Power Increases"
