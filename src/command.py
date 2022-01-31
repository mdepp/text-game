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


class SimpleVerbCommand(Command):

    def __init__(self, *verbs: str):
        verbs_pattern = '|'.join(re.escape(verb) for verb in verbs)
        pattern = re.compile(rf'(?:{verbs_pattern})(?: the)? (\w+(?: \w+)?)')
        self.command = RegexCommand(pattern)

    def get_entity_names(self, command_string: str) -> list[str] | None:
        return self.command.get_entity_names(command_string)
