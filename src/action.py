from component import (DescriptionComponent, FloorComponent,
                       InventoryComponent, OnComponent, TakeableComponent)
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

    def rewind(self, world: World):
        raise NotImplementedError()


class DefaultTakeAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, )),

    def apply(self, world: World, entities: list[Entity]):
        print('You cannot take that.')
        return

    def rewind(self, world: World):
        pass


class ExamineAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, )),

    def apply(self, world: World, entities: list[Entity]):
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

    def rewind(self, world: World):
        pass


class DefaultExamineAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=()),

    def apply(self, world: World, entities: list[Entity]):
        print("It doesn't look like anything to you.")
        return

    def rewind(self, world: World):
        pass


class PutOnAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return (EntitySpec(required=(DescriptionComponent, )),
                EntitySpec(required=(DescriptionComponent, )))

    def apply(self, world: World, entities: list[Entity]):
        subject, object_ = entities
        if subject not in world.player[InventoryComponent].items:
            print('You are not carrying that.')
            return
        if subject == object_:
            print('That is less possible than you might expect.')
            return
        if OnComponent not in object_:
            print('You cannot put anything on '
                  f'{object_[DescriptionComponent].describe_the()}')
            return

        world.player[InventoryComponent].items.remove(subject)
        object_[OnComponent].items.add(subject)
        print(f'You put {subject[DescriptionComponent].describe_the()} on '
              f'{object_[DescriptionComponent].describe_the()}.')

    def rewind(self, world: World):
        raise NotImplementedError()


class DropAction(Action):

    def __init__(self):
        self.put_action = PutOnAction()

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return (EntitySpec(required=(DescriptionComponent, ))),

    def apply(self, world: World, entities: list[Entity]):
        subject, = entities
        floor = None
        for entity in world.entities:
            if FloorComponent in entity:
                floor = entity
                break
        if floor is None:
            raise RuntimeError('Expected a floor to drop things onto')
        return self.put_action.apply(world, [subject, floor])

    def rewind(self, world: World):
        return self.put_action.rewind(world)


class InventoryAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return ()

    def apply(self, world: World, entities: list[Entity]):
        items = world.player[InventoryComponent].items
        if not items:
            print('Your inventory is empty')
            return
        print('Your inventory contains:')
        for item in items:
            print(f' - {item[DescriptionComponent].describe_a()}')

    def rewind(self, world: World):
        pass
