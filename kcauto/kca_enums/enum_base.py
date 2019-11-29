from enum import Enum


class EnumBase(Enum):
    @property
    def display_name(self):
        return self.value

    @classmethod
    def contains_value(cls, value):
        if value in cls._value2member_map_:
            return True
        return False

    @classmethod
    def get_default(cls):
        return next(iter(cls.__members__.items()))

    @classmethod
    def display_name_to_enum(cls, display_name):
        for member in cls:
            if member.display_name == display_name:
                return member

    @classmethod
    def display_name_to_value(cls, display_name):
        for member in cls:
            if member.display_name == display_name:
                return member.value
