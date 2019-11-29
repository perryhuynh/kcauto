import pyautogui
from pyvisauto import Region, FindFailed
from time import sleep

import config.config_core as cfg
import stats.stats_core as sts
import util.kca as kca_u
from util.logger import Log


pyautogui.FAILSAFE = False


class Recovery(object):
    """Recovery module.
    """
    @classmethod
    def attempt_recovery(cls):
        """Primary method that runs through all the various recovery options.
        Runs through basic recovery, result screen recovery, catbomb recovery,
        then Chrome tab crash recoveries. Typically run when there has been a
        generic Exception caused.

        Returns:
            bool: True if recovery was successful; False otherwise.
        """
        Log.log_warn("Attempting recovery.")

        screen = Region()

        if cls.basic_recovery():
            Log.log_success("Basic Recovery successful.")
            sts.stats.recovery.recoveries_done += 1
            sts.stats.recovery.basic_recoveries_done += 1
            return True

        if (
                kca_u.kca.exists(screen, 'global|next.png')
                or kca_u.kca.exists(screen, 'global|next_alt.png')):
            Log.log_warn("Results screen detected.")
            if cls.recovery_from_results(screen):
                Log.log_success("Results Recovery successful.")
                sts.stats.recovery.recoveries_done += 1
                sts.stats.recovery.results_recoveries_done += 1
                return True
            return False

        if kca_u.kca.exists(screen, 'global|catbomb.png'):
            Log.log_warn("Catbomb detected.")
            if cls.recovery_from_catbomb(screen=screen):
                return True
            else:
                Log.log_error("Catbomb Recovery failed.")
            return False

        if kca_u.kca.exists(screen, 'global|chrome_crash.png'):
            Log.log_warn("Chrome Crash (Type 1) detected.")
            if cls.recovery_from_chrome_crash(screen, crash_type=1):
                return True

        visual_events = kca_u.kca.visual_hook.pop_messages()
        for event in visual_events:
            if event['method'] == 'Inspector.targetCrashed':
                Log.log_warn("Chrome Crash (Type 2) detected.")
                if cls.recovery_from_chrome_crash(screen, crash_type=2):
                    return True

    @staticmethod
    def basic_recovery():
        """Method that contains steps for basic recovery attempt, which
        involves clearing any interaction-blocking browser popups.

        Returns:
            bool: True if recovery was successful; False otherwise.
        """
        Log.log_debug("Attempting Basic Recovery.")

        if cfg.config.general.is_direct_control:
            pyautogui.moveTo(1, 1)
            pyautogui.press('esc')
            sleep(0.5)
            pyautogui.press('space')
            sleep(0.5)
            pyautogui.press('f10')
            sleep(0.5)

        try:
            if kca_u.kca.find_kancolle():
                return True
        except FindFailed:
            pass

        return False

    @staticmethod
    def recovery_from_results(screen):
        """Method that contains steps for recovery attempt from a results
        screen (such as Expedition results screen, combat results screen,
        etc).

        Args:
            screen (Region): screen region.

        Returns:
            bool: True if recovery was successful; False otherwise.
        """
        while (
                kca_u.kca.exists(screen, 'global|next.png')
                or kca_u.kca.exists(screen, 'global|next_alt.png')):
            if kca_u.kca.exists(screen, 'global|next.png', cached=True):
                region = kca_u.kca.find(screen, 'global|next.png', cached=True)
            elif kca_u.kca.exists(screen, 'global|next_alt.png', cached=True):
                region = kca_u.kca.find(
                    screen, 'global|next_alt.png', cached=True)
            region.click()
        if kca_u.kca.exists(screen, 'nav|home_menu_sortie.png'):
            return True
        return False

    @classmethod
    def recovery_from_catbomb(cls, screen=Region(), catbomb_201=False):
        """Method that contains steps for recovery attempt from catbombs. If
        the catbomb_201 flag is set to True the recovery is attempt is far less
        aggressive to not aggravate the fairies any further. Includes
        incremental fallback for retry attempts.

        Args:
            screen (Region, optional): screen region. Defaults to Region().
            catbomb_201 (bool, optional): whether or not this is a 201 catbomb.
                Defaults to False.

        Returns:
            bool: True if recovery was successful; False otherwise.
        """
        catbomb_count = 0 if not catbomb_201 else 2
        if catbomb_201:
            if sts.stats.recovery.catbomb_201_encountered > 0:
                Log.log_error(
                    "Multiple 201 catbombs encountered. Shutting down kcauto.")
                return False
            else:
                kca_u.kca.sleep(300)

        while catbomb_count < 3:
            cls._refresh_screen(screen)
            if kca_u.kca.start_kancolle():
                Log.log_success("Catbomb Recovery successful.")
                kca_u.kca.hook_chrome(port=cfg.config.general.chrome_dev_port)
                sts.stats.recovery.recoveries_done += 1
                if catbomb_201:
                    sts.stats.recovery.catbomb_201_encountered += 1
                    sts.stats.recovery.catbomb_201_recoveries_done += 1
                else:
                    sts.stats.recovery.catbomb_recoveries_done += 1
                return True
            elif kca_u.kca.exists(screen, 'global|catbomb.png'):
                if catbomb_201:
                    Log.log_error(
                        "Persistent 201 catbomb. Shutting down kcauto.")
                    return False

                catbomb_count += 1
                # incremental backoff; 16, 64, then 256 seconds
                sleep_len = pow(4, catbomb_count + 1)
                Log.log_warn(
                    f"Catbomb Recovery attempt {catbomb_count}. Sleeping for "
                    f"{sleep_len} seconds before next recovery attempt.")
                sleep(sleep_len)
            else:
                return False
        return False

    @classmethod
    def recovery_from_chrome_crash(cls, screen=Region(), crash_type=1):
        """Method that contains steps for recovery from Chrome tab crashes.

        Args:
            screen (Region, optional): screen region. Defaults to Region().
            crash_type (int, optional): type of Chrome tab crash encountered.
                Defaults to 1.

        Returns:
            bool: True if recovery was successful; False otherwise.
        """
        cls._refresh_screen(screen)
        if kca_u.kca.start_kancolle():
            Log.log_success("Chrome Crash Recovery successful.")
            sts.stats.recovery.recoveries_done += 1
            if crash_type == 1:
                sts.stats.recovery.chrome_crash_t1_recoveries_done += 1
            elif crash_type == 2:
                sts.stats.recovery.chrome_crash_t2_recoveries_done += 1
            return True
        Log.log_error("Chrome Crash Recovery failed.")
        return False

    @staticmethod
    def _refresh_screen(screen):
        """Helper method that contains steps for refreshing the tab. Includes
        logic to re-instantiate neccessary Chrome hooks.

        Args:
            screen (Region, optional): screen region.
        """
        if cfg.config.general.is_direct_control:
            pyautogui.press('f5')
            sleep(0.5)
            pyautogui.press('space')
            sleep(0.5)
            pyautogui.press('tab')
            sleep(0.5)
            pyautogui.press('space')
            sleep(5)
        else:
            kca_u.kca.visual_hook.Page.reload()
            sleep(0.5)

        kca_u.kca.wait(screen, 'global|game_start.png', 90)
        sleep(3)
