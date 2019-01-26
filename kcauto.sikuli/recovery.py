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

    @classmethod
    def recover(cls, kcauto, config, e):
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
            kcauto.stats.increment_basic_recoveries()
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
                kcauto.stats.increment_basic_recoveries()
                return True

        # check viable recoveries
        if kc_region.exists('chrome_crash.png', 30):
            if cls._handle_chrome(kcauto, kc_region):
                return True
        if kc_region.exists('catbomb.png', 30):
            if cls._handle_catbomb(kcauto, kc_region):
                return True
        if kc_region.exists(Pattern('whitescreen.png').exact(), 30):
            if cls._handle_whitescreen(kcauto, kc_region):
                return True

        # recovery failed
        Util.log_error("** Irrecoverable crash. **")
        print(e)
        raise

    @classmethod
    def _handle_catbomb(cls, kcauto, kc_region):
        """Checks whether or not catbomb recovery is enabled, and starts or
        defers recovery accordingly.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a successful recovery was done; False otherwise
        """
        if ('catbomb' in Globals.ENABLED_RECOVERIES):
            return cls._perform_catbomb_recovery(kcauto, kc_region)
        else:
            Util.log_error(
                "** Catbomb detected, but catbomb recovery is disabled. **")
            return False

    @classmethod
    def _handle_chrome(cls, kcauto, kc_region):
        """Checks whether or not chrome crash recovery is enabled, and starts
        or defers recovery accordingly.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a successful recovery was done; False otherwise
        """
        if ('chrome' in Globals.ENABLED_RECOVERIES):
            return cls._perform_chrome_recovery(kcauto, kc_region)
        else:
            Util.log_error(
                "** Chrome crash detected, but Chrome crash recovery is "
                "disabled. **")
            return False

    @classmethod
    def _handle_whitescreen(cls, kcauto, kc_region):
        """Checks whether or not whitescreen recovery is enabled, and starts or
        defers recovery accordingly.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a successful recovery was done; False otherwise
        """
        if ('whitescreen' in Globals.ENABLED_RECOVERIES):
            return cls._perform_whitescreen_recovery(kcauto, kc_region)
        else:
            Util.log_error(
                "** Whitescreen detected, but whitescreen recovery is "
                "disabled.")
            return False

    @classmethod
    def _perform_catbomb_recovery(cls, kcauto, kc_region):
        """Method to perform catbomb recovery.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a successful recovery was done; False otherwise
        """
        Util.log_warning("** Catbomb detected. **")
        catbombed = True
        catbomb_n = 0
        while catbombed and catbomb_n < 7:
            cls._refresh_keystrokes(kc_region)
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
        if cls._start_kancolle(kcauto, kc_region):
            Util.log_success("Catbomb recovery successful.")
            kcauto.stats.increment_recoveries()
            kcauto.stats.increment_catbomb_recoveries()
            return True
        return False

    @classmethod
    def _perform_chrome_recovery(cls, kcauto, kc_region):
        """Method to perform chrome tab crash recovery.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a successful recovery was done; False otherwise
        """
        Util.log_warning("** Chrome crash detected. **")
        cls._refresh_keystrokes(kc_region)
        if cls._start_kancolle(kcauto, kc_region):
            Util.log_success("Chrome crash recovery successful.")
            kcauto.stats.increment_recoveries()
            kcauto.stats.increment_chrome_recoveries()
            return True
        return False

    @classmethod
    def _perform_whitescreen_recovery(cls, kcauto, kc_region):
        """Method to perform whitescreen crash recovery.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a successful recovery was done; False otherwise
        """
        Util.log_warning("** Whitescreen crash detected. **")
        cls._refresh_keystrokes(kc_region)
        if cls._start_kancolle(kcauto, kc_region):
            Util.log_success("Whitescreen crash recovery successful.")
            kcauto.stats.increment_recoveries()
            kcauto.stats.increment_whitescreen_recoveries()
            return True
        return False

    @classmethod
    def _start_kancolle(cls, kcauto, kc_region):
        """Method to check and restart the game from the splash screen. If a
        whitescreen is detected at this point, whitescreen recovery will be
        performed, if enabled.

        Args:
            kcauto (KCAuto): KCAuto instance
            kc_region (Region): Sikuli game region

        Returns:
            bool: True if a game was successfully restarted; False otherwise
        """
        if kc_region.exists(Pattern('game_start.png').similar(0.999), 120):
            # game refreshed properly
            Util.check_and_click(kc_region, 'game_start.png')
            Util.log_success("Restarting game.")
            kc_region.wait('home_menu_resupply.png', 60)
            Util.log_success("Game restarted.")
            return True
        elif kc_region.exists(Pattern('whitescreen.png').exact(), 30):
            return cls._handle_whitescreen(kcauto, kc_region)
        return False

    @staticmethod
    def _refresh_keystrokes(kc_region):
        """Fires off generic F5-space-tab-space keystrokes to mimick a refresh
        attempt applicable to most browsers/viewers.

        Args:
            kc_region (Region): Sikuli game region
        """
        Region.type(kc_region, Key.F5)
        sleep(1)
        Region.type(kc_region, Key.SPACE)
        sleep(1)
        Region.type(kc_region, Key.TAB)
        sleep(1)
        Region.type(kc_region, Key.SPACE)
        sleep(5)
        # clear mouse
        kc_region.mouseMove(Location(1, 1))


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
