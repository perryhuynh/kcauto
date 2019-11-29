import os
from sys import exit
from time import sleep

import args.args_core as arg
from config.combat import ConfigCombat
from config.event_reset import ConfigEventReset
from config.expedition import ConfigExpedition
from config.general import ConfigGeneral
from config.passive_repair import ConfigPassiveRepair
from config.pvp import ConfigPvP
from config.quest import ConfigQuest
from config.scheduler import ConfigScheduler
from config.ship_switcher import ConfigShipSwitcher
from util.json_data import JsonData
from util.logger import Log


class Config(object):
    cfg_path = None
    last_cfg_update_time = None
    general = None
    expedition = None
    pvp = None
    combat = None
    event_reset = None
    ship_switcher = None
    passive_repair = None
    quest = None
    scheduler = None

    def __init__(self):
        Log.log_success("Initializing kcauto.")
        if arg.args.parsed_args.cfg_path:
            self.cfg_path = arg.args.parsed_args.cfg_path
        else:
            cfg_file = arg.args.parsed_args.cfg
            self.cfg_path = JsonData.create_path(f'configs|{cfg_file}.json')
        self.initialize_config()
        if not self.general:
            Log.log_error("Error loading config.")
            exit(1)

    def _load_cfg_json(self):
        return JsonData.load_json(self.cfg_path)

    def initialize_config(self):
        update = False
        config_json = self._load_cfg_json()
        initial_load = True
        new_update_time = os.path.getmtime(self.cfg_path)

        if self.general:
            initial_load = False
            if config_json != self.general._config:
                Log.log_msg("Changes detected from previous config load.")
            else:
                Log.log_debug("No change from previous config load.")
                self.last_cfg_update_time = new_update_time
                return False

        try:
            new_general = ConfigGeneral(config_json)
            new_expedition = ConfigExpedition(config_json)
            new_pvp = ConfigPvP(config_json)
            new_combat = ConfigCombat(config_json)
            new_event_reset = ConfigEventReset(config_json)
            new_ship_switcher = ConfigShipSwitcher(config_json)
            new_passive_repair = ConfigPassiveRepair(config_json)
            new_quest = ConfigQuest(config_json)
            new_scheduler = ConfigScheduler(config_json)
            update = True
        except Exception as e:
            Log.log_error(e)

        if update:
            Log.log_success("Config successfully loaded.")
            if not initial_load:
                Log.log_success("Hot-reloading config in 3...")
                sleep(1)
                Log.log_success("2...")
                sleep(1)
                Log.log_success("1...")
                sleep(1)
            self.general = new_general
            self.expedition = new_expedition
            self.pvp = new_pvp
            self.combat = new_combat
            self.event_reset = new_event_reset
            self.ship_switcher = new_ship_switcher
            self.passive_repair = new_passive_repair
            self.quest = new_quest
            self.scheduler = new_scheduler
            self.last_cfg_update_time = new_update_time
            return True

    @property
    def config_changed(self):
        cfg_update_time = os.path.getmtime(self.cfg_path)
        if cfg_update_time != self.last_cfg_update_time:
            Log.log_msg("Config last modification time changed.")
            return True
        return False


config = Config()
