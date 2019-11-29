from datetime import datetime, timedelta
from pyvisauto import Region
from random import randint

import api.api_core as api
import ships.ships_core as shp
import stats.stats_core as sts
import util.kca as kca_u
from kca_enums.formations import FormationEnum
from kca_enums.kcsapi_paths import KCSAPIEnum
from kca_enums.ship_types import ShipTypeEnum
from util.core_base import CoreBase
from util.kc_time import KCTime
from util.logger import Log


class PvPCore(CoreBase):
    module_name = 'pvp'
    module_display_name = 'PvP'
    available_pvp = []
    next_pvp_time = None

    def __init__(self):
        self.update_from_config()

    def update_from_config(self):
        super().update_from_config()
        self._set_next_pvp_time()

    def update_pvp_list(self, data):
        Log.log_debug("Updating PvP data from API.")
        self.available_pvp = []
        for index, pvp in enumerate(data):
            if pvp['api_state'] == 0:
                self.available_pvp.append(index)

    def time_to_pvp(self):
        if datetime.now() > self.next_pvp_time:
            return True
        return False

    def pvp_available(self):
        if len(self.available_pvp) > 0:
            return True
        self._reset_next_pvp_time()
        return False

    def conduct_pvp(self):
        if len(self.available_pvp) == 0:
            Log.log_msg("No PvP opponents available.")
            return True

        Log.log_msg(f"{len(self.available_pvp)} PvP opponents available.")
        pvp_index = self.available_pvp.pop(0)
        self._conduct_pvp(pvp_index)

        if len(self.available_pvp) == 0:
            self._reset_next_pvp_time()

    def _conduct_pvp(self, index):
        pvp_list_region = Region(
            kca_u.kca.game_x + 280,
            kca_u.kca.game_y + 268 + (index * 82),
            795, 64)
        kca_u.kca.click(pvp_list_region)
        api_result = api.api.update_from_api({KCSAPIEnum.PVP_ENEMY_INFO})
        formation, nb = self._get_formation_and_nb(
            api_result[KCSAPIEnum.PVP_ENEMY_INFO.name][0])
        kca_u.kca.r['top'].hover()
        kca_u.kca.wait_and_click('lower', 'pvp|pvp_start_1.png')
        kca_u.kca.sleep()
        kca_u.kca.wait_and_click('lower', 'pvp|pvp_start_2.png')
        kca_u.kca.sleep()
        sts.stats.pvp.pvp_done += 1

        kca_u.kca.wait_and_click(
            f'formation_{formation.value}',
            f'fleet|formation_{formation.value}.png')
        kca_u.kca.r['top'].hover()

        while not kca_u.kca.exists('lower_right_corner', 'global|next.png'):
            if nb:
                kca_u.kca.click_existing('kc', 'global|combat_nb_fight.png')
            else:
                kca_u.kca.click_existing('kc', 'global|combat_nb_retreat.png')
            kca_u.kca.sleep(2)

        while not kca_u.kca.exists('home_menu', 'nav|home_menu_sortie.png'):
            kca_u.kca.r['shipgirl'].click()
            kca_u.kca.sleep(1)

        Log.log_debug("PvP complete.")
        api.api.update_from_api({KCSAPIEnum.PORT})

    def _get_formation_and_nb(self, api_result):
        ship_count = 0
        sub_count = 0
        for ship in api_result:
            if ship['api_id'] == -1:
                break
            ship_count += 1
            data = shp.ships.get_ship_from_api_id(ship['api_ship_id'])

            if data.ship_type in (ShipTypeEnum.SS, ShipTypeEnum.SSV):
                sub_count += 1

        if sub_count / ship_count >= 0.5:
            return (FormationEnum.LINE_ABREAST, False)
        return (FormationEnum.LINE_AHEAD, True)

    def _set_next_pvp_time(self):
        """Method to set the next PvP time. Called on first instantiation.
        """
        jst_time = KCTime.convert_to_jst(datetime.now())
        if 3 <= jst_time.hour < 5:
            # do not PvP between 3 AM and 5 AM; wait until quests reset at 5AM
            temp_time = jst_time.replace(hour=5)
            self.next_pvp_time = KCTime.convert_from_jst(temp_time)
        else:
            self.next_pvp_time = datetime.now()

    def _reset_next_pvp_time(self):
        """Method to reset the next PvP time. Called when the next PvP time
        needs to be reset in subsequent times.
        """
        jst_time = KCTime.convert_to_jst(datetime.now())
        if 5 <= jst_time.hour < 15:
            temp_time = jst_time.replace(hour=15, minute=randint(5, 15))
        elif 15 <= jst_time.hour < 24:
            temp_time = jst_time + timedelta(days=1)
            temp_time = temp_time.replace(hour=5, minute=randint(5, 15))
        else:
            temp_time = jst_time.replace(hour=5, minute=randint(5, 15))
        self.next_pvp_time = KCTime.convert_from_jst(temp_time)
        Log.log_debug(
            f"Next PvP at {KCTime.datetime_to_str(self.next_pvp_time)}.")


pvp = PvPCore()
