from kca_enums.enum_base import EnumBase


class LBASStateEnum(EnumBase):
    STANDBY = 0
    SORTIE = 1
    AIR_DEFENSE = 2
    RETREAT = 3
    REST = 4

    @property
    def display_name(self):
        return self.name.replace('_', ' ').title()
