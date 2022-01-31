from component import (DescriptionComponent, InventoryComponent, OnComponent,
                       TakeableComponent)
from core import Action, Entity, EntitySpec, World


class TakeAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, TakeableComponent)),

    def apply(self, world: World, entities: list[Entity]):
        entity, = entities
        world.player[InventoryComponent].items.append(entity)
        for on_component in world.iter_components(OnComponent):
            if entity in on_component.items:
                on_component.items.remove(entity)
        print(f'You take {entity[DescriptionComponent].describe_the()}')
        return True

    def rewind(self, world: World):
        raise NotImplementedError()


class DefaultTakeAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, )),

    def apply(self, world: World, entities: list[Entity]) -> bool:
        print('You cannot take that.')
        return False

    def rewind(self, world: World):
        pass


class ExamineAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, )),

    def apply(self, world: World, entities: list[Entity]) -> bool:
        entity, = entities
        print(entity[DescriptionComponent].description)
        return True

    def rewind(self, world: World):
        pass


class DefaultExamineAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=()),

    def apply(self, world: World, entities: list[Entity]) -> bool:
        print("It doesn't look like anything to you.")
        return False

    def rewind(self, world: World):
        pass
