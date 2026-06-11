from typing import NamedTuple

from .names import RegionName
from .rules import GenericCollectionRule


class Connection(NamedTuple):
    """Describes a connection to another region and the rule necessary to traverse that connection"""
    to: RegionName
    rule: GenericCollectionRule = lambda _int, _options: None

class RegionData(NamedTuple):
    """Data needed to create the region and its connections (besides name)"""
    connections: list[Connection] = []
    hint: str | None = None

# Create a dictionary of RegionData with names as the keys.
region_data_dict: dict[RegionName, RegionData] = {
    RegionName.MENU.value : RegionData()
}
