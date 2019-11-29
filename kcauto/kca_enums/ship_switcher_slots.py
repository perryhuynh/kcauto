from kca_enums.enum_base import EnumBase


class ShipSwitcherConditionSlot0Enum(EnumBase):
    LEVEL = 'level'
    DAMAGE = 'damage'
    MORALE = 'morale'

    @property
    def display_name(self):
        return self.name.title()


class ShipSwitcherCriteriaSlot0Enum(EnumBase):
    SHIP = 'ship'
    CLASS = 'class'

    @property
    def display_name(self):
        return self.name.title()


class ShipSwitcherCriteriaSlot8Enum(EnumBase):
    NA = ''
    LOCKED = 'locked'
    UNLOCKED = 'unlocked'

    @property
    def display_name(self):
        if self is self.NA:
            return 'N/A'
        return self.name.title()


class ShipSwitcherCriteriaSlot9Enum(EnumBase):
    NA = ''
    RINGED = 'ringed'
    NOT_RINGED = 'not_ringed'

    @property
    def display_name(self):
        if self is self.NA:
            return 'N/A'
        return self.name.replace('_', ' ').title()


class ShipSwitcherOperatorEnum(EnumBase):
    LT = '<'
    GT = '>'
    LE = '<='
    GE = '>='
    EQ = '=='
    NE = '!='
