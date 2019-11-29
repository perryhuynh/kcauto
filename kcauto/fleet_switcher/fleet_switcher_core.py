from pyvisauto import Region
from random import choice
from sys import exit

import config.config_core as cfg
import fleet.fleet_core as flt
import nav.nav as nav
import util.kca as kca_u
from util.logger import Log


class FleetSwitcherCore(object):
    max_presets = 0
    presets = {}
    next_combat_preset = None

    def __init__(self):
        self._set_next_combat_preset()

    def update_fleetpreset_data(self, data):
        self.presets = {}
        self.max_presets = data['api_max_num']
        for preset_id in data['api_deck']:
            self.presets[int(preset_id)] = [
                ship_id for ship_id in data['api_deck'][preset_id]['api_ship']
                if ship_id > -1]

    def _set_next_combat_preset(self):
        if len(cfg.config.combat.fleet_presets) > 0:
            self.next_combat_preset = choice(cfg.config.combat.fleet_presets)

    def _get_next_preset_id(self, context):
        if context == 'combat':
            preset_id = self.next_combat_preset
        elif context == 'pvp':
            preset_id = cfg.config.pvp.fleet_preset
        return preset_id

    def require_fleetswitch(self, context):
        preset_id = self._get_next_preset_id(context)
        if preset_id is None:
            return False

        if preset_id in self.presets:
            if self.presets[preset_id] == flt.fleets.fleets[1].ship_ids:
                Log.log_debug("Preset Fleet is already loaded.")
                return False
        Log.log_msg(f"Need to switch to Fleet Preset {preset_id}.")
        return True

    def goto(self):
        nav.navigate.to('fleetcomp')
        kca_u.kca.click_existing(
            'lower_left', 'fleetswitcher|fleetswitch_submenu.png')
        kca_u.kca.wait(
            'lower_left', 'fleetswitcher|fleetswitch_submenu_exit.png')

    def switch_fleet(self, context):
        preset_id = self._get_next_preset_id(context)
        Log.log_msg(f"Switching to Fleet Preset {preset_id}.")
        if preset_id not in self.presets:
            Log.log_error(
                f"Fleet Preset {preset_id} is not specified in-game. Please "
                f"check your config.")
            exit(1)

        list_idx = (preset_id if preset_id < 5 else 5) - 1
        idx_offset = preset_id - 5
        if idx_offset > 0:
            kca_u.kca.sleep()
            self._scroll_preset_list(idx_offset)

        kca_u.kca.r['top'].hover()
        kca_u.kca.sleep()
        preset_idx_region = Region(
            kca_u.kca.game_x + 410,
            kca_u.kca.game_y + 275 + (list_idx * 76),
            70, 45)
        kca_u.kca.click_existing(
            preset_idx_region, 'fleetswitcher|fleetswitch_button.png')
        if kca_u.kca.exists(
                'left', 'fleetswitcher|fleetswitch_fail_check.png'):
            Log.log_error(
                f"Could not switch in fleet preset {preset_id}. Please check "
                f"your config and fleet presets.")
            exit(1)
        Log.log_msg(f"Fleet Preset {preset_id} loaded.")

        if context == 'combat':
            self._set_next_combat_preset()

    def _scroll_preset_list(self, target_clicks):
        Log.log_debug(f"Scrolling to target preset ({target_clicks} clicks).")
        clicks = 0
        while clicks < target_clicks:
            kca_u.kca.click_existing('lower_left', 'global|scroll_next.png')
            kca_u.kca.sleep(0.1)
            clicks += 1


fleet_switcher = FleetSwitcherCore()
