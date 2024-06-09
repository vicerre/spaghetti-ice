import re
from dataclasses import dataclass
from typing import Dict


@dataclass
class Replacements:
    innerpattern: str
    outerpattern: str
    replacements: Dict[str, str]

    @staticmethod
    def from_dict(d: Dict[str, str]):
        return Replacements(
            innerpattern="|".join(d.keys()),
            outerpattern="|".join(rf"[\W_]{key}[\W_]" for key in d.keys()),
            replacements=d,
        )

    def _replaceinner(self, s: str) -> str:
        if self.innerpattern == "":
            return s
        return re.sub(
            self.innerpattern, lambda match: self.replacements[match.group(0)], s
        )

    def _replaceouter(self, s: str) -> str:
        if self.outerpattern == "":
            return s
        return re.sub(
            self.outerpattern, lambda match: self._replaceinner(match.group(0)), s
        )

    def multikeyreplace(self, s: str) -> str:
        return self._replaceouter(s)

    def multititlereplace(self, s: str) -> str:
        return self._replaceinner(s)
