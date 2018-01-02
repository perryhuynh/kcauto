from sikuli import App, Region, Location, Pattern, Key
from time import sleep
from util import Util


class Recovery(object):
    """Recovery module that contains kcauto-kai's recover method (basic, WIP)
    """

    @staticmethod
    def recover(kcauto_kai, e):
        """Attempts very basic recovery actions on a FindFailed exception. WIP
        and does not integrate with the config.

        Args:
            kcauto_kai (KCAutoKai): KCAutoKai instance
            e (Exception): Exception

        Returns:
            bool: True on successful recovery, otherwise raises an error
        """
        kc_region = kcauto_kai.kc_region
        regions = kcauto_kai.regions
        recovery_method = 'kc3'

        Util.log_warning(
            "FindFailed error occurred; attempting basic recovery.")

        App.focus(kcauto_kai.config.program)
        kc_region.mouseMove(Location(1, 1))

        # basic recovery attempt
        type(Key.ESC)
        sleep(1)
        if kc_region.exists(Pattern('kc_reference_point.png').exact()):
            # reference point exists, so we are in-game
            Util.log_success("Recovery successful.")
            kcauto_kai.stats.increment_recoveries()
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
                kcauto_kai.stats.increment_recoveries()
                return True

        # catbomb recovery
        if kc_region.exists('catbomb.png') and recovery_method != 'None':
            if recovery_method == 'browser':
                Region.type(Key.F5)
            elif recovery_method == 'kc3':
                Region.type(Key.F5)
                sleep(1)
                Region.type(Key.SPACE)
                sleep(1)
                Region.type(Key.TAB)
                sleep(1)
                Region.type(Key.SPACE)
            elif recovery_method == 'kcv':
                Region.type(Key.F5)
            elif recovery_method == 'kct':
                Region.type(Key.ALT)
                sleep(1)
                Region.type(Key.DOWN)
                sleep(1)
                Region.type(Key.DOWN)
                sleep(1)
                Region.type(Key.ENTER)
            elif recovery_method == 'eo':
                Region.type(Key.F5)
                sleep(1)
                Region.type(Key.TAB)
                sleep(1)
                Region.type(Key.SPACE)
            sleep(3)
            kc_region.mouseMove(Location(0, 0))
            sleep(3)
            Util.wait_and_click(
                kc_region, Pattern('game_start.png').similar(0.999), 60)
            sleep(5)
            Util.log_success("Recovery successful.")
            kcauto_kai.stats.increment_recoveries()
            return True

        # recovery failed
        Util.log_error("Irrecoverable crash")
        print(e)
        raise
