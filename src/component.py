import re

from core import Entity, EntityComponent


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


class InventoryComponent(EntityComponent):

    def __init__(self):
        self.items: list[Entity] = []


class OnComponent(EntityComponent):

    def __init__(self, items: set[Entity] | None = None):
        self.items = items or set()


class TakeableComponent(EntityComponent):
    pass
