from functools import total_ordering

from kca_enums.enum_base import EnumBase


@total_ordering
class DamageStateEnum(EnumBase):
    HEAVY = 4
    MODERATE = 3
    MINOR = 2
    SCRATCH = 1
    NO = 0
    RETREATED = -1
    REPAIRING = -2

    @property
    def display_name(self):
        if self is self.NO:
            return 'No Damage'
        return self.name.title()

    @classmethod
    def get_damage_state_from_hp_percent(cls, hp_percent):
        if hp_percent <= 0.25:
            return cls.HEAVY
        elif hp_percent <= 0.5:
            return cls.MODERATE
        elif hp_percent <= 0.75:
            return cls.MINOR
        elif hp_percent < 1:
            return cls.SCRATCH
        return cls.NO

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
