from sikuli import App, Region, Location, Pattern, Key
from time import sleep
from util import Util


class Recovery(object):
    """Recovery module that contains kcauto's recover method (basic, WIP)
    """

    @staticmethod
    def recover(kcauto, config, e):
        """Attempts very basic recovery actions on a FindFailed exception. WIP
        and does not integrate with the config.

        Args:
            kcauto (KCAuto): KCAuto instance
            config (Config): Config instance
            e (Exception): Exception

        Returns:
            bool: True on successful recovery, otherwise raises an error
        """
        kc_region = (
            kcauto.kc_region if kcauto.kc_region
            else Util.focus_kc(config))
        kc_region = kcauto.kc_region
        regions = kcauto.regions

        Util.log_warning(e)
        Util.log_warning(
            "** FindFailed error occurred; attempting basic recovery. **")

        App.focus(kcauto.config.program)
        kc_region.mouseMove(Location(1, 1))

        # basic recovery attempt
        Region.type(kc_region, Key.ESC)
        sleep(1)
        Region.type(kc_region, Key.SPACE)
        if kc_region.exists(Pattern('kc_reference_point.png').exact()):
            # reference point exists, so we are in-game
            Util.log_success("Recovery successful.")
            kcauto.stats.increment_recoveries()
            return True
        elif kc_region.exists('next.png'):
            # crashed at some results screen; try to click it away until we see
            # the main game screen
            while (kc_region.exists('next.png') and
                    not kc_region.exists(
                        Pattern('kc_reference_point.png').exact())):
                Util.click_preset_region(regions, 'center')
                sleep(2)
            if kc_region.exists(Pattern('kc_reference_point.png').exact()):
                # reference point exists, so we are back in-game
                Util.log_success("Recovery successful.")
                kcauto.stats.increment_recoveries()
                return True

        # catbomb recovery
        if kc_region.exists('catbomb.png', 10):
            Util.log_warning("** Catbomb detected. **")
            catbombed = True
            catbomb_n = 0
            while catbombed and catbomb_n < 7:
                # generic f5-space-tab-space keystrokes to mimick refresh
                # attempt
                Region.type(kc_region, Key.F5)
                sleep(1)
                Region.type(kc_region, Key.SPACE)
                sleep(1)
                Region.type(kc_region, Key.TAB)
                sleep(1)
                Region.type(kc_region, Key.SPACE)
                sleep(3)
                # clear mouse
                kc_region.mouseMove(Location(1, 1))
                if kc_region.exists('catbomb.png'):
                    sleep_len = pow(2, catbomb_n + 4)
                    Util.log_warning(
                        "Catbomb recovery attempt {} failed; trying again in "
                        "{} seconds!".format(catbomb_n + 1, sleep_len))
                    sleep(sleep_len)
                    catbomb_n += 1
                else:
                    catbombed = False
            sleep(3)
            Util.wait_and_click(
                kc_region, Pattern('game_start.png').similar(0.999), 60)
            sleep(5)
            Util.log_success("Catbomb recovery successful.")
            kcauto.stats.increment_recoveries()
            return True

        # recovery failed
        Util.log_error("** Irrecoverable crash. **")
        print(e)
        raise
