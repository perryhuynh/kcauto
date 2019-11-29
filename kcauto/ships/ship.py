from datetime import timedelta

import repair.repair_core as rep
import ships.ships_core as shp
from kca_enums.damage_states import DamageStateEnum
from kca_enums.fatigue_states import FatigueStateEnum
from kca_enums.ship_types import ShipTypeEnum
from util.kc_time import KCTime


class Ship(object):
    _name = None
    api_id = None
    sortno = None
    sort_id = None
    ship_type = None
    local_id = None
    level = None
    hp = None
    hp_max = None
    ammo = None
    ammo_max = None
    fuel = None
    fuel_max = None
    morale = None
    locked = None
    ndock_time_ms = None

    def __init__(self, ship_id, id_type='api_id', local_data=None):
        for ship in shp.ships.ship_library:
            match_id = None
            if id_type == 'api_id':
                match_id = ship['api_id']
            elif id_type == 'sortno':
                match_id = ship['api_sortno']

            if match_id == ship_id:
                self.api_id = ship['api_id']
                self.sortno = ship['api_sortno']
                self.sort_id = ship['api_sort_id']
                self.name = ship['api_name']
                self.ship_type = ShipTypeEnum(ship['api_stype'])
                self.ammo_max = ship['api_bull_max']
                self.fuel_max = ship['api_fuel_max']
                break

        if local_data:
            self.local_id = local_data['api_id']
            self.level = local_data['api_lv']
            self.hp = local_data['api_nowhp']
            self.hp_max = local_data['api_maxhp']
            self.ammo = local_data['api_bull']
            self.fuel = local_data['api_fuel']
            self.morale = local_data['api_cond']
            self.locked = local_data['api_locked'] == 1
            self.ndock_time_ms = local_data['api_ndock_time']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self.api_id in shp.ships.name_db:
            name_db_entry = shp.ships.name_db[self.api_id]
            if name_db_entry['non_jp']:
                value = name_db_entry['non_jp']
            elif name_db_entry['jp']:
                value = name_db_entry['jp']
        self._name = value

    @property
    def hp_p(self):
        return self.hp / self.hp_max

    @property
    def damage(self):
        return self._get_damage_state(self.local_id, self.hp_p)

    @property
    def fatigue(self):
        return FatigueStateEnum.get_fatigue_state_from_morale(self.morale)

    @property
    def ringed(self):
        return self.level >= 100

    @property
    def needs_resupply(self):
        if self.fuel < self.fuel_max:
            return True
        if self.ammo < self.ammo_max:
            return True
        return False

    @needs_resupply.setter
    def needs_resupply(self, value):
        if type(value) is not bool:
            raise TypeError("need resupply value is not bool.")
        if value is True:
            self.ammo = 0
            self.fuel = 0
        else:
            self.ammo = self.ammo_max
            self.fuel = self.fuel_max

    @property
    def under_repair(self):
        if self.damage is DamageStateEnum.REPAIRING:
            return True
        return False

    @property
    def repair_time_delta(self):
        if type(self.ndock_time_ms) is int:
            return KCTime.seconds_to_timedelta(self.ndock_time_ms // 1000)
        return timedelta(seconds=0)

    def repair(self):
        self.hp = self.hp_max

    def _get_damage_state(self, local_id, hp_percent):
        if local_id in rep.repair.ships_under_repair:
            return DamageStateEnum.REPAIRING
        else:
            return DamageStateEnum.get_damage_state_from_hp_percent(
                hp_percent)

    def __repr__(self):
        return (
            f"{self.name} (#{self.sortno}:{self.api_id}:{self.sort_id}) / "
            f"{self.ship_type.name} lvl{self.level} ({self.local_id}) / "
            f"HP:{self.hp}/{self.hp_max} ({self.hp_p:.3n}:"
            f"{self.damage.name}) / "
            f"F:{self.fuel}/{self.fuel_max} / "
            f"A:{self.ammo}/{self.ammo_max} / "
            f"M:{self.morale} ({self.fatigue.name})")
