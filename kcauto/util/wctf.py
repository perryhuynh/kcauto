import requests

from constants import WCTF_DB_URL, WCTF_SUFFIX_URL
from util.json_data import JsonData
from util.logger import Log


class WhoCallsTheFleetData(object):
    """Class that contains methods for retrieving, parsing, and saving
    Who Calls the Fleet (WCTF) data.
    """
    @classmethod
    def get_and_save_wgtf_data(cls):
        """Wrapper method for retrieving and storing WCTF data.
        """
        Log.log_debug("Attempting to get WCTF data.")

        suffixes = cls._get_suffix_data()
        name_db = cls._get_ship_name_data(suffixes)

        Log.log_debug("Successfully downloaded WCTF data.")
        JsonData.dump_json(name_db, 'data|temp|wctf.json')

    @staticmethod
    def _get_suffix_data():
        """Method for retrieving and parsing the WCTF suffix data needed to
        generate complete ship names.

        Returns:
            dict: suffix dict
        """
        suf_res = requests.get(WCTF_SUFFIX_URL)
        suffixes = {}

        if suf_res.status_code == 200:
            suf_split = suf_res.text.split('\n')
            for line in suf_split:
                line = line.strip()
                if not line:
                    continue

                line_dict = JsonData.load_json_str(line)
                suffixes[line_dict['id']] = {
                    'jp': line_dict['ja_jp'],
                    'non_jp': line_dict['ja_romaji']
                }
        else:
            Log.log_warn("Could not download WCTF suffix data.")

        return suffixes

    @staticmethod
    def _get_ship_name_data(suffixes):
        """Method for retrieving and parsing the WCTF ship name data with
        appropriate suffixes.

        Args:
            suffixes (dict): suffix dict

        Returns:
            dict: dict of ship names
        """
        db_res = requests.get(WCTF_DB_URL)
        name_db = {}
        if db_res.status_code == 200:
            db_split = db_res.text.split('\n')
            for line in db_split:
                line = line.strip()
                if not line:
                    continue

                line_dict = JsonData.load_json_str(line)
                suffix_id = line_dict['name']['suffix']
                jp_name = line_dict['name']['ja_jp']
                non_jp_name = line_dict['name']['ja_romaji'].title()
                if suffix_id:
                    jp_name += f" {suffixes[suffix_id]['jp']}"
                    if non_jp_name:
                        non_jp_name += f" {suffixes[suffix_id]['non_jp']}"
                name_db[line_dict['id']] = {
                    'jp': jp_name,
                    'non_jp': non_jp_name
                }
        else:
            Log.log_warn("Could not download WCTF ship data.")

        return name_db
