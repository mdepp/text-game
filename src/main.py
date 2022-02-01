import argparse
import logging

import logzero

from action import (DefaultExamineAction, DefaultTakeAction,
                    DescribeWorldAction, DropAction, ExamineAction,
                    InventoryAction, PutOnAction, TakeAction)
from command import PatternCommand, SimpleVerbCommand
from component import (DescriptionComponent, FloorComponent,
                       InventoryComponent, OnComponent, TakeableComponent,
                       WorldDescriptionComponent)
from core import Action, Command, Entity, Room, World
from util import CommandInterpretationError, interpret_command


def make_command_to_action():
    take_command = SimpleVerbCommand('take', 'pick up', 'grab', 'get')
    examine_command = SimpleVerbCommand('examine', 'x', 'look at', 'l',
                                        'describe')
    put_command = PatternCommand('put|place|drop <item> on <item>')
    drop_command = PatternCommand('drop <item>')
    inventory_command = PatternCommand('inventory|i')
    describe_world_command = PatternCommand('examine|x|look|look_around|l')

    command_to_action: list[tuple[Command, Action]] = [
        (take_command, TakeAction()),
        (take_command, DefaultTakeAction()),
        (examine_command, ExamineAction()),
        (examine_command, DefaultExamineAction()),
        (put_command, PutOnAction()),
        (drop_command, DropAction()),
        (inventory_command, InventoryAction()),
        (describe_world_command, DescribeWorldAction()),
    ]
    return command_to_action


def make_world():
    world = World(player=Entity([
        InventoryComponent(),
        DescriptionComponent(names=['player', 'me', 'self', 'myself'],
                             description="It's just you")
    ]))
    room = Room()
    room.add_entity(
        Entity([
            DescriptionComponent(names=['you', 'narrator'],
                                 description='Who, me?')
        ]))
    key = Entity([
        DescriptionComponent(names=['iron key'],
                             description='A rusty iron key'),
        TakeableComponent(),
    ])
    room.add_entity(key)
    room.add_entity(
        Entity([
            DescriptionComponent(names=['floor', 'ground']),
            OnComponent({key}),
            FloorComponent(),
        ]))
    room.add_entity(
        Entity([
            WorldDescriptionComponent(
                'You are on a floor in an infinite featureless plain.')
        ]))
    room.add_entity(
        Entity([
            DescriptionComponent(names=['infinite featureless plain'],
                                 description='It is featureless.')
        ]))
    world.add_room(room)
    world.set_room(room)
    return world


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if not args.verbose:
        logzero.loglevel(logging.FATAL)

    command_to_action = make_command_to_action()
    world = make_world()

    DescribeWorldAction().apply(world, [])
    while True:
        try:
            command_string = input('> ')
        except EOFError:
            break
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
