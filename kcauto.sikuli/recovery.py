import org.sikuli.script.FindFailed as FindFailed
from sikuli import App, Region, Location, Pattern, Key, FOREVER
from abc import ABCMeta
from time import sleep
from util import Util
from kca_globals import Globals


class Recovery(object):
    """Recovery module that contains kcauto's recovery method. Supports
    dealing with dialogue popups, lingering KC3Kai overlays, catbombs, and
    chrome tab crashes.
    """

    @staticmethod
    def recover(kcauto, config, e):
        """Attempts very basic recovery actions on a FindFailed exception.

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
        sleep(1)
        Region.type(kc_region, Key.F10)  # clear KC3Kai overlay
        sleep(1)
        if (kc_region.exists(Pattern('kc_ref_point_1.png').exact())
                or kc_region.exists(Pattern('kc_ref_point_2.png').exact())
                or kc_region.exists(Pattern('kc_ref_point_3.png').exact())):
            # reference point exists, so we are in-game
            Util.log_success("Recovery successful.")
            kcauto.stats.increment_recoveries()
            return True
        elif kc_region.exists('next.png') or kc_region.exists('next_alt.png'):
            # crashed at some results screen; try to click it away until we see
            # the main game screen
            while ((kc_region.exists('next.png')
                    or kc_region.exists('next_alt.png'))
                    and not kc_region.exists(
                        Pattern('home_menu_sortie.png').exact())):
                Util.click_preset_region(regions, 'shipgirl')
                sleep(2)
            if kc_region.exists(Pattern('home_menu_sortie.png').exact()):
                # reference point exists, so we are back in-game
                Util.log_success("Recovery successful.")
                kcauto.stats.increment_recoveries()
                return True

        # Chrome crash recovery
        if ('chrome' in Globals.ENABLED_RECOVERIES):
            if kc_region.exists('chrome_crash.png'):
                Util.log_warning("** Chrome crash detected. **")
                Region.type(kc_region, Key.F5)
                sleep(1)
                Region.type(kc_region, Key.SPACE)
                Util.wait_and_click(
                    kc_region, Pattern('game_start.png').similar(0.999), 120)
                Util.log_success("Re-starting game.")
                kc_region.wait('home_menu_resupply.png', 60)
                Util.log_success("Chrome crash recovery successful.")
                kcauto.stats.increment_recoveries()
                return True

        # catbomb recovery
        if ('catbomb' in Globals.ENABLED_RECOVERIES):
            if kc_region.exists('catbomb.png', 60):
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
                            "Catbomb recovery attempt {} failed; trying again "
                            "in {} seconds!".format(catbomb_n + 1, sleep_len))
                        sleep(sleep_len)
                        catbomb_n += 1
                    else:
                        catbombed = False
                sleep(5)
                Util.wait_and_click(
                    kc_region, Pattern('game_start.png').similar(0.999), 120)
                Util.log_success("Re-starting game.")
                kc_region.wait('home_menu_resupply.png', 60)
                Util.log_success("Catbomb recovery successful.")
                kcauto.stats.increment_recoveries()
                return True

        # recovery failed
        Util.log_error("** Irrecoverable crash. **")
        print(e)
        raise


class RecoverableModule:
    """Abstract class used by modules that need a background observer to detect
    catbomb and chrome crashes. Provides a set of inheritable class variables
    and methods to be used in the child classes.
    """
    __metaclass__ = ABCMeta

    crash_detected = False

    def _start_crash_observer(self):
        """Method that starts the observeInBackground to check for catbombs
        and chrome crashes.
        """
        self.kc_region.onAppear('catbomb.png', self._set_crash_detected)
        self.kc_region.onAppear('chrome_crash.png', self._set_crash_detected)
        self.kc_region.observeInBackground(FOREVER)

    def _stop_crash_observer(self):
        """Method that stops the observer in the absence of valid observer
        event.
        """
        self.kc_region.stopObserver()

    def _set_crash_detected(self, event):
        """Method that sets the class variable indicating that a crash has been
        detected, stopping the observer as needed.
        """
        Util.log_warning("** Crash detected. **")
        event.region.stopObserver()
        self.crash_detected = True

    def _check_and_recovery_crash(self, observed_regions=()):
        """Method that raises the FindFailed exception based on the value of
        the class variable indicating a detected crash. Any region that has
        ongoing observers should be passed in as part of a list/tuple so
        their observers can be stopped before raising the exception. Call this
        from the primary process.

        Args:
            observed_regions (tuple, optional): Defaults to (). List of regions
                that have ongoing observers

        Raises:
            FindFailed: Catbomb or Chrome crash detected
        """

        if self.crash_detected:
            for observed_region in observed_regions:
                observed_region.stopObserver()
            raise FindFailed(None)
