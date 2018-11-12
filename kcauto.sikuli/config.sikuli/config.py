# config module
import ConfigParser
import os
import sys
from time import sleep
from copy import deepcopy
from sikuli import getBundlePath
from config_general import ConfigGeneral
from config_scheduled_sleep import ConfigScheduledSleep
from config_scheduled_stop import ConfigScheduledStop
from config_expeditions import ConfigExpeditions
from config_pvp import ConfigPvP
from config_combat import ConfigCombat
from config_event_reset import ConfigEventReset
from config_ship_switcher import ConfigShipSwitcher
from config_fleet_switcher import ConfigFleetSwitcher
from config_quests import ConfigQuests
from util import Util


class ConfigModule(object):
    """Config module that reads and validates the config to be passed to
    kcauto
    """

    def __init__(self, config_file):
        """Initializes the config file by changing the working directory to the
        root kcauto folder and reading the passed in config file.

        Args:
            config_file (str): name of config file
        """
        Util.log_msg("Initializing config module.")
        os.chdir(getBundlePath())
        os.chdir('..')

        self.config_file = config_file
        self.config_modified_time = None
        self.ok = True
        self.initialized = False
        self.changed = False
        self.program = ''
        self.jst_offset = 0
        self.pause = False
        self.scheduled_sleep = None
        self.scheduled_stop = None
        self.expeditions = None
        self.pvp = None
        self.combat = None
        self.event_reset = None
        self.ship_switcher = None
        self.fleet_switcher = None
        self.quests = None

    def read(self):
        """Method that backs up the previous config, reads in the specified
        config file and validates it.
        """
        temp_config = deepcopy(self.__dict__)
        del temp_config['config_modified_time']  # do not restore this attr

        # only read config on first init or the modified time of the config
        # file has changed since last read
        new_modified_time = os.path.getmtime(self.config_file)
        if not self.initialized:
            Util.log_msg('Reading config.')
            self.config_modified_time = new_modified_time
        elif self.config_modified_time != new_modified_time:
            Util.log_msg('Reading updated config.')
            self.config_modified_time = new_modified_time
        else:
            return

        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self.config_file)

        # initialize custom config parser modules
        module_general = ConfigGeneral(config_parser)
        module_scheduled_sleep = ConfigScheduledSleep(config_parser)
        module_scheduled_stop = ConfigScheduledStop(config_parser)
        module_expeditions = ConfigExpeditions(config_parser)
        module_pvp = ConfigPvP(config_parser)
        module_combat = ConfigCombat(config_parser)
        module_event_reset = ConfigEventReset(config_parser)
        module_ship_switcher = ConfigShipSwitcher(config_parser)
        module_quests = ConfigQuests(config_parser)

        # store results in temporary config
        temp_general = module_general.parse_cfg()
        temp_config['program'] = temp_general['program']
        temp_config['jst_offset'] = temp_general['jst_offset']
        temp_config['pause'] = temp_general['pause']
        temp_config['scheduled_sleep'] = module_scheduled_sleep.parse_cfg()
        temp_config['scheduled_stop'] = module_scheduled_stop.parse_cfg()
        temp_config['expeditions'] = module_expeditions.parse_cfg()
        temp_config['pvp'] = module_pvp.parse_cfg()
        temp_config['combat'] = module_combat.parse_cfg()
        temp_config['event_reset'] = module_event_reset.parse_cfg()
        temp_config['ship_switcher'] = module_ship_switcher.parse_cfg()
        temp_config['quests'] = module_quests.parse_cfg()

        # special handling for FleetSwitcher module
        if ((temp_config['combat']['enabled']
                and len(temp_config['combat']['fleets']) > 0)
                or (temp_config['pvp']['enabled']
                    and temp_config['pvp']['fleet'])):
            module_fleet_switcher = ConfigFleetSwitcher(config_parser)
            temp_config['fleet_switcher'] = module_fleet_switcher.parse_cfg()
        else:
            module_fleet_switcher = None
            temp_config['fleet_switcher'] = {'enabled': False}

        # validate temporary config
        self.ok = True
        self.ok = self.ok & module_general.validate_cfg(temp_config)
        self.ok = self.ok & module_scheduled_sleep.validate_cfg(temp_config)
        self.ok = self.ok & module_scheduled_stop.validate_cfg(temp_config)
        self.ok = self.ok & module_expeditions.validate_cfg(temp_config)
        self.ok = self.ok & module_pvp.validate_cfg(temp_config)
        self.ok = self.ok & module_combat.validate_cfg(temp_config)
        self.ok = self.ok & module_event_reset.validate_cfg(temp_config)
        self.ok = self.ok & module_ship_switcher.validate_cfg(temp_config)
        self.ok = self.ok & module_quests.validate_cfg(temp_config)
        if module_fleet_switcher:
            self.ok = self.ok & module_fleet_switcher.validate_cfg(temp_config)

        # handle passing new config into kcauto
        if (self.ok and not self.initialized):
            # first valid boot of kcauto
            Util.log_msg("Starting kcauto!")
            self._apply_config(temp_config)
            self.initialized = True
            self.changed = True
        elif (not self.ok and not self.initialized):
            # invalid config on boot of kcauto
            Util.log_error("Invalid config. Please check your config file.")
            sys.exit(1)
        elif (not self.ok and self.initialized):
            # hot-reload with invalid config
            Util.log_error(
                "Config change detected, but with problems. Ignoring config.")
        elif (self.ok and self.initialized):
            # make sure that there was actually a change in the config
            cur_config = deepcopy(self.__dict__)
            del cur_config['config_modified_time']
            if cur_config != temp_config:
                # hot-reload with valid, changed config
                Util.log_warning(
                    "Config change detected. Hot-reloading in 3...")
                sleep(1)
                Util.log_warning("2...")
                sleep(1)
                Util.log_warning("1...")
                sleep(1)
                self._apply_config(temp_config)
                self.changed = True
            else:
                # no actual change in config
                Util.log_msg("No change in config detected.")

    def _apply_config(self, config):
        """Method to apply the new config to the config instance.

        Args:
            config (dict): new config to apply
        """
        for key in config:
            setattr(self, key, config[key])
