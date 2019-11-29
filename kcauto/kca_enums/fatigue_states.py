from functools import total_ordering

from kca_enums.enum_base import EnumBase


@total_ordering
class FatigueStateEnum(EnumBase):
    HEAVY_FATIGUE = 4
    MEDIUM_FATIGUE = 3
    LIGHT_FATIGUE = 2
    NO_FATIGUE = 1
    SPARKLED = 0

    @property
    def display_name(self):
        return self.name.replace('_', ' ').title()

    @classmethod
    def get_fatigue_state_from_morale(cls, condition):
        if condition <= 19:
            return cls.HEAVY_FATIGUE
        elif 20 <= condition <= 29:
            return cls.MEDIUM_FATIGUE
        elif 30 <= condition <= 39:
            return cls.LIGHT_FATIGUE
        elif 40 <= condition <= 49:
            return cls.NO_FATIGUE
        elif 50 <= condition:
            return cls.SPARKLED

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
