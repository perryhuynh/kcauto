from kca_enums.enum_base import EnumBase


class EventDifficultyEnum(EnumBase):
    HARD = 4
    NORMAL = 3
    EASY = 2
    CASUAL = 1
    NONE = 0

    @property
    def display_name(self):
        return self.name.title()
