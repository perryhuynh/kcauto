import fleet.fleet_core as flt
import nav.nav as nav
import stats.stats_core as sts
import util.kca as kca_u
from util.logger import Log


class ResupplyCore(object):
    exp_provisional_enabled = None

    def __init__(self):
        pass

    def goto(self):
        nav.navigate.to('resupply')

    @property
    def need_to_resupply(self):
        fleets = [fleet.fleet_id for fleet in self._get_fleets_to_resupply()]
        if len(fleets) == 1:
            Log.log_msg(f"Fleet {fleets[0]} needs resupply.")
            return True
        elif len(fleets) > 1:
            display_text = kca_u.kca.readable_list_join(fleets)
            Log.log_msg(f"Fleets {display_text} need resupply.")
            return True
        return False

    def resupply_fleets(self):
        fleets = self._get_fleets_to_resupply()
        for fleet in fleets:
            Log.log_msg(f"Resupplying Fleet {fleet.fleet_id}.")
            fleet.select()
            resupply_button = kca_u.kca.wait(
                'upper_left', 'resupply|resupply_all.png')
            resupply_button.hover()
            while not kca_u.kca.exists(
                    'lower_right', 'resupply|resupply_all_done.png'):
                resupply_button.click()
                kca_u.kca.sleep(0.2)
            kca_u.kca.r['top'].hover()
            sts.stats.resupply.resupplies_done += 1
            kca_u.kca.sleep()

    def exp_provisional_resupply(self, fleet):
        if kca_u.kca.click_existing(
                'lower_right', 'resupply|expedition_resupply_fairy.png'):
            self.exp_provisional_enabled = True
            kca_u.kca.wait_vanish(
                'lower_right', 'resupply|expedition_resupply_fairy.png')
            fleet.needs_resupply = False
            kca_u.kca.sleep(0.5)
            sts.stats.resupply.provisional_resupplies_done += 1
            return True
        if self.exp_provisional_enabled is None:
            self.exp_provisional_enabled = False
        return False

    def _get_fleets_to_resupply(self):
        fleets_to_resupply = []
        for fleet_id in flt.fleets.fleets:
            fleet = flt.fleets.fleets[fleet_id]
            if fleet.enabled and fleet.needs_resupply:
                fleets_to_resupply.append(fleet)
        return fleets_to_resupply


resupply = ResupplyCore()
