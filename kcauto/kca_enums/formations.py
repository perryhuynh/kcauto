from kca_enums.enum_base import EnumBase


class FormationEnum(EnumBase):
    LINE_AHEAD = 'line_ahead'
    DOUBLE_LINE = 'double_line'
    DIAMOND = 'diamond'
    ECHELON = 'echelon'
    LINE_ABREAST = 'line_abreast'
    VANGUARD = 'vanguard'
    COMBINED_FLEET_1 = 'combined_fleet_1'
    COMBINED_FLEET_2 = 'combined_fleet_2'
    COMBINED_FLEET_3 = 'combined_fleet_3'
    COMBINED_FLEET_4 = 'combined_fleet_4'

    @property
    def display_name(self):
        return self.name.replace('_', ' ').title()
