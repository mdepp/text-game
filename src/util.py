from typing import Type

from logzero import logger

from component import DescriptionComponent
from core import Action, Command, Entity, EntityComponent, World


class Query:

    def __init__(self, world: World, component_classes=None):
        self.world = world
        self.component_classes = component_classes or []

    def has(self, component_class: Type[EntityComponent]):
        return Query(self.world, self.component_classes + [component_class])

    def all(self):
        for entity in self.world.entities:
            if all(component_class in entity
                   for component_class in self.component_classes):
                yield entity

    def one(self):
        entity, = self.all()
        return entity


def lookup_entities(world: World, entity_name: str) -> list[Entity]:
    matching_entities = []
    for entity in Query(world).has(DescriptionComponent).all():
        if entity[DescriptionComponent].matches(entity_name):
            matching_entities.append(entity)

    return matching_entities


class CommandInterpretationError(Exception):

    def __init__(self, message: str):
        super().__init__(f'Could not interpret command: {message}')
        self.message = message


def interpret_command(world: World, command_to_action: list[tuple[Command,
                                                                  Action]],
                      command_string: str) -> tuple[Action, list[Entity]]:

    for command, action in command_to_action:
        entity_names = command.get_entity_names(command_string)
        if entity_names is None:
            continue

        logger.info('Command: %s', command)
        logger.info('Action: %s', action)
        logger.info('Entity names: %s', entity_names)

        entities = []
        for entity_name in entity_names:
            matching_entities = lookup_entities(world, entity_name)
            logger.info(
                'Name %s matched %d entities: %s', entity_name,
                len(matching_entities),
                [e[DescriptionComponent].names[0] for e in matching_entities])
            if len(matching_entities) == 1:
                entities.extend(matching_entities)
            elif len(matching_entities) == 0:
                raise CommandInterpretationError(
                    'No objects match that description')
            else:
                raise CommandInterpretationError(
                    'Multiple objects match that description')

        entity_specs = action.prerequisites()
        if len(entity_specs) != len(entities):
            logger.warning(
                'Command has %d entities but action expects %d, skipping',
                len(entities), len(entity_specs))
            continue

        spec_matches = False
        for entity_spec, entity in zip(entity_specs, entities):
            if not entity_spec.matches(entity):
                logger.info('Entity %s does not match spec %s, skipping',
                            entity, entity_spec)
                spec_matches = True
                break
        if spec_matches:
            continue

        return action, entities

    raise CommandInterpretationError('Invalid command.')
