from config_base import AbstractConfigModule
from util import Util


class ConfigShipSwitcher(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the ShipSwitcher settings of the passed-in config.
        """
        cp = self.config_parser

        if not cp.getboolean('ShipSwitcher', 'Enabled'):
            self.config.clear()
            self.config['enabled'] = False
            return self.config

        self.config['enabled'] = True
        for slot in range(0, 6):
            criteria = self._getlist(
                cp, 'ShipSwitcher', 'Slot{}Criteria'.format(slot + 1))
            ships = self._getlist(
                cp, 'ShipSwitcher', 'Slot{}Ships'.format(slot + 1))
            if criteria and ships:
                self.config[slot] = self._create_ship_switcher_dict(
                    slot, criteria, ships)

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the ShipSwitcher settings.
        """
        valid = True
        ship_switcher_cfg = config['ship_switcher']
        combat_cfg = config['combat']

        if not ship_switcher_cfg['enabled']:
            if len(ship_switcher_cfg) != 1:
                valid = False
            return valid

        # validate combat being enabled
        if not combat_cfg['enabled']:
            Util.log_error(
                "Ship Switcher can only be used if Combat is enabled")
            valid = False

        # validate combat fleet mode
        if combat_cfg['fleet_mode'] != '':
            Util.log_error(
                "Ship Switcher can only be used with standard fleets")
            valid = False

        # validate each slot
        for slot in range(0, 6):
            if slot not in ship_switcher_cfg:
                continue
            criteria = ship_switcher_cfg[slot]['criteria']

            # validate criteria
            for c in criteria:
                if c not in ('damage', 'fatigue', 'sparkle'):
                    Util.log_error(
                        "Invalid switch criteria for slot {}: '{}'".format(
                            slot, c))
                    valid = False

            # validate number of expected params for position mode
            if ship_switcher_cfg[slot]['mode'] == 'position':
                for ship in ship_switcher_cfg[slot]['ships']:
                    if len(ship) != 3:
                        Util.log_error(
                            "Invalid # of arguments for ship in slot {}"
                            .format(slot))
                        valid = False

            # validate number of expeted params for class mode
            if ship_switcher_cfg[slot]['mode'] == 'class':
                for ship in ship_switcher_cfg[slot]['ships']:
                    if len(ship) < 2:
                        Util.log_error(
                            "Invalid # of arguments for ship in slot {}"
                            .format(slot))
                        valid = False

        return valid

    @staticmethod
    def _create_ship_switcher_dict(slot, criteria, ships):
        """Helper method for generating the config dictionary for a slot in the
        ship switcher config.

        Args:
            slot (int): slot in fleet (0-based)
            criteria (str): criteria for ship switcher to check against
            ships (list[str]): raw list of target ship config lines

        Returns:
            dict: config dict for slot
        """
        slot_dict = {
            'slot': slot,
            'criteria': criteria,
            'mode': None,
            'ships': []
        }

        for ship in ships:
            ship_dict = {}
            ship_split = ship.split(':')
            if ship_split[0] == 'A':
                # asset mode
                ship_dict['sort_order'] = 'class'
                slot_dict['mode'] = 'asset'
                ship_dict['asset'] = ship_split[1].lower()
                # if asset can be split once by '_', it is in the format
                # [class]_[shipname], so infer the class from it; otherwise
                # the asset is for the entire class
                asset_ship_check = ship_dict['asset'].split('_')
                ship_dict['class'] = (
                    asset_ship_check[0]
                    if len(asset_ship_check) == 2
                    else ship_dict['asset'])
                if ship_split[2] != '_':
                    ship_dict['level'] = ship_split[2]
                if ship_split[3] != '_':
                    ship_dict['locked'] = (
                        True if ship_split[3] == 'L' else False)
                if ship_split[4] != '_':
                    ship_dict['ringed'] = (
                        True if ship_split[4] == 'R' else False)
            elif ship_split[0] == 'P':
                # position mode
                slot_dict['mode'] = (
                    'position' if slot_dict['mode'] is None else
                    slot_dict['mode'])
                if ship_split[1] == 'N':
                    ship_dict['sort_order'] = 'new'
                elif ship_split[1] == 'C':
                    ship_dict['sort_order'] = 'class'
                elif ship_split[1] == 'L':
                    ship_dict['sort_order'] = 'level'
                if ship_split[2] == 'E':
                    ship_dict['offset_ref'] = 'end'
                elif ship_split[2] == 'S':
                    ship_dict['offset_ref'] = 'start'
                ship_dict['offset'] = int(ship_split[3])
            slot_dict['ships'].append(ship_dict)
        return slot_dict
