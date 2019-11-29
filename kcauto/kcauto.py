import combat.combat_core as com
import config.config_core as cfg
import expedition.expedition_core as exp
import fleet_switcher.fleet_switcher_core as fsw
import nav.nav as nav
import pvp.pvp_core as pvp
import quest.quest_core as qst
import repair.repair_core as rep
import resupply.resupply_core as res
import scheduler.scheduler_core as sch
import ship_switcher.ship_switcher_core as ssw
import stats.stats_core as sts
import util.kca as kca_u
from util.logger import Log


class Kcauto(object):
    """Primary kcauto class.
    """
    end_loop_at_port = False

    def __init__(self):
        kca_u.kca.hook_chrome(port=cfg.config.general.chrome_dev_port)

    def start_kancolle(self):
        kca_u.kca.start_kancolle()

    def find_kancolle(self):
        kca_u.kca.find_kancolle()

    def hook_health_check(self):
        kca_u.kca.hook_health_check()

    def check_config(self):
        if cfg.config.config_changed:
            Log.log_msg("Config change detected. Loading updated config.")
            if cfg.config.initialize_config():
                com.combat.update_from_config()
                exp.expedition.update_from_config()
                pvp.pvp.update_from_config()
                qst.quest.update_from_config()
                sch.scheduler.update_from_config()

    def initialization_check(self):
        if sts.stats.rsc.ammo is None:
            Log.log_msg("kcauto is initializing.")
            if not exp.expedition.receive_expedition():
                nav.navigate.to('refresh_home')
                sts.stats.set_print_loop_end_stats()

    def check_for_expedition(self):
        if not exp.expedition.receive_expedition():
            if exp.expedition.expect_returned_fleets():
                nav.navigate.to('refresh_home')
                exp.expedition.receive_expedition()
                sts.stats.set_print_loop_end_stats()

    def fast_check_for_expedition(self):
        exp.expedition.receive_expedition()

    def run_expedition_logic(self):
        if not exp.expedition.enabled:
            return False

        if exp.expedition.expect_returned_fleets():
            self.find_kancolle()
            nav.navigate.to('home')
            self.fast_check_for_expedition()

        if exp.expedition.fleets_are_ready:
            nav.navigate.to('home')
            self.fast_check_for_expedition()
            exp.expedition.goto()
            exp.expedition.send_expeditions()
            sts.stats.set_print_loop_end_stats()

    def run_pvp_logic(self):
        if not pvp.pvp.enabled:
            return False

        if pvp.pvp.time_to_pvp():
            self.find_kancolle()
            self.fast_check_for_expedition()
            self.run_quest_logic('pvp')
            nav.navigate.to('home')
            self.fast_check_for_expedition()
            self._run_fleetswitch_logic('pvp')
            self.run_resupply_logic(home_after=True)
            sts.stats.set_print_loop_end_stats()
        else:
            return False

        pvp.pvp.goto()
        while pvp.pvp.pvp_available():
            pvp.pvp.conduct_pvp()
            self.run_resupply_logic(home_after=True)
            self.run_quest_logic('pvp', fast_check=True, home_after=True)
            if pvp.pvp.pvp_available():
                pvp.pvp.goto()
        sts.stats.set_print_loop_end_stats()
        return True

    def run_combat_logic(self):
        if not com.combat.enabled:
            return False

        if com.combat.time_to_sortie:
            self.find_kancolle()
            self.fast_check_for_expedition()
            nav.navigate.to('refresh_home')
            self.fast_check_for_expedition()
        else:
            return False

        if com.combat.should_and_able_to_sortie:
            self.find_kancolle()
            self.fast_check_for_expedition()
            self.run_quest_logic('combat', fast_check=True)
            nav.navigate.to('home')
            self.fast_check_for_expedition()
            self._run_fleetswitch_logic('combat')
            if com.combat.should_and_able_to_sortie:
                com.combat.goto()
                if com.combat.conduct_sortie():
                    sts.stats.set_print_loop_end_stats()
                    self.fast_check_for_expedition()

    def run_resupply_logic(self, home_after=False):
        if res.resupply.need_to_resupply:
            self.find_kancolle()
            self.fast_check_for_expedition()
            res.resupply.goto()
            res.resupply.resupply_fleets()
            self.handle_home_after(home_after)
            if not home_after:
                self.end_loop_at_port = True
            sts.stats.set_print_loop_end_stats()

    def run_repair_logic(self, home_after=False):
        if rep.repair.can_conduct_repairs:
            self.find_kancolle()
            self.fast_check_for_expedition()
            rep.repair.goto()
            rep.repair.repair_ships()
            self.handle_home_after(home_after)
            if not home_after:
                self.end_loop_at_port = True
            sts.stats.set_print_loop_end_stats()

    def _run_fleetswitch_logic(self, context):
        if fsw.fleet_switcher.require_fleetswitch(context):
            fsw.fleet_switcher.goto()
            fsw.fleet_switcher.switch_fleet(context)
            self.handle_home_after(True)

    def run_shipswitch_logic(self, home_after=False):
        if ssw.ship_switcher.need_to_switch:
            nav.navigate.to('home')
            self.fast_check_for_expedition()
            ssw.ship_switcher.goto()
            ssw.ship_switcher.switch_ships()
            self.handle_home_after(home_after)
            if not home_after:
                self.end_loop_at_port = True

    def run_quest_logic(
            self, context=None, fast_check=False, home_after=False):
        if not qst.quest.enabled:
            return False

        if qst.quest.need_to_check(context):
            self.find_kancolle()
            self.fast_check_for_expedition()
            qst.quest.goto()
            qst.quest.manage_quests(context, fast_check)
            sts.stats.quest.times_checked += 1
            self.handle_home_after(home_after)
            sts.stats.set_print_loop_end_stats()

    def handle_home_after(self, home_after):
        if home_after:
            nav.navigate.to('home')
            self.fast_check_for_expedition()

    def run_scheduler(self):
        sch.scheduler.check_and_process_rules()

    def check_end_loop_at_port(self):
        if self.end_loop_at_port:
            self.end_loop_at_port = False
            self.handle_home_after(True)

    @property
    def scheduler_kca_active(self):
        return sch.scheduler.kca_active

    def print_stats(self):
        if sts.stats.print_loop_end_stats:
            sts.stats.loop_count += 1
            sts.stats.print_stats()


kcauto = Kcauto()
