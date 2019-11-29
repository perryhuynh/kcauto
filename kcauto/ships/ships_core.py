from ships.ship import Ship
from util.json_data import JsonData
from util.logger import Log
from util.wctf import WhoCallsTheFleetData


class ShipsCore(object):
    max_ship_count = 0
    local_ships = []
    local_ships_by_local_id = {}
    ship_library = []
    name_db = {}

    def __init__(self):
        Log.log_debug("Initializing Ship core.")
        self.load_wctf_names()

    def update_local_ships(self, data):
        # from this api call, api_id = local_api_id, and api_ship_id = api_id
        Log.log_debug("Updating ship data from API.")
        self.local_ships = []
        self.local_ships_by_local_id = {}
        for ship in data:
            ship_instance = ship_instance = self.get_ship_from_api_id(
                ship['api_ship_id'], ship)
            self.local_ships.append(ship_instance)
            self.local_ships_by_local_id[ship['api_id']] = ship_instance

    def update_ship_library(self, data):
        Log.log_debug("Updating ship library data.")
        self.ship_library = data

    def load_wctf_names(self, force_update=False):
        if force_update:
            WhoCallsTheFleetData.get_and_save_wgtf_data()

        try:
            temp_db = JsonData.load_json('data|temp|wctf.json')
        except FileNotFoundError:
            WhoCallsTheFleetData.get_and_save_wgtf_data()
            temp_db = JsonData.load_json('data|temp|wctf.json')

        self.name_db = {}
        for key in temp_db:
            self.name_db[int(key)] = temp_db[key]

    @property
    def current_ship_count(self):
        return len(self.local_ships)

    def get_local_ships(self, req_ships):
        ships = []
        for local_id in req_ships:
            ships.append(self.local_ships_by_local_id[local_id])
        return ships

    def get_ship_from_api_id(self, api_id, local_ship_data=None):
        return Ship(api_id, local_data=local_ship_data)

    def get_ship_from_sortno(self, sortno):
        return Ship(sortno, id_type='sortno')


ships = ShipsCore()
