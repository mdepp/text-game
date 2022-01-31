from action import (DefaultExamineAction, DefaultTakeAction, ExamineAction,
                    TakeAction)
from command import SimpleVerbCommand
from component import DescriptionComponent, InventoryComponent
from core import Action, Command, Entity, World
from util import CommandInterpretationError, interpret_command


def main():
    take_command = SimpleVerbCommand('take', 'pick up', 'grab', 'get')
    examine_command = SimpleVerbCommand('examine', 'x', 'look at', 'l',
                                        'describe')
    command_to_action: list[tuple[Command, Action]] = [
        (take_command, TakeAction()), (take_command, DefaultTakeAction()),
        (examine_command, ExamineAction()),
        (examine_command, DefaultExamineAction())
    ]

    world = World(player=Entity([
        InventoryComponent(),
        DescriptionComponent(names=['player', 'me', 'self', 'myself'],
                             description="It's just you")
    ]))

    command_string = input('> ')

    try:
        action, entities = interpret_command(world, command_to_action,
                                             command_string)
        action.apply(world, entities)
    except CommandInterpretationError as err:
        print(err.message)


if __name__ == '__main__':
    main()
