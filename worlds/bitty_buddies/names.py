### A collection of enums for standardizing names across the Bitty Buddies Archipelago.
from enum import IntEnum, StrEnum


class Buddy(IntEnum):
    BUD = 0
    BIFF = 1
    BENSON = 2
    BRIE = 3
    BAZZ = 4


class RegionName(StrEnum):
    MENU = "Menu"


class LocationName(StrEnum):
    TRASH_DASH_1 = "Trash Dash Goal Score 1"
    TRASH_DASH_2 = "Trash Dash Goal Score 2"
    TRASH_DASH_3 = "Trash Dash Goal Score 3"
    TRASH_DASH_4 = "Trash Dash Goal Score 4"
    TRASH_DASH_5 = "Trash Dash Goal Score 5"

    HAVE_AT_THEE_1 = "Have At Thee Goal Score 1"
    HAVE_AT_THEE_2 = "Have At Thee Goal Score 2"
    HAVE_AT_THEE_3 = "Have At Thee Goal Score 3"
    HAVE_AT_THEE_4 = "Have At Thee Goal Score 4"
    HAVE_AT_THEE_5 = "Have At Thee Goal Score 5"

    TREATMENT_TO_GO_1 = "Treatment To-Go Goal Score 1"
    TREATMENT_TO_GO_2 = "Treatment To-Go Goal Score 2"
    TREATMENT_TO_GO_3 = "Treatment To-Go Goal Score 3"
    TREATMENT_TO_GO_4 = "Treatment To-Go Goal Score 4"
    TREATMENT_TO_GO_5 = "Treatment To-Go Goal Score 5"

    ACROBIRD_1 = "Acrobird Goal Score 1"
    ACROBIRD_2 = "Acrobird Goal Score 2"
    ACROBIRD_3 = "Acrobird Goal Score 3"
    ACROBIRD_4 = "Acrobird Goal Score 4"
    ACROBIRD_5 = "Acrobird Goal Score 5"

    BAZZS_BIG_DAY_1 = "Bazz's Big Day Goal Score 1"
    BAZZS_BIG_DAY_2 = "Bazz's Big Day Goal Score 2"
    BAZZS_BIG_DAY_3 = "Bazz's Big Day Goal Score 3"
    BAZZS_BIG_DAY_4 = "Bazz's Big Day Goal Score 4"
    BAZZS_BIG_DAY_5 = "Bazz's Big Day Goal Score 5"

    ALL_BUDDIES_LEVEL_1 = "1st Goal Score Achieved in All Cartridges"
    ALL_BUDDIES_LEVEL_2 = "2nd Goal Score Achieved in All Cartridges"
    ALL_BUDDIES_LEVEL_3 = "3rd Goal Score Achieved in All Cartridges"
    ALL_BUDDIES_LEVEL_4 = "4th Goal Score Achieved in All Cartridges"

    FLAT_TIRE = "Flat Tire"

CARTRIDGE_GOAL_SCORE_NAMES: dict[Buddy, list[LocationName]] = {
    Buddy.BUD: [
        LocationName.TRASH_DASH_1, LocationName.TRASH_DASH_2, LocationName.TRASH_DASH_3,
        LocationName.TRASH_DASH_4, LocationName.TRASH_DASH_5
    ],
    Buddy.BIFF: [
        LocationName.HAVE_AT_THEE_1, LocationName.HAVE_AT_THEE_2, LocationName.HAVE_AT_THEE_3,
        LocationName.HAVE_AT_THEE_4, LocationName.HAVE_AT_THEE_5
    ],
    Buddy.BENSON: [
        LocationName.TREATMENT_TO_GO_1, LocationName.TREATMENT_TO_GO_2, LocationName.TREATMENT_TO_GO_3,
        LocationName.TREATMENT_TO_GO_4, LocationName.TREATMENT_TO_GO_5
    ],
    Buddy.BRIE: [
        LocationName.ACROBIRD_1, LocationName.ACROBIRD_2, LocationName.ACROBIRD_3,
        LocationName.ACROBIRD_4, LocationName.ACROBIRD_5
    ],
    Buddy.BAZZ: [
        LocationName.BAZZS_BIG_DAY_1, LocationName.BAZZS_BIG_DAY_2, LocationName.BAZZS_BIG_DAY_3,
        LocationName.BAZZS_BIG_DAY_4, LocationName.BAZZS_BIG_DAY_5
    ],
}

BUDDY_POWER_LOCATION_NAMES: list[LocationName] = [
    LocationName.ALL_BUDDIES_LEVEL_1, LocationName.ALL_BUDDIES_LEVEL_2,
    LocationName.ALL_BUDDIES_LEVEL_3, LocationName.ALL_BUDDIES_LEVEL_4
]


class ItemName(StrEnum):
    BUD_LEVEL_UP = "Bud Progressive Level"
    BIFF_LEVEL_UP = "Biff Progressive Level"
    BENSON_LEVEL_UP = "Benson Progressive Level"
    BRIE_LEVEL_UP = "Brie Progressive Level"
    BAZZ_LEVEL_UP = "Bazz Progressive Level"

    BUDDY_POWER = "Buddy Power Progressive"

    TRASH_DASH_SCORE = "Trash Dash Bonus Points"
    HAVE_AT_THEE_SCORE = "Have At Thee Bonus Points"
    TREATMENT_TO_GO_SCORE = "Treatment To-Go Bonus Points"
    ACROBIRD_SCORE = "Acrobird Bonus Points"
    BAZZS_BIG_DAY_SCORE = "Bazz's Big Day Bonus Points"

LEVEL_UP_NAMES: list[ItemName] = [
    ItemName.BUD_LEVEL_UP, ItemName.BIFF_LEVEL_UP, ItemName.BENSON_LEVEL_UP, ItemName.BRIE_LEVEL_UP, ItemName.BAZZ_LEVEL_UP
]
BONUS_SCORE_NAMES: list[ItemName] = [
    ItemName.TRASH_DASH_SCORE, ItemName.HAVE_AT_THEE_SCORE, ItemName.TREATMENT_TO_GO_SCORE,
    ItemName.ACROBIRD_SCORE, ItemName.BAZZS_BIG_DAY_SCORE
]


class EventName(StrEnum):
    VICTORY = "Victory"
