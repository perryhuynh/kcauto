from datetime import datetime

import config.config_core as cfg
import ships.ships_core as shp
import util.kca as kca_u
from kca_enums.damage_states import DamageStateEnum
from kca_enums.fatigue_states import FatigueStateEnum
from constants import VISUAL_DAMAGE, FLEET_NUMBER_ICON
from util.kc_time import KCTime
from util.logger import Log


class Fleet(object):
    fleet_id = None
    _fleet_type = None
    _enabled = False
    _at_base = True
    _ship_ids = []
    _return_time = None
    ship_data = []
    visual_health = []

    def __init__(self, fleet_id, fleet_type, enabled=True):
        self.fleet_id = fleet_id
        self.enabled = enabled
        self.fleet_type = fleet_type

    def update_ship_data(self):
        self.ship_data = shp.ships.get_local_ships(self.ship_ids)

    def select(self):
        Log.log_debug(f"Selecting fleet {self.fleet_id}.")
        kca_u.kca.click_existing(
            'top_submenu', f'fleet|fleet_{self.fleet_id}.png')
        while not kca_u.kca.exists(
                'top_submenu', f'fleet|fleet_{self.fleet_id}_active.png',
                FLEET_NUMBER_ICON):
            kca_u.kca.click_existing(
                'top_submenu', f'fleet|fleet_{self.fleet_id}.png',
                FLEET_NUMBER_ICON)
        kca_u.kca.sleep()

    @property
    def fleet_type(self):
        return self._fleet_type

    @fleet_type.setter
    def fleet_type(self, value):
        if self.fleet_id == 1 and value != 'combat':
            raise ValueError("Fleet 1 can only be a combat fleet.")
        if value not in ('combat', 'expedition'):
            raise ValueError("Invalid value for fleet type.")
        self._fleet_type = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise TypeError("Fleet enabled is not boolean.")
        print_log = True if value != self._enabled else False
        if value is True and print_log:
            Log.log_success(f"Fleet {self.fleet_id} activated.")
        elif value is False and print_log:
            Log.log_success(f"Fleet {self.fleet_id} deactivated.")
            self._at_base = True
            self._ships = []
            self._return_time = None
            self.ship_data = []
        self._enabled = value

    @property
    def at_base(self):
        return self._at_base

    @at_base.setter
    def at_base(self, value):
        if type(value) is not bool:
            raise TypeError("Fleet at-base location is not a boolean.")
        print_log = True if value != self._enabled else False
        if value is True and print_log:
            Log.log_msg(f"Fleet {self.fleet_id} has arrived at base!")
            for ship in self.ship_data:
                ship.needs_resupply = True
        elif value is False and print_log:
            Log.log_msg(f"Fleet {self.fleet_id} is away on assignment.")
        self._at_base = value

    @property
    def ship_ids(self):
        return self._ship_ids

    @ship_ids.setter
    def ship_ids(self, value):
        if type(value) is not list:
            raise TypeError("Not a list!")
        self._ship_ids = [ship_id for ship_id in value if ship_id > -1]
        self.update_ship_data()

    @property
    def return_time(self):
        return self._return_time

    @return_time.setter
    def return_time(self, value):
        if type(value) is datetime:
            self._return_time = value
        elif value == 0:
            self._return_time = None
        elif type(value) is int:
            self._return_time = KCTime.convert_epoch(value)
            Log.log_msg(
                f"Fleet {self.fleet_id} returns at "
                f"{KCTime.datetime_to_str(self._return_time)}.")
        else:
            raise TypeError("Wrong type for return_time")

    @property
    def needs_resupply(self):
        for ship in self.ship_data:
            if ship.needs_resupply:
                return True
        return False

    @needs_resupply.setter
    def needs_resupply(self, value):
        if type(value) is not bool:
            raise ValueError("NEeds resupply flag is not bool")
        for ship in self.ship_data:
            if value is True:
                ship.needs_resupply = True
            else:
                ship.needs_resupply = False

    @property
    def needs_repair(self):
        for ship in self.ship_data:
            if ship.damage >= cfg.config.combat.repair_limit:
                return True
        return False

    @property
    def under_repair(self):
        for ship in self.ship_data:
            if ship.under_repair:
                return True
        return False

    @property
    def weakest_state(self):
        weakest_state = DamageStateEnum.NO
        for ship in self.ship_data:
            if ship.damage > weakest_state:
                weakest_state = ship.damage
        return weakest_state

    @property
    def highest_fatigue(self):
        highest_fatigue = FatigueStateEnum.SPARKLED
        for ship in self.ship_data:
            if ship.fatigue > highest_fatigue:
                highest_fatigue = ship.fatigue
        return highest_fatigue

    @property
    def lowest_morale(self):
        lowest_morale = 100
        for ship in self.ship_data:
            if ship.morale < lowest_morale:
                lowest_morale = ship.morale
        return lowest_morale

    @property
    def has_returned(self):
        if self.return_time is None:
            return False
        return datetime.now() > self.return_time

    @property
    def combat_fleet_status(self):
        return (
            f"Fleet {self.fleet_id} / "
            f"{self.weakest_state.display_name} fleet damage / "
            f"{self.highest_fatigue.display_name}")

    @property
    def expedition_fleet_status(self):
        return_time_string = ((
                " / Returning at "
                f"{KCTime.datetime_to_str(self.return_time)}")
            if self.return_time
            else "")

        return (
            f"Fleet {self.fleet_id} / "
            f"{'At base' if self.at_base else 'On expedition'}"
            f"{return_time_string}")

    @property
    def detailed_fleet_status(self):
        ship_strings = []
        for ship in self.ship_data:
            ship_strings.append(
                f"{ship.name} ({ship.damage.display_name} damage)")
        return " : ".join(ship_strings)

    def update_ship_hps(self, hps):
        for idx, ship in enumerate(self.ship_data):
            ship.hp = hps[idx]

    def visual_health_check(self, region):
        Log.log_debug(f"Running visual health check of fleet {self.fleet_id}.")

        find_heavy = kca_u.kca.find_all(
            region, 'fleet|ship_state_dmg_heavy.png', VISUAL_DAMAGE)
        heavy = len(find_heavy)

        find_moderate = kca_u.kca.find_all(
            region, 'fleet|ship_state_dmg_moderate.png', VISUAL_DAMAGE, True)
        moderate = len(find_moderate)

        find_minor = kca_u.kca.find_all(
            region, 'fleet|ship_state_dmg_minor.png', VISUAL_DAMAGE, True)
        minor = len(find_minor)

        self.visual_health = {
            'heavy': heavy,
            'moderate': moderate,
            'minor': minor
        }
        Log.log_debug(f"Visual health check results: {self.visual_health}")
        return self.visual_health

    def __str__(self):
        if self.fleet_type == 'combat':
            return self.combat_fleet_status
        else:
            return self.expedition_fleet_status
