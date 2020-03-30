import os
import PyChromeDevTools
from datetime import datetime, timedelta
from pyvisauto import Region, FindFailed, ImageMatch
from random import randint, uniform
from time import sleep

import api.api_core as api
import args.args_core as arg
import config.config_core as cfg
import ships.ships_core as shp
import util.click_tracker as clt
from constants import (
    GAME_W, GAME_H, VISUAL_URL, API_URL, EXACT, DEFAULT, SLEEP_MODIFIER)
from kca_enums.interaction_modes import InteractionModeEnum
from kca_enums.kcsapi_paths import KCSAPIEnum
from util.exceptions import ChromeCrashException
from util.logger import Log


class Kca(object):
    """Primary kcauto utility class.
    """
    ASSETS_FOLDER = 'assets'
    visual_hook = None
    api_hook = None
    game_x = None
    game_y = None
    last_ui = None
    r = {}

    def __init__(self):
        Log.log_debug("Kca module initialized.")

    def hook_chrome(self, host="localhost", port=9222):
        """Method that initializes the necessary hooks to Chrome using
        PyChromeDevTools. The visual hook connects to the tab that actually
        contains the Kancolle HTML5 canvas, while the api hook connects to the
        tab that interacts with the Kancolle backend. The former is used for
        detecting refreshes and when using the Chrome driver interaction mode,
        while the latter is used for reading all API interactions.

        Args:
            host (str, optional): Chrome dev protocol server address. Defaults
                to "localhost".
            port (int, optional): Chrome dev protocol server port. Defaults to
                9222.

        Raises:
            Exception: could not find Kancolle tabs in Chrome.
        """
        Log.log_msg("Hooking into Chrome.")
        self.visual_hook = PyChromeDevTools.ChromeInterface(
            host=host, port=port)
        self.api_hook = PyChromeDevTools.ChromeInterface(host=host, port=port)

        visual_tab = None
        visual_tab_id = None
        api_tab = None
        api_tab_id = None
        for n, tab in enumerate(self.visual_hook.tabs):
            if tab['url'] == VISUAL_URL:
                visual_tab = n
                visual_tab_id = tab['id']
            if API_URL in tab['url']:
                api_tab = n
                api_tab_id = tab['id']

        if visual_tab_id is None or api_tab_id is None:
            Log.log_error(
                "No Kantai Collection tab found in Chrome. Shutting down "
                "kcauto.")
            raise Exception(
                "No running Kantai Collection tab found in Chrome.")

        self.visual_hook.connect_targetID(visual_tab_id)
        Log.log_debug(
            f"Connected to visual tab ({visual_tab}:{visual_tab_id})")
        self.visual_hook.Page.enable()

        self.api_hook.connect_targetID(api_tab_id)
        self.api_hook.Network.enable()
        Log.log_debug(f"Connected to API tab ({api_tab}:{api_tab_id})")
        Log.log_success("Connected to Chrome")

    def hook_health_check(self):
        """Method that runs through the different events reported to the api
        and visual hooks to ascertain whether or not the tab has crashed or
        was refreshed.

        Raises:
            ChromeCrashException: Chrome tab crash was detected.
        """
        api_events = self.api_hook.pop_messages()
        visual_events = self.visual_hook.pop_messages()
        for event in api_events:
            if event['method'] == 'Inspector.detached':
                Log.log_warn("Chrome API hook is stale. Reconnecting.")
                self.hook_chrome(port=cfg.config.general.chrome_dev_port)
                return
        visual_events = self.visual_hook.pop_messages()
        for event in visual_events:
            if event['method'] == 'Page.frameDetached':
                Log.log_warn("Chrome visual hook is stale. Reconnecting.")
                self.hook_chrome(port=cfg.config.general.chrome_dev_port)
                return
            if event['method'] == 'Inspector.targetCrashed':
                Log.log_warn("Chrome crash detected.")
                raise ChromeCrashException

    def start_kancolle(self):
        """Method that attempts to start Kancolle from the game's splash
        screen. If starting from the splash screen, kcauto will load the data
        from the get_data api call. Otherwise, it will load the stored data
        from previous startups.
        """
        screen = Region()
        if self.click_existing(screen, 'global|game_start.png'):
            Log.log_msg("Starting kancolle from splash screen.")
            api.api.update_from_api({
                KCSAPIEnum.GET_DATA, KCSAPIEnum.REQUIRE_INFO, KCSAPIEnum.PORT})
            self.wait(screen, 'nav|home_menu_sortie.png', 60)
            Log.log_success("Kancolle successfully started.")
            shp.ships.load_wctf_names(force_update=True)
        else:
            api.api.update_ship_library_from_json()
        self.sleep()

        return True

    def find_kancolle(self):
        """Method that finds the Kancolle game on-screen and determine the UI
        being used as well as the position of the game. On first startup the
        method will look for all UIs until one is found; on subsequent runs
        it will first look for the last found UI. Generates or modifies
        pre-defined regions accordingly.

        Raises:
            FindFailed: could not find the game on-screen.
        """
        Log.log_msg("Finding kancolle.")
        ref_r = None
        attempt = 0
        screen = Region()

        # look for last-seen UI, if set
        if self.last_ui:
            try:
                ref_r = self.find(
                    screen, f'global|kc_ref_point_{self.last_ui}.png', EXACT)
            except FindFailed:
                self.last_ui = None
                Log.log_debug("Last known UI not found.")

        # if last-seen UI was not found, or if kcauto is in first start
        while not ref_r:
            try:
                ref_r = self.find(screen, 'global|kc_ref_point_1.png', EXACT)
                self.last_ui = 1
                Log.log_debug("Using UI 1 or 2")
                break
            except FindFailed:
                Log.log_debug("Not using UI 1 or 2")
            try:
                ref_r = self.find(screen, 'global|kc_ref_point_2.png', EXACT)
                self.last_ui = 2
                Log.log_debug("Using UI 3")
                break
            except FindFailed:
                Log.log_debug("Not using UI 3")
            try:
                ref_r = self.find(screen, 'global|kc_ref_point_3.png', EXACT)
                self.last_ui = 3
                Log.log_debug("Using UI 4 or 5")
                break
            except FindFailed:
                Log.log_debug("Not using UI 4 or 5")
            attempt += 1
            sleep(1)
            if attempt > 3:
                Log.log_error("Could not find Kancolle reference point.")
                raise FindFailed()

        new_game_x = ref_r.x - 144
        new_game_y = ref_r.y
        Log.log_debug(f"Game X:{new_game_x}, Y:{new_game_y}")

        # define click callback as needed
        if not arg.args.parsed_args.no_click_track:
            ImageMatch.click_callback = clt.click_tracker.track_click

        # define click and hover method overrides as needed
        if (cfg.config.general.interaction_mode
                is InteractionModeEnum.CHROME_DRIVER):
            ImageMatch.override_click_method = self._override_click_method
            ImageMatch.override_hover_method = self._override_hover_method

        if new_game_x != self.game_x or new_game_y != self.game_y:
            if not self.game_x or self.game_y:
                Log.log_success("Game found. Initializing regions.")
            else:
                Log.log_msg("Game has moved. Shifting regions.")
            self.game_x = new_game_x
            self.game_y = new_game_y
            self._update_regions()

        return True

    def _update_regions(self):
        """Method that generates or updates all pre-defined regions
        accordingly based on the game's current x and y position.
        """
        Log.log_debug("Updating regions.")
        x = self.game_x
        y = self.game_y
        w = GAME_W
        h = GAME_H
        hw = w / 2
        hh = h / 2

        # general regions
        self._create_or_shift_region('kc', x, y, w, h)
        self._create_or_shift_region('left', x, y, hw, h)
        self._create_or_shift_region('right', x + hw, y, hw, h)
        self._create_or_shift_region('upper', x, y, w, hh)
        self._create_or_shift_region('lower', x, y + hh, w, hh)
        self._create_or_shift_region('upper_left', x, y, hw, hh)
        self._create_or_shift_region('upper_right', x + hw, y, hw, hh)
        self._create_or_shift_region('lower_left', x, y + hh, hw, hh)
        self._create_or_shift_region('lower_right', x + hw, y + hh, hw, hh)
        self._create_or_shift_region(
            'lower_right_corner', x + 1100, y + 620, 100, 100)
        self._create_or_shift_region('center', x + 225, y + 180, 750, 360)
        self._create_or_shift_region('top', x + 400, y + 12, 800, 30)
        self._create_or_shift_region('shipgirl', x + 700, y + 130, 400, 420)
        self._create_or_shift_region(
            'combat_click', x + 700, y + 680, 200, 30)
        # function-specific regions
        self._create_or_shift_region(
            'expedition_flag', x + 750, y + 20, 70, 50)
        self._create_or_shift_region('top_menu', x + 185, y + 50, 800, 50)
        self._create_or_shift_region(
            'top_menu_quest', x + 790, y + 50, 105, 45)
        self._create_or_shift_region('home_menu', x + 45, y + 130, 500, 490)
        self._create_or_shift_region('side_menu', x, y + 190, 145, 400)
        self._create_or_shift_region(
            'top_submenu', x + 145, y + 145, 1055, 70)
        self._create_or_shift_region(
            'quest_status', x + 1065, y + 165, 95, 500)
        self._create_or_shift_region(
            'check_damage_combat', x + 470, y + 215, 50, 475)
        self._create_or_shift_region('lbas', x + 500, y + 5, 200, 45)
        self._create_or_shift_region(
            'lbas_mode_switch', x + 1135, y + 200, 55, 80)
        self._create_or_shift_region('7th_next', x + 386, y + 400, 27, 27)
        # combat-related regions
        self._create_or_shift_region(
            'formation_line_ahead', x + 596, y + 256, 250, 44)
        self._create_or_shift_region(
            'formation_double_line', x + 791, y + 256, 250, 44)
        self._create_or_shift_region(
            'formation_diamond', x + 989, y + 256, 150, 44)
        self._create_or_shift_region(
            'formation_echelon', x + 596, y + 495, 252, 44)
        self._create_or_shift_region(
            'formation_line_abreast', x + 791, y + 495, 253, 44)
        self._create_or_shift_region(
            'formation_vanguard', x + 989, y + 495, 150, 44)
        self._create_or_shift_region(
            'formation_combined_fleet_1', x + 640, y + 240, 215, 45)
        self._create_or_shift_region(
            'formation_combined_fleet_2', x + 890, y + 240, 215, 45)
        self._create_or_shift_region(
            'formation_combined_fleet_3', x + 640, y + 445, 215, 45)
        self._create_or_shift_region(
            'formation_combined_fleet_4', x + 890, y + 445, 215, 45)

    def _create_or_shift_region(self, key, x, y, w, h):
        """Helper method for generating or shifting an existing Region's x
        and y position.

        Args:
            key (str): region key.
            x (int): x position of upper-left corner of Region.
            y (int): y position of upper-left corner of Region.
            w (int): width of Region.
            h (int): height of Region.
        """
        if key not in self.r or not isinstance(self.r[key], Region):
            self.r[key] = Region(x, y, w, h)
        else:
            self.r[key].shift_region(x, y)

    def _create_asset_path(self, asset):
        """Helper method for generating the proper OS-safe path to an asset.

        Args:
            asset (str): kcauto-internal asset-style path. This should be in
                the format of '[folder1]|[folder2]|[imagename]'. 'folder1' is
                expected to be within the assets folder of kcauto.

        Returns:
            str: OS-safe path to an asset.
        """
        asset_split = asset.split('|')
        return os.path.join(self.ASSETS_FOLDER, *asset_split)

    def _get_region(self, region):
        """Helper method that returns a Region based on the region passed in.
        If a Region or Match object is passed in, it will return that  object
        as-is. If a string is passed in, it will look up that string key from
        the pre-defined region dictionary and return it if there is a match.

        Args:
            region (Region, Match str): Region/Match object or string key of
                pre-defined region.

        Raises:
            TypeError: string region key was not found in pre-defined region
                list.

        Returns:
            Region/ImageMatch: Region or ImageMatch object.
        """
        if type(region) == str:
            return self.r[region]
        elif isinstance(region, ImageMatch):
            return region
        else:
            raise TypeError("Invalid region specified.")

    def find(self, region, asset, similarity=DEFAULT, cached=False):
        """Wrapper method for finding an asset on-screen.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.
            cached (bool, optional): flag for using cached snapshot of region.
                Defaults to False.

        Returns:
            Match: Match instance of best asset match.
        """
        r = self._get_region(region)
        return r.find(self._create_asset_path(asset), similarity, cached)

    def find_all(self, region, asset, similarity=DEFAULT, cached=False):
        """Wrapper method for finding all matches of an asset on-screen.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.
            cached (bool, optional): flag for using cached snapshot of region.
                Defaults to False.

        Returns:
            [Match]: list of Match instances of asset matches above the defined
                similarity score.
        """
        r = self._get_region(region)
        return r.find_all(self._create_asset_path(asset), similarity, cached)

    def exists(self, region, asset, similarity=DEFAULT, cached=False):
        """Wrapper method for reporting whether an asset exists on-screen.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.
            cached (bool, optional): flag for using cached snapshot of region.
                Defaults to False.

        Returns:
            bool: True if asset exists on-screen, False otherwise.
        """
        r = self._get_region(region)
        return r.exists(self._create_asset_path(asset), similarity, cached)

    def wait(self, region, asset, wait=30, similarity=DEFAULT):
        """Wrapper method for waiting for an asset to exist on-screen.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            wait (int): seconds to wait for asset to appear. Defaults to 30.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.

        Returns:
            Match: Match instance of best asset match.
        """
        r = self._get_region(region)
        return r.wait(self._create_asset_path(asset), wait, similarity)

    def wait_vanish(self, region, asset, wait=30, similiarity=DEFAULT):
        """Wrapper method for waiting for an asset to no longer exist
        on-screen.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            wait (int): seconds to wait for asset to disappear. Defaults to 30.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.

        Returns:
            bool: True when asset no longer exists on-screen.
        """
        r = self._get_region(region)
        return r.wait_vanish(self._create_asset_path(asset), wait, similiarity)

    def hover(self, region):
        """Helper method that hovers the mouse cursor over the defined region.
        This method is a no-op if using the Chrome Driver interaction mode.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
        """
        if (cfg.config.general.interaction_mode
                is InteractionModeEnum.DIRECT_CONTROL):
            r = self._get_region(region)
            r.hover()

    def click(self, region, pad=(0, 0, 0, 0)):
        """Helper method that clicks a passed in region. The pad parameter
        allows for further tweaking of the valid click region.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            pad (tuple, optional): click region modifier. Defaults to
                (0, 0, 0, 0).
        """
        r = self._get_region(region)
        if (cfg.config.general.interaction_mode
                is InteractionModeEnum.DIRECT_CONTROL):
            r.click(pad=pad)
        elif (cfg.config.general.interaction_mode
                is InteractionModeEnum.CHROME_DRIVER):
            self._chrome_driver_click_method(region, pad)

    def click_existing(
            self, region, asset, similarity=DEFAULT, pad=(0, 0, 0, 0),
            cached=False):
        """Helper method that clicks a region if it exists. The pad parameter
        allows for further tweaking of the valid click region.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.
            pad (tuple, optional): click region modifier. Defaults to
                (0, 0, 0, 0).
            cached (bool, optional): flag for using cached snapshot of region.
                Defaults to False.

        Returns:
            bool: True if the region was found and clicked; False otherwise.
        """
        r = self._get_region(region)
        try:
            match = r.find(self._create_asset_path(asset), similarity, cached)
            self.click(match, pad=pad)
            self.sleep()
            return True
        except FindFailed:
            return False

    def wait_and_click(self, region, asset, wait=10, similarity=DEFAULT):
        """Helper method that waits for an asset match to show up in a region
        and then click it.

        Args:
            region (Region, Match, str): Region/Match object or pre-defined
                region key.
            asset (str): kcauto-style asset path.
            wait (int): seconds to wait for asset to appear. Defaults to 30.
            similarity (float, optional): minimum similarity score. Defaults to
                DEFAULT.
        """
        r = self._get_region(region)
        match = r.wait(self._create_asset_path(asset), wait, similarity)
        self.click(match)

    def sleep(self, base=None, flex=None):
        """Helper method for sleeping the script. Adds in random variance to
        the time slept. If no parameters are passed the sleep length will be
        between 0.3 and 0.7 seconds. The sleep time is further influenced by
        the SLEEP_MODIFIER.

        Args:
            base (int/float, optional): base number of seconds to sleep.
                Defaults to None.
            flex (int/float, optional): allowed amount of time to deviate from
                the base sleep length. Defaults to None.
        """
        if base is None:
            sleep(uniform(0.3, 0.7) + SLEEP_MODIFIER)
        else:
            flex = base if flex is None else flex
            sleep(uniform(base, base + flex) + SLEEP_MODIFIER)

    def while_wrapper(
            self, conditional_func, internal_func=None, timeout=None,
            attempt_limit=None):
        """A wrapper for while conditionals that allow for execution timeouts
        and loop number limits to be defined. The conditional_func parameter
        should be a function or lambda with it returning True when the while
        loop should exit successfully. The internal_function, if specified,
        will execute within the while loop. Either timeout or attempt_limit
        must be specified. Meant to facilitate visual asset searches in while
        loops.

        Args:
            conditional_func (func/lambda): conditional function/lambda.
            internal_func (func/lambda): function/lambda to execute within
                the while loop. Defaults to None.
            timeout (int, optional): max number of seconds the while loop
                should execute. Defaults to None.
            attempt_limit (int, optional): max number of times the while loop
                should execute. Defaults to None.

        Raises:
            TypeError: neither timeout or attempt limit specified.
            FindFailed: the conditional failed to succeed before the timeout
                or within the attempt limit.

        Returns:
            True: conditional_func succeeded and returned True
        """
        if not timeout and not attempt_limit:
            raise TypeError("timeout or attempt_limit must be defined.")

        failed_conditional = False
        if timeout:
            end_time = datetime.now() + timedelta(seconds=timeout)
        elif attempt_limit:
            counter = 0

        while not conditional_func():
            if timeout and datetime.now() > end_time:
                failed_conditional = True
                break
            elif attempt_limit:
                counter += 1
                if counter >= attempt_limit:
                    failed_conditional = True
                    break
            if internal_func:
                internal_func()

        if failed_conditional:
            raise FindFailed(
                "Conditional failed by exceeding timeout or attempt limit")

        return True

    def readable_list_join(self, raw_list):
        """Helper method for joining a list into a human-readable string,
        adding 'and' between the second to last and last items as needed.

        Args:
            raw_list (list): list to join

        Returns:
            str: joined string
        """
        display_text = ', '.join([str(i) for i in raw_list])
        display_text = ' and'.join(display_text.rsplit(',', 1))
        return display_text

    def _override_hover_method(self, r, x, y):
        """Hover method is a no-op when using the Chrome Driver interaction
        mode.
        """
        pass

    def _override_click_method(self, r, x, y, pad):
        """Click method override used when using Chrome Driver interaction
        mode.

        Args:
            r (Region, Match): Region/Match region to click
            x (int): x-coordinate of click generated by pyvisauto
            y (int): y-coordinate of click generated by pyvisauto
            pad (tuple): padding parameter used to modify click coordinate
        """
        self._chrome_driver_click_method(r, pad)

    def _chrome_driver_click_method(self, r, pad):
        """Click method used in Chrome Driver interaction mode.

        Args:
            r (Region, Match): Region/Match region to click
            pad (tuple): padding parameter used to modify click coordinate
        """
        layout_width = (
            self.visual_hook.Page.getLayoutMetrics()[
                'result']['layoutViewport']['clientWidth'])
        # 692,557 is the offset for the game start button
        game_x = self.game_x if self.game_x else r.x - 692
        game_y = self.game_y if self.game_y else r.y - 557
        x_pad = game_x - ((layout_width - GAME_W) // 2)
        y_pad = game_y
        x = randint(r.x - x_pad - pad[3], r.x + r.w - x_pad + pad[1])
        y = randint(r.y - y_pad - pad[0], r.y + r.h - y_pad + pad[2])
        self.visual_hook.Input.synthesizeTapGesture(x=x, y=y)


kca = Kca()
