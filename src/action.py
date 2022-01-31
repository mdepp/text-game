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
        description = entity[DescriptionComponent].description
        if OnComponent in entity:
            items_on = entity[OnComponent].items
        else:
            items_on = set()

        if description is not None:
            print(description)
        if description is None and len(items_on) == 0:
            print("It doesn't look like anything to you.")
        if items_on:
            print(
                f"{entity[DescriptionComponent].describe_the()} contains: {', '.join(item[DescriptionComponent].describe_a() for item in items_on)}"
            )
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


class PutOnAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return (EntitySpec(required=(DescriptionComponent, )),
                EntitySpec(required=(DescriptionComponent, )))

    def apply(self, world: World, entities: list[Entity]) -> bool:
        subject, object_ = entities
        if subject not in world.player[InventoryComponent].items:
            print('You are not carrying that.')
            return False
        if subject == object_:
            print('That is less possible than you might expect.')
            return False
        if OnComponent not in object_:
            print('You cannot put anything on '
                  f'{object_[DescriptionComponent].describe_the()}')
            return False

        world.player[InventoryComponent].items.remove(subject)
        object_[OnComponent].items.add(subject)
        print(f'You put {subject[DescriptionComponent].describe_the()} on '
              f'{object_[DescriptionComponent].describe_the()}.')
        return True

    def rewind(self, world: World):
        raise NotImplementedError()


class InventoryAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return ()

    def apply(self, world: World, entities: list[Entity]) -> bool:
        items = world.player[InventoryComponent].items
        if not items:
            print('Your inventory is empty')
            return True
        print('Your inventory contains:')
        for item in items:
            print(f' - {item[DescriptionComponent].describe_a()}')
        return True

    def rewind(self, world: World):
        pass
