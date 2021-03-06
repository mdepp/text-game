from component import (DescriptionComponent, Direction, FloorComponent,
                       InventoryComponent, OnComponent, PortalComponent,
                       TakeableComponent, WorldDescriptionComponent)
from core import Action, Entity, EntitySpec, World
from util import Query


class TakeAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, TakeableComponent)),

    def apply(self, world: World, entities: list[Entity]):
        entity, = entities
        if entity in world.player[InventoryComponent].items:
            print('You are already carrying that.')
            return
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
            item_names = ', '.join(item[DescriptionComponent].describe_a()
                                   for item in items_on)
            print(f'{entity[DescriptionComponent].describe_the()} contains:'
                  f' {item_names}')

    def rewind(self, world: World):
        pass


class DefaultExamineAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=()),

    def apply(self, world: World, entities: list[Entity]):
        print("It doesn't look like anything to you.")

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
        floor = Query(world).has(FloorComponent).one()
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


class DescribeWorldAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return ()

    def apply(self, world: World, entities: list[Entity]):
        component = next(world.iter_components(WorldDescriptionComponent))
        print(component.description)

        floors = Query(world).has(OnComponent).has(FloorComponent).all()
        for floor in floors:
            for entity in floor[OnComponent].items:
                print(f'There is {entity[DescriptionComponent].describe_a()}'
                      ' here.')

    def rewind(self, world: World):
        pass


class MoveAction(Action):

    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return ()

    def apply(self, world: World, entities: list[Entity]):
        found_portal = False
        for portal in world.iter_components(PortalComponent):
            if portal.direction == self.direction:
                found_portal = True
                world.set_room(portal.room)

        if not found_portal:
            print('You cannot go that way.')

    def rewind(self, world: World):
        raise NotImplementedError()


class EnterAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(PortalComponent, )),

    def apply(self, world: World, entities: list[Entity]):
        portal, = entities
        world.set_room(portal[PortalComponent].room)

    def rewind(self, world: World):
        raise NotImplementedError()


class DefaultEnterAction(Action):

    @staticmethod
    def prerequisites() -> tuple[EntitySpec, ...]:
        return EntitySpec(required=(DescriptionComponent, )),

    def apply(self, world: World, entities: list[Entity]):
        entity, = entities
        name = entity[DescriptionComponent].describe_the()
        print(f'You cannot enter {name}.')

    def rewind(self, world: World):
        pass
