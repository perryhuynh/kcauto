from kca_enums.enum_base import EnumBase


class InteractionModeEnum(EnumBase):
    DIRECT_CONTROL = 'direct_control'
    CHROME_DRIVER = 'chrome_driver'

    @property
    def display_name(self):
        return self.name.replace('_', ' ').title()
