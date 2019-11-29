from functools import total_ordering

from kca_enums.enum_base import EnumBase


@total_ordering
class LBASFatigueEnum(EnumBase):
    HEAVY_FATIGUE = 3
    MEDIUM_FATIGUE = 2
    NO_FATIGUE = 1

    def display_name(self):
        return self.name.replace('_', ' ').title()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
