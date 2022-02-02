import argparse
import logging

import logzero

from action import (DefaultEnterAction, DefaultExamineAction,
                    DefaultTakeAction, DescribeWorldAction, DropAction,
                    EnterAction, ExamineAction, InventoryAction, MoveAction,
                    PutOnAction, TakeAction)
from command import PatternCommand
from component import (DescriptionComponent, Direction, FloorComponent,
                       InventoryComponent, OnComponent, PortalComponent,
                       TakeableComponent, WorldDescriptionComponent)
from core import Action, Command, Entity, Room, World
from util import CommandInterpretationError, interpret_command


def make_command_to_action():
    take_command = PatternCommand('take|pick_up|grab|get <item>')
    examine_command = PatternCommand('examine|x|look_at|l|describe <item>')
    put_command = PatternCommand('put|place|drop <item> on <item>')
    drop_command = PatternCommand('drop <item>')
    inventory_command = PatternCommand('inventory|i')
    describe_world_command = PatternCommand('examine|x|look|look_around|l')

    move_north_command = PatternCommand('[move|go|travel|m ]n|north')
    move_east_command = PatternCommand('[move|go|travel|m ]e|east')
    move_south_command = PatternCommand('[move|go|travel|m ]s|south')
    move_west_command = PatternCommand('[move|go|travel|m ]w|west')

    enter_command = PatternCommand(
        'enter|move_through|walk_through|go_through|travel_through <item>')

    command_to_action: list[tuple[Command, Action]] = [
        (take_command, TakeAction()),
        (take_command, DefaultTakeAction()),
        (examine_command, ExamineAction()),
        (examine_command, DefaultExamineAction()),
        (put_command, PutOnAction()),
        (drop_command, DropAction()),
        (inventory_command, InventoryAction()),
        (describe_world_command, DescribeWorldAction()),
        (move_north_command, MoveAction(Direction.N)),
        (move_east_command, MoveAction(Direction.E)),
        (move_south_command, MoveAction(Direction.S)),
        (move_west_command, MoveAction(Direction.W)),
        (enter_command, EnterAction()),
        (enter_command, DefaultEnterAction()),
    ]
    return command_to_action


def make_world():
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

    room1 = Room()
    room2 = Room()

    key = Entity([
        DescriptionComponent(names=['iron key'],
                             description='A rusty iron key'),
        TakeableComponent(),
    ])
    room1.add_entity(key)
    room1.add_entity(
        Entity([
            DescriptionComponent(names=['floor', 'ground']),
            OnComponent({key}),
            FloorComponent(),
        ]))
    room1.add_entity(
        Entity([
            WorldDescriptionComponent(
                'You are on a floor in an infinite featureless plain.'
                ' On the eastern edge of the plain looms an ethereal doorframe,'
                ' beyond which you only see blackness.')
        ]))
    room1.add_entity(
        Entity([
            DescriptionComponent(names=['infinite featureless plain'],
                                 description='It is featureless.')
        ]))
    room1.add_entity(
        Entity([
            DescriptionComponent(
                names=['ethereal door', 'ethereal doorframe'],
                description='Beyond the door there is only blackness.'),
            PortalComponent(room=room2, direction=Direction.E),
        ]))

    room2.add_entity(
        Entity([
            WorldDescriptionComponent(
                'It is very dark here. You cannot see or feel anything.')
        ]))

    world.add_room(room1)
    world.add_room(room2)
    world.set_room(room1)
    return world


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if not args.verbose:
        logzero.loglevel(logging.FATAL)

    command_to_action = make_command_to_action()
    world = make_world()

    current_room = None
    while True:
        if world.current_room != current_room:
            DescribeWorldAction().apply(world, [])
            current_room = world.current_room
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
