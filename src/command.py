import re

from core import Command


class RegexCommand(Command):

    def __init__(self, pattern: str | re.Pattern[str]):
        self.pattern = pattern

    def get_entity_names(self, command_string: str) -> list[str] | None:
        match = re.fullmatch(self.pattern, command_string)
        if match is None:
            return None

        return list(match.groups())


class PatternCommand(Command):
    """
    Command defined using a simple help-like syntax, e.g.

        put|place|drop <item> on <item>
        [move|go ]north|n
    """

    def __init__(self, pattern: str):
        pattern = pattern.replace('<item>', r'(?:the )?(\w+(?: \w+)?)')
        pattern = re.sub(r'\b((\w+\|)+(\w+))\b', r'(?:\1)', pattern)
        pattern = re.sub(r'\[(.*?)\]', r'(?:\1)?', pattern)
        pattern = pattern.replace('_', ' ')
        self.command = RegexCommand(pattern)

    def get_entity_names(self, command_string: str) -> list[str] | None:
        return self.command.get_entity_names(command_string)
