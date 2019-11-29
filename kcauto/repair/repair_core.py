from datetime import datetime, timedelta
from pyvisauto import Region

import api.api_core as api
import combat.combat_core as com
import config.config_core as cfg
import fleet.fleet_core as flt
import nav.nav as nav
import ships.ships_core as shp
import stats.stats_core as sts
import util.kca as kca_u
from kca_enums.damage_states import DamageStateEnum
from kca_enums.kcsapi_paths import KCSAPIEnum
from util.kc_time import KCTime
from util.logger import Log


class RepairCore(object):
    complete_times = []
    ships_under_repair = []
    docks_count = 0
    docks_available_count = 0
    current_repair_list_page = 1

    def __init__(self):
        pass

    def goto(self):
        nav.navigate.to('repair')
        self.current_repair_list_page = 1

    @property
    def docks_are_available(self):
        self._clean_timers()
        if self.docks_available_count > 0:
            return True
        return False

    @property
    def can_conduct_repairs(self):
        if self.docks_are_available:
            if cfg.config.combat.enabled and self.fleets_need_repair:
                return True
            if cfg.config.passive_repair.enabled and self.ships_need_repair:
                if (
                        cfg.config.passive_repair.slots_to_reserve
                        >= self.docks_available_count):
                    return False
                return True
        return False

    @property
    def soonest_complete_time(self):
        self._clean_timers()
        sorted_timers = sorted(self.complete_times)
        return sorted_timers[0]

    def _clean_timers(self):
        # ships_under_repair will go out of sync with this until port check
        new_complete_times = []
        for timer in self.complete_times:
            if timer > datetime.now():
                new_complete_times.append(timer)
            else:
                self.docks_available_count += 1
        self.complete_times = new_complete_times

    def update_repair_data(self, data):
        Log.log_debug("Updating Repair data from API.")
        self.docks_count = 0
        self.docks_available_count = 0
        self.complete_times = []
        self.ships_under_repair = []
        for dock_data in data:
            if dock_data['api_state'] > -1:
                self.docks_count += 1
            if dock_data['api_state'] == 0:
                self.docks_available_count += 1
            if dock_data['api_state'] == 1:
                self.complete_times.append(
                    KCTime.convert_epoch(dock_data['api_complete_time']))
                self.ships_under_repair.append(dock_data['api_ship_id'])

    def repair_ships(self):
        repair_list = self._local_ships_sorted_by_repair
        idx_of_combat_ships = {}
        idx_of_passive_ships = {}
        for idx, ship in enumerate(repair_list):
            if ship.damage is DamageStateEnum.REPAIRING:
                continue
            elif ship in flt.fleets.combat_ships:
                if ship.damage >= cfg.config.combat.repair_limit:
                    idx_of_combat_ships[idx] = ship
            elif cfg.config.passive_repair.enabled:
                if ship.damage >= cfg.config.passive_repair.repair_threshold:
                    if ship not in flt.fleets.active_ships:
                        idx_of_passive_ships[idx] = ship

        if len(idx_of_combat_ships) + len(idx_of_passive_ships) == 0:
            Log.log_debug("No combat or passive ships to repair.")
            return False

        while self.can_conduct_repairs:
            Log.log_debug(
                f"Combat repair index: {idx_of_combat_ships.keys()}")
            Log.log_debug(
                f"Passive repair index: {idx_of_passive_ships.keys()}")

            idx, ship, context = self._select_idx_and_ship(
                idx_of_combat_ships, idx_of_passive_ships)
            self._select_dock()
            self._check_repair_sort()
            self._select_ship(idx, ship)
            bucketed = self._start_repair(ship, context)
            if idx in idx_of_combat_ships:
                com.combat.set_next_sortie_time(
                    idx_of_combat_ships[idx].repair_time_delta)
                del idx_of_combat_ships[idx]
            elif idx in idx_of_passive_ships:
                del idx_of_passive_ships[idx]

            if bucketed:
                ship.repair()
                idx_of_combat_ships = self._shift_idx_list_based_on_idx(
                    idx_of_combat_ships, idx)
                idx_of_passive_ships = self._shift_idx_list_based_on_idx(
                    idx_of_passive_ships, idx)
                sts.stats.repair.buckets_used += 1

            kca_u.kca.wait('left', 'nav|side_menu_home.png')
            kca_u.kca.sleep(0.5)

    def _select_idx_and_ship(self, idx_of_combat_ships, idx_of_passive_ships):
        if len(idx_of_combat_ships) > 0:
            idx = list(idx_of_combat_ships.keys())[0]
            ship = idx_of_combat_ships.pop(idx)
            return (idx, ship, 'combat')
        if len(idx_of_passive_ships) > 0:
            idx = list(idx_of_passive_ships.keys())[0]
            ship = idx_of_passive_ships.pop(idx)
            return (idx, ship, 'passive')

    def _shift_idx_list_based_on_idx(self, idx_list, idx):
        new_idx_list = {}
        for lidx in idx_list:
            if lidx > idx:
                new_idx_list[lidx - 1] = idx_list[lidx]
            else:
                new_idx_list[lidx] = idx_list[lidx]
        return new_idx_list

    def _select_dock(self):
        kca_u.kca.wait_and_click('left', 'repair|empty_dock.png')
        kca_u.kca.sleep(1)

    def _check_repair_sort(self):
        if not kca_u.kca.exists('upper_right', 'repair|repairlist_icon.png'):
            Log.log_msg("Changing repair list sort.")
            sort_button = Region(
                kca_u.kca.game_x + 1125, kca_u.kca.game_y + 155, 58, 26)
            while not kca_u.kca.exists(
                    'upper_right', 'repair|repairlist_icon.png'):
                sort_button.click()

    def _select_ship(self, idx, ship):
        page = (idx // 10) + 1 if idx > 9 else 1
        Log.log_msg(f"Selecting lvl{ship.level} {ship.name} (pg{page}#{idx}).")
        if page > 1:
            tot_pages = shp.ships.current_ship_count // 10
            list_control_region = Region(
                kca_u.kca.game_x + 610, kca_u.kca.game_y + 660, 490, 45)
            nav.navigate_list.to_page(
                list_control_region, tot_pages, self.current_repair_list_page,
                page, 'repair')
            self.current_repair_list_page = page
        repair_list_region = Region(
            kca_u.kca.game_x + 596,
            kca_u.kca.game_y + 194 + (idx % 10 * 46),
            500, 31)
        kca_u.kca.click(repair_list_region)
        kca_u.kca.r['top'].hover()
        kca_u.kca.wait('right', 'repair|repair_confirm_1.png')

    def _start_repair(self, ship, context):
        bucketed = False
        Log.log_msg(
            "Ship repair time of "
            f"{KCTime.timedelta_to_str(ship.repair_time_delta)}.")
        if context == 'combat' and self._ship_needs_bucket(ship):
            Log.log_msg("Using bucket to repair.")
            kca_u.kca.click_existing(
                'right', 'repair|bucket_switch.png', cached=True)
            bucketed = True
        kca_u.kca.click_existing(
            'right', 'repair|repair_confirm_1.png', cached=True)
        kca_u.kca.r['top'].hover()
        kca_u.kca.wait_and_click('lower', 'repair|repair_confirm_2.png')
        kca_u.kca.r['top'].hover()
        api.api.update_from_api({KCSAPIEnum.REPAIR_DOCKS})
        sts.stats.repair.repairs_done += 1
        if context == 'passive':
            sts.stats.repair.passive_repairs_done += 1
        return bucketed

    def _ship_needs_bucket(self, ship):
        repair_timelimit = timedelta(
            hours=cfg.config.combat.repair_timelimit_hours,
            minutes=cfg.config.combat.repair_timelimit_minutes)
        if ship.repair_time_delta > repair_timelimit:
            return True
        return False

    @property
    def _local_ships_sorted_by_repair(self):
        return sorted(
            [s for s in shp.ships.local_ships if s.hp_p < 1],
            key=lambda s: (s.hp_p, s.sort_id, s.local_id))

    @property
    def fleets_need_repair(self):
        if cfg.config.combat.enabled:
            for fleet in flt.fleets.combat_fleets:
                if fleet.needs_repair:
                    return True
        return False

    @property
    def ships_need_repair(self):
        if cfg.config.passive_repair.enabled:
            for ship in shp.ships.local_ships:
                if ship.damage >= cfg.config.passive_repair.repair_threshold:
                    if ship not in flt.fleets.active_ships:
                        return True
        return False


repair = RepairCore()
