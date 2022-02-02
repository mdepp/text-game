import re
from enum import Enum

from core import Entity, EntityComponent, Room


class DescriptionComponent(EntityComponent):

    def __init__(self, names: list[str], description: str | None = None):
        self.names = names
        self.description = description

    def describe_the(self) -> str:
        if self.names[0].startswith('the '):
            return self.names[0]
        else:
            return f'the {self.names[0]}'

    def describe_a(self) -> str:
        if self.names[0].startswith('the'):
            return self.names[0]
        elif self.names[0].startswith('a '):
            return self.names[0]
        elif self.names[0][0] in 'aeiou':
            return f'an {self.names[0]}'
        else:
            return f'a {self.names[0]}'

    def matches(self, text: str):
        for name in self.names:
            if re.search(r'\b' + re.escape(text) + r'\b', name) is not None:
                return True
        return False


class WorldDescriptionComponent(EntityComponent):

    def __init__(self, description: str):
        self.description = description


class InventoryComponent(EntityComponent):

    def __init__(self):
        self.items: list[Entity] = []


class OnComponent(EntityComponent):

    def __init__(self, items: set[Entity] | None = None):
        self.items = items or set()


class TakeableComponent(EntityComponent):
    pass


class FloorComponent(EntityComponent):
    pass


class Direction(Enum):
    N = 'north'
    NE = 'north-east'
    E = 'east'
    SE = 'south-east'
    S = 'south'
    SW = 'south-west'
    W = 'west'
    NW = 'north-west'
    UP = 'up'
    DOWN = 'down'
    NONE = 'none'


class PortalComponent(EntityComponent):

    def __init__(self, room: Room, direction: Direction):
        self.room = room
        self.direction = direction
