from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, TypeVar


class EntityComponent(ABC):
    pass


class Entity:

    def __init__(self, components: list[EntityComponent]):
        self.components = {
            component.__class__.__name__: component
            for component in components
        }

    T = TypeVar("T", bound=EntityComponent)

    def get(self, component_class: Type[T]) -> T | None:
        return self.components.get(component_class.__name__)

    def __getitem__(self, component_class: Type[T]) -> T:
        return self.components[component_class.__name__]

    def __contains__(self, component_class: Type[T]):
        return component_class.__name__ in self.components


class World:

    def __init__(self, player: Entity):
        self.player = player
        self.entities = [player]

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    T = TypeVar('T', bound=EntityComponent)

    def iter_components(self, component_class: Type[T]):
        for entity in self.entities:
            if component_class in entity:
                yield entity[component_class]


class Command(ABC):

    @abstractmethod
    def get_entity_names(self, command_string: str) -> list[str] | None:
        pass


@dataclass
class EntitySpec:
    required: tuple[Type[EntityComponent], ...]

    def matches(self, entity: Entity):
        return all(component_class in entity
                   for component_class in self.required)


class Action(ABC):

    @staticmethod
    @abstractmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        pass

    @abstractmethod
    def apply(self, world: World, entities: list[Entity]) -> bool:
        pass

    @abstractmethod
    def rewind(self, world: World):
        pass
