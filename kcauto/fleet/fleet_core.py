import config.config_core as cfg
from fleet.fleet import Fleet
from kca_enums.fleet_modes import FleetModeEnum, CombinedFleetModeEnum
from util.kc_time import KCTime
from util.logger import Log


class FleetCore(object):
    fleets = {}

    def __init__(self):
        self.fleets[1] = Fleet(1, 'combat')
        self.fleets[2] = Fleet(2, 'expedition', False)
        self.fleets[3] = Fleet(3, 'expedition', False)
        self.fleets[4] = Fleet(4, 'expedition', False)

    def update_fleets(self, data):
        Log.log_debug("Updating fleet data from API.")
        fleets_in_data = []
        for fleet_data in data:
            fleet_id = fleet_data['api_id']
            fleets_in_data.append(fleet_id)
            fleet = self.fleets[fleet_id]
            if not fleet.enabled:
                fleet.enabled = True
            if fleet_id == 2:
                fleet.fleet_type = (
                    'combat' if self.combined_fleet else 'expedition')
            if fleet_id == 3:
                fleet.fleet_type = (
                    'combat' if self.strike_force_fleet else 'expedition')
            fleet.ship_ids = fleet_data['api_ship']
            at_base = fleet_data['api_mission'][0] == 0
            if at_base != fleet.at_base:
                fleet.at_base = at_base
            return_time = KCTime.convert_epoch(fleet_data['api_mission'][2])
            if return_time != fleet.return_time:
                fleet.return_time = fleet_data['api_mission'][2]

        remove_fleets = set(fleets_in_data) - set(self.fleets.keys())
        for fleet_id in remove_fleets:
            self.fleets[fleet_id].enabled = False

    @property
    def combat_fleets(self):
        if cfg.config.combat.enabled:
            if cfg.config.combat.fleet_mode is FleetModeEnum.STANDARD:
                return [self.fleets[1]]
            elif cfg.config.combat.fleet_mode is FleetModeEnum.STRIKE:
                return [self.fleets[3]]
            elif CombinedFleetModeEnum.contains_value(
                    cfg.config.combat.fleet_mode.value):
                return [self.fleets[1], self.fleets[2]]
        return []

    @property
    def combined_fleet(self):
        return len(self.combat_fleets) == 2

    @property
    def strike_force_fleet(self):
        return cfg.config.combat.fleet_mode is FleetModeEnum.STRIKE

    @property
    def pvp_fleet(self):
        if cfg.config.pvp.enabled:
            return self.fleets[1]
        return []

    @property
    def ships_in_fleets(self):
        ships = []
        for fleet_id in self.fleets:
            ships.extend(self.fleets[fleet_id].ship_ids)
        return ships

    @property
    def expedition_fleets(self):
        expedition_fleets = []
        if not cfg.config.expedition.enabled:
            return expedition_fleets

        if (
                len(cfg.config.expedition.fleet_2) > 0
                and self.fleets[2].enabled):
            expedition_fleets.append(self.fleets[2])
        if (
                not self.strike_force_fleet
                and len(cfg.config.expedition.fleet_3) > 0
                and self.fleets[3].enabled):
            expedition_fleets.append(self.fleets[3])
        if (
                len(cfg.config.expedition.fleet_4) > 0
                and self.fleets[4].enabled):
            expedition_fleets.append(self.fleets[4])
        return expedition_fleets

    @property
    def combat_ships(self):
        combat_ships = []
        for f in self.combat_fleets:
            combat_ships += f.ship_data
        return combat_ships

    @property
    def active_ships(self):
        active_ships = []
        for fleet_id in self.fleets:
            if self.fleets[fleet_id].enabled:
                active_ships += self.fleets[fleet_id].ship_data
        return active_ships

    def __str__(self):
        for fleet_id in self.fleets:
            fleet = self.fleets[fleet_id]
            if fleet.enabled:
                Log.log_msg(fleet)


fleets = FleetCore()
