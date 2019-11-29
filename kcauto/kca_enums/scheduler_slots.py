from kca_enums.enum_base import EnumBase


class SchedulerSlot0Enum(EnumBase):
    TIME = 'time'
    TIME_RUN = 'time_run'
    SORTIES_RUN = 'sorties_run'
    EXPEDITIONS_RUN = 'expeditions_run'
    PVP_RUN = 'pvp_run'
    RESCUE = 'rescue'
    DOCKS_FULL = 'docks_full'
    CLEAR_STOP = 'clear_stop'

    @property
    def display_name(self):
        if self is self.PVP_RUN:
            return 'PvP Run'
        return self.name.replace('_', ' ').title()


class SchedulerSlot2Enum(EnumBase):
    SLEEP = 'sleep'
    STOP = 'stop'

    @property
    def display_name(self):
        return self.name.title()


class SchedulerSlot3Enum(EnumBase):
    KCAUTO = 'kcauto'
    COMBAT_MODULE = 'combat'
    EXPEDITION_MODULE = 'expedition'
    PVP_MODULE = 'pvp'

    @property
    def display_name(self):
        if self is self.KCAUTO:
            return self.value
        elif self is self.PVP_MODULE:
            return 'PvP Module'
        return self.name.replace('_', ' ').title()
