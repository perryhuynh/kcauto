from sikuli import Region, Pattern
from threading import Thread
from globals import Globals


# Order by NEW
# - select NTH ship from START/END that is LOCKED/UNLOCKED/EITHER

# Order by LEVEL
# - select NTH ship from START/END that is LOCKED/UNLOCKED/EITHER

# Order by TYPE
# - select ship of TYPE that is LOCKED/UNLOCKED/EITHER
# - (for subs) select specific SHIP of TYPE that is LOCKED/UNLOCKED/EITHER

# [N/L][#][S/E][L/U/E]
# T[L/U/E][SS/SSV/etc]


class ShipSwitcher(object):
    def __init__(self, config, stats, regions, fleets, combat):
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.ship_count = 1
        self.current_shiplist_page = 1

    def ship_switch_logic(self):
        self._get_ship_count()
        for i in range(1, 7):
            if self._check_need_to_switch_ship(i):
                self._press_switch_ship_button(i)
                for '__OPTIONS':
                    self._resolve_replacement_ship()

    def _get_ship_count(self):
        # read number at top of interface
        pass

    def _switch_fleet(self, fleet):
        # unused for now
        pass

    def _check_need_to_switch_ship(self, position):
        # check against settings in specific region: damage? fatigue?
        pass

    def _press_switch_ship_button(self, position):
        pass

    def _switch_shiplist_sorting(self, target):
        pass

    def _change_shiplist_page(self, target):
        if target == 'end':
            pass
        elif target == 'back':
            pass
        elif target == 'forward':
            pass
        elif target == 'start':
            pass

    def _switch_shiplist_page(self, target_page):
        current_page = self.curent_shiplist_page
        pass

    def _choose_ship_by_position(self, position):
        pass

    def _check_ship_availability(self):
        ship_not_available = False
        if ship_not_available:
            return False
        return True

    def _resolve_replacement_ship(self):
        self._switch_shiplist_sorting('__TARGET')
        self._switch_shiplist_page(5)
        self._choose_ship_by_position(4)
        if self._check_ship_availability():
            # click switch button
            return True
        else:
            return False
