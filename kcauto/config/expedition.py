from config.config_base import ConfigBase
from kca_enums.expeditions import ExpeditionEnum
from kca_enums.fleet_modes import FleetModeEnum, CombinedFleetModeEnum


class ConfigExpedition(ConfigBase):
    _enabled = False
    _fleet_2 = []
    _fleet_3 = []
    _fleet_4 = []

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['expedition.enabled']
        all_expeditions = (
            config['expedition.fleet_2'] + config['expedition.fleet_3']
            + config['expedition.fleet_4'])
        if len(all_expeditions) != len(set(all_expeditions)):
            raise ValueError("Conflicting expeditions assigned")
        self.fleet_2 = config['expedition.fleet_2']
        self.fleet_3 = config['expedition.fleet_3']
        self.fleet_4 = config['expedition.fleet_4']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for expedition enabled is not a boolean.")
        self._enabled = value

    @property
    def fleet_2(self):
        return self._fleet_2

    @fleet_2.setter
    def fleet_2(self, value):
        if not self._validate_expeditions(value):
            raise ValueError(
                "Specified value for EXPEDITIONS_FLEET2 is not a valid exped")
        if (
                self._config['expedition.enabled']
                and len(value) > 0
                and self._config['combat.enabled']
                and CombinedFleetModeEnum.contains_value(
                    self._config['combat.fleet_mode'])):
            raise ValueError(
                "Fleet 2 cannot be assigned to expeditions when combat is CF")
        self._fleet_2 = [ExpeditionEnum(expedition) for expedition in value]

    @property
    def fleet_3(self):
        return self._fleet_3

    @fleet_3.setter
    def fleet_3(self, value):
        if not self._validate_expeditions(value):
            raise ValueError(
                "Specified value for EXPEDITIONS_FLEET3 is not a valid exped")
        if (
                self._config['expedition.enabled']
                and len(value) > 0
                and self._config['combat.enabled']
                and FleetModeEnum.STRIKE.contains_value(
                    self._config['combat.fleet_mode'])):
            raise ValueError(
                "Fleet 3 cannot be assigned to expeditions when combat is +"
                " strike force")
        self._fleet_3 = [ExpeditionEnum(expedition) for expedition in value]

    @property
    def fleet_4(self):
        return self._fleet_4

    @fleet_4.setter
    def fleet_4(self, value):
        if not self._validate_expeditions(value):
            raise ValueError(
                "Specified value for EXPEDITIONS_FLEET4 is not a valid exped")
        self._fleet_4 = [ExpeditionEnum(expedition) for expedition in value]

    def expeditions_for_fleet(self, value):
        if not 1 < value < 5:
            raise ValueError("Invalid fleet id specified")
        return getattr(self, f'fleet_{value}')

    @property
    def all_expeditions(self):
        return self._fleet_2 + self._fleet_3 + self._fleet_4

    def _validate_expeditions(self, expeditions):
        for expedition in expeditions:
            if not ExpeditionEnum.contains_value(expedition):
                return False
        return True

    @property
    def expedition_fleets(self):
        expedition_fleets = []
        if len(self.fleet_2) > 0:
            expedition_fleets.append(2)
        if len(self.fleet_3) > 0:
            expedition_fleets.append(3)
        if len(self.fleet_4) > 0:
            expedition_fleets.append(4)
        return expedition_fleets
