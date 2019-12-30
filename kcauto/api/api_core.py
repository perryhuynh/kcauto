import json
import sys
from datetime import datetime, timedelta

import combat.combat_core as com
import combat.lbas_core as lbas
import expedition.expedition_core as exp
import fleet.fleet_core as flt
import fleet_switcher.fleet_switcher_core as fsw
import pvp.pvp_core as pvp
import quest.quest_core as qst
import repair.repair_core as rep
import resupply.resupply_core as res
import ships.ships_core as shp
import stats.stats_core as sts
import util.kca as kca_u
from kca_enums.kcsapi_paths import KCSAPIEnum
from util.exceptions import (
    ApiException, Catbomb201Exception, ChromeCrashException)
from util.json_data import JsonData
from util.logger import Log


class ApiWrapper(object):
    def __init__(self):
        Log.log_debug("API Wrapper module initialized.")

    def update_from_api(
            self, target_apis={KCSAPIEnum.ANY}, need_all=True, timeout=30):
        if KCSAPIEnum.NONE in target_apis:
            return

        target_apis = set(target_apis)
        Log.log_debug("Begin waiting for API payload(s).")
        kcapi_received = False
        kcapi_requests = {}
        results = {}
        if timeout:
            timeout_time = datetime.now() + timedelta(seconds=timeout)

        while (
                not kcapi_received
                or len(kcapi_requests) > 0
                or len(target_apis) > 0):
            messages = kca_u.kca.api_hook.pop_messages()
            for message in messages:
                if message['method'] == 'Network.responseReceived':
                    request_url = message['params']['response']['url']
                    found_target = None
                    for target_api in target_apis:
                        if target_api.value in request_url:
                            found_target = target_api
                            request_id = message['params']['requestId']
                            Log.log_debug(
                                f"Waiting for request {request_id} "
                                f"({request_url})")
                            kcapi_requests[request_id] = {
                                'type': target_api,
                                'url': request_url
                            }
                    if found_target:
                        target_apis.remove(found_target)
                elif message['method'] == 'Network.loadingFinished':
                    message_request_id = message['params']['requestId']
                    if message_request_id in kcapi_requests:
                        Log.log_debug(f"Request {message_request_id} received")
                        kcapi_received = True
                        request_data = kcapi_requests.pop(message_request_id)
                        response_body = (
                            kca_u.kca.api_hook.Network.getResponseBody(
                                requestId=message_request_id))
                        response_body_attempt = 0
                        while not response_body and response_body_attempt < 5:
                            Log.log_debug("Empty API response. Trying again.")
                            response_body = (
                                kca_u.kca.api_hook.Network.getResponseBody(
                                    requestId=message_request_id))
                            if response_body:
                                break
                            kca_u.kca.sleep(0.5)
                            response_body_attempt += 1
                        try:
                            raw_svdata = response_body['result']['body'][7:]
                        except Exception:
                            raise ApiException(
                                "Empty or invalid API response.")
                        res = self._load_api_data(
                            request_data, json.loads(raw_svdata))
                        if request_data['type'].name in results:
                            results[request_data['type'].name].append(res)
                        else:
                            results[request_data['type'].name] = [res]

                        if not need_all:
                            return results
            if timeout:
                if datetime.now() > timeout_time:
                    break

        self._check_for_chrome_crash()

        return results

    def _check_for_chrome_crash(self):
        visual_events = kca_u.kca.visual_hook.pop_messages()
        for event in visual_events:
            if event['method'] == 'Inspector.targetCrashed':
                Log.log_warn("Chrome Crash detected.")
                raise ChromeCrashException

    def _load_api_data(self, request_data, data):
        request_type = request_data['type']
        if data['api_result'] != 1:
            Log.log_debug("Encountered non-1 API result.")
            Log.log_debug(data)
            if data['api_result'] == 201:
                Log.log_error("Encountered catbomb.")
                raise Catbomb201Exception
            else:
                raise ApiException
        if request_type is KCSAPIEnum.GET_DATA:
            return self._process_get_data(data)
        elif request_type is KCSAPIEnum.REQUIRE_INFO:
            return self._process_require_info(data)
        elif request_type is KCSAPIEnum.PORT:
            return self._process_port(data)
        elif request_type is KCSAPIEnum.SORTIE_MAPS:
            return self._process_sortie_maps(data)
        elif request_type is KCSAPIEnum.SORTIE_START:
            return self._process_sortie_start(data)
        elif request_type is KCSAPIEnum.SORTIE_NEXT:
            return self._process_sortie_next(data)
        elif request_type is KCSAPIEnum.SORTIE_BATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_NIGHTBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_AIRBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_LD_AIRBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_LD_SHOOTING:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_N2D:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_NIGHT_ONLY:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_ECF_BATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_ECF_NIGHTBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_BATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_NIGHTBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_AIRBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_WATERBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_LD_AIRBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_LD_SHOOTING:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_N2D:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_NIGHT_ONLY:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_EACH_NIGHT_ONLY:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_ECF_BATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_ECF_AIRBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_ECF_WATERBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_ECF_LD_AIRBATTLE:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_ECF_LD_SHOOTING:
            return self._process_battle(data)
        elif request_type is KCSAPIEnum.SORTIE_RESULT:
            return self._process_battle_result(data)
        elif request_type is KCSAPIEnum.SORTIE_CF_RESULT:
            return self._process_battle_result(data)
        elif request_type is KCSAPIEnum.SORTIE_SHIPDECK:
            return self._process_battle_deck(data)
        elif request_type is KCSAPIEnum.EXPEDITION_LIST:
            return self._process_expedition_list(data)
        elif request_type is KCSAPIEnum.EXPEDITION_START:
            return self._process_expedition_start(data)
        elif request_type is KCSAPIEnum.PVP_LIST:
            return self._process_pvp_list(data)
        elif request_type is KCSAPIEnum.PVP_ENEMY_INFO:
            return self._process_pvp_enemy_info(data)
        elif request_type is KCSAPIEnum.FLEETCOMP_PRESETS:
            return self._process_fleetcomp_presets(data)
        elif request_type is KCSAPIEnum.REPAIR_DOCKS:
            return self._process_repair_dock_data(data)
        elif request_type is KCSAPIEnum.QUEST_LIST:
            return self._process_quest_data(data)
        elif request_type is KCSAPIEnum.RESUPPLY_ACTION:
            return True
        elif request_type is KCSAPIEnum.LBAS_RESUPPLY_ACTION:
            return True
        return None

    def _process_get_data(self, data):
        try:
            get_data_ship = data['api_data']['api_mst_ship']
            shp.ships.update_ship_library(get_data_ship)
            JsonData.dump_json(get_data_ship, 'data|temp|get_data_ship.json')
        except KeyError:
            Log.log_debug("No getData found in API response.")

        return None

    def _process_require_info(self, data):
        try:
            exp_prov_resupply = data['api_data']['api_extra_supply'][0] == 1
            res.resupply.exp_provisional_enabled = exp_prov_resupply
        except KeyError:
            Log.log_debug("No provisional resupply data found in API response")

    def _process_port(self, data):
        try:
            rsc_data = data['api_data']['api_material']
            sts.stats.rsc.update_resource_stats(rsc_data)
        except KeyError:
            Log.log_debug("No resource data found in API response.")

        try:
            ship_data = data['api_data']['api_ship']
            shp.ships.update_local_ships(ship_data)
        except KeyError:
            Log.log_debug("No ship data found in API response.")

        try:
            repair_data = data['api_data']['api_ndock']
            rep.repair.update_repair_data(repair_data)
        except KeyError:
            Log.log_debug("No repair data found in API response.")

        try:
            fleet_data = data['api_data']['api_deck_port']
            flt.fleets.update_fleets(fleet_data)
        except KeyError:
            Log.log_debug("No fleet data found in API response.")

        try:
            max_ships = data['api_data']['api_basic']['api_max_chara']
            shp.ships.max_ship_count = max_ships
        except KeyError:
            Log.log_debug("No ship count data found in API response.")

        try:
            max_quests = data['api_data']['api_parallel_quest_count']
            qst.quest.max_quests = max_quests
        except KeyError:
            Log.log_debug("No quest data found in API response.")

        return None

    def _process_sortie_maps(self, data):
        try:
            available_maps = data['api_data']['api_map_info']
            com.combat.update_combat_map_list(available_maps)
        except KeyError:
            Log.log_debug("No available combat map data in API response.")

        try:
            lbas_data = data['api_data']['api_air_base']
            lbas.lbas.update_lbas_groups(lbas_data)
        except KeyError:
            Log.log_debug("No available lbas data in API response.")

    def _process_sortie_start(self, data):
        try:
            select_nodes = (
                data['api_data']['api_select_route']['api_select_cells'])
            com.combat.select_nodes = select_nodes
        except KeyError:
            Log.log_debug("No select node data found in API response.")

        try:
            next_node = data['api_data']['api_no']
            return next_node
        except KeyError:
            Log.log_debug("No next node data found in API response.")

    def _process_sortie_next(self, data):
        try:
            next_node = data['api_data']['api_no']
            return next_node
        except KeyError:
            Log.log_debug("No next node data found in API response.")

    def _process_battle(self, data):
        try:
            battle_data = data['api_data']
            com.combat.predict_battle(battle_data)
        except KeyError:
            Log.log_debug("No battle data found in API response.")

    def _process_battle_result(self, data):
        try:
            result_data = data['api_data']
            com.combat.process_battle_result(result_data)
        except KeyError:
            Log.log_debug("No CF battle data found in API response.")

    def _process_battle_deck(self, data):
        try:
            deck_data = data['api_data']['api_ship_data']
            shp.ships.update_local_ships(deck_data)
            for fleet in flt.fleets.combat_fleets:
                fleet.update_ship_data()
        except KeyError:
            Log.log_debug("No CF battle data found in API response.")

    def _process_expedition_list(self, data):
        try:
            exp.expedition.available_expeditions = (
                data['api_data']['api_list_items'])
            exp.expedition.populate_available_expeditions_per_world()
        except KeyError:
            Log.log_debug("No expedition list data found in API response.")

        return None

    def _process_pvp_list(self, data):
        try:
            pvp_data = data['api_data']['api_list']
            pvp.pvp.update_pvp_list(pvp_data)
        except KeyError:
            Log.log_debug("No pvp data found in API response.")

        return None

    def _process_pvp_enemy_info(self, data):
        try:
            enemy_info = data['api_data']['api_deck']['api_ships']
            return enemy_info
        except KeyError:
            Log.log_debug("No pvp enemy info data found in API response.")

    def _process_expedition_start(self, data):
        try:
            complete_time = data['api_data']['api_complatetime']
            return complete_time
        except KeyError:
            Log.log_debug("No expedition sent data")

        return None

    def _process_fleetcomp_presets(self, data):
        try:
            preset_data = data['api_data']
            fsw.fleet_switcher.update_fleetpreset_data(preset_data)
        except KeyError:
            Log.log_debug("No fleetcomp preset data found in API response.")

    def _process_repair_dock_data(self, data):
        try:
            repair_data = data['api_data']
            rep.repair.update_repair_data(repair_data)
        except KeyError:
            Log.log_debug("No repair data found in API response.")

    def _process_quest_data(self, data):
        try:
            quest_data = data['api_data']
            qst.quest.update_quest_data(quest_data)
        except KeyError:
            Log.log_debug("No quest data found in API response.")

    def update_ship_library_from_json(self):
        try:
            ship_data = JsonData.load_json('data|temp|get_data_ship.json')
            shp.ships.update_ship_library(ship_data)
        except FileNotFoundError as e:
            Log.log_error(
                "get_data_ship.json not found. Please run kcauto from the "
                "Kancolle splash screen to download data.")
            Log.log_error(e)
            sys.exit(1)


api = ApiWrapper()
