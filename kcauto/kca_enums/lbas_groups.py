from kca_enums.enum_base import EnumBase


class LBASGroupEnum(EnumBase):
    G01 = 1
    G02 = 2
    G03 = 3

    @property
    def display_name(self):
        return self.value
