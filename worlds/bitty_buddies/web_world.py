from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_presets


class BittyBuddiesWebWorld(WebWorld):
    game = "Bitty Buddies"

    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Bitty Buddies Archipelago randomizer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ben Morledge-Hampton"],
    )

    tutorials = [setup_en]

    options_presets = option_presets
