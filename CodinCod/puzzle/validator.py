from dataclasses import dataclass

from ..piston import piston, Language

from .validator_type import ValidatorType
from ..piston.language import Language
from pistonapi.exceptions import PistonError

@dataclass
class Validator:
    type: ValidatorType
    input: str
    output: str

    async def execute(self, code: str, language: Language, retry_limit: int = 2) -> tuple[bool, str]:
        # TODO: this function is blocking, so everything will stop working until the code finishes executing!!
        # pistonapi library in itself is blocking we need to use threads or change pistonapi.
        lang = language.name
        version = language.version
        for _ in range(retry_limit):
            try:
                output: str = piston.execute(
                    lang, version, code, self.input, timeout = 1000)
                return output.rstrip() == self.output.rstrip(), output
            except PistonError:
                continue

        return (False, "Internal error")

    def as_dict(self) -> dict:
        """
        Return a represention of the game room that can be sent
        to the client.
        """

        return {
            "validator_type": self.type.value,
            "input": self.input,
            "output": self.output,
        }
