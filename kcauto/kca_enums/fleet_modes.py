from kca_enums.enum_base import EnumBase


class FleetModeEnum(EnumBase):
    STANDARD = 'standard'
    TCF = 'tcf'
    CTF = 'ctf'
    STF = 'stf'

    @property
    def display_name(self):
        if self is self.STANDARD:
            return self.name.title()
        return self.name


class CombinedFleetModeEnum(EnumBase):
    TCF = 'tcf'
    CTF = 'ctf'
    STF = 'stf'
