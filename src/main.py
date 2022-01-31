from action import (DefaultExamineAction, DefaultTakeAction, DropAction,
                    ExamineAction, InventoryAction, PutOnAction, TakeAction)
from command import PatternCommand, SimpleVerbCommand
from component import (DescriptionComponent, FloorComponent,
                       InventoryComponent, OnComponent, TakeableComponent)
from core import Action, Command, Entity, World
from util import CommandInterpretationError, interpret_command


def main():
    take_command = SimpleVerbCommand('take', 'pick up', 'grab', 'get')
    examine_command = SimpleVerbCommand('examine', 'x', 'look at', 'l',
                                        'describe')
    put_command = PatternCommand('put|place|drop <item> on <item>')
    drop_command = PatternCommand('drop <item>')
    inventory_command = PatternCommand('inventory|i')

    command_to_action: list[tuple[Command, Action]] = [
        (take_command, TakeAction()),
        (take_command, DefaultTakeAction()),
        (examine_command, ExamineAction()),
        (examine_command, DefaultExamineAction()),
        (put_command, PutOnAction()),
        (drop_command, DropAction()),
        (inventory_command, InventoryAction()),
    ]

    world = World(player=Entity([
        InventoryComponent(),
        DescriptionComponent(names=['player', 'me', 'self', 'myself'],
                             description="It's just you")
    ]))
    world.add_entity(
        Entity([
            DescriptionComponent(names=['you', 'narrator'],
                                 description='Who, me?')
        ]))
    key = Entity([
        DescriptionComponent(names=['iron key'],
                             description='A rusty iron key'),
        TakeableComponent(),
    ])
    world.add_entity(key)
    world.add_entity(
        Entity([
            DescriptionComponent(names=['floor', 'ground']),
            OnComponent({key}),
            FloorComponent(),
        ]))

    while True:
        command_string = input('> ')
        if command_string == 'exit':
            break

        try:
            action, entities = interpret_command(world, command_to_action,
                                                 command_string)
            action.apply(world, entities)
        except CommandInterpretationError as err:
            print(err.message)


if __name__ == '__main__':
    main()
