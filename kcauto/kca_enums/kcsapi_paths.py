from kca_enums.enum_base import EnumBase


class KCSAPIEnum(EnumBase):
    NONE = None
    ANY = 'kcsapi'
    GET_DATA = 'kcsapi/api_start2/getData'
    REQUIRE_INFO = 'kcsapi/api_get_member/require_info'
    PORT = 'kcsapi/api_port/port'
    SORTIE_MAPS = 'kcsapi/api_get_member/mapinfo'
    PVP_LIST = 'kcsapi/api_get_member/practice'
    EXPEDITION_LIST = 'kcsapi/api_get_member/mission'
    FLEETCOMP_PRESETS = 'kcsapi/api_get_member/preset_deck'
    RESUPPLY_ACTION = 'kcsapi/api_req_hokyu/charge'
    REPAIR_DOCKS = 'kcsapi/api_get_member/ndock'
    QUEST_LIST = 'kcsapi/api_get_member/questlist'
    QUEST_TURN_IN = 'kcsapi/api_req_quest/clearitemget'
    # generic combat endpoints
    SORTIE_START = 'kcsapi/api_req_map/start'
    SORTIE_ASSIGN_LBAS = 'kcsapi/api_req_map/start_air_base'
    SORTIE_NEXT = 'kcsapi/api_req_map/next'
    SORTIE_SHIPDECK = 'kcsapi/api_get_member/ship_deck'
    # standard fleet combat endpoints
    SORTIE_BATTLE = 'kcsapi/api_req_sortie/battle'
    SORTIE_NIGHTBATTLE = 'kcsapi/api_req_battle_midnight/battle'
    SORTIE_AIRBATTLE = 'kcsapi/api_req_sortie/airbattle'
    SORTIE_LD_AIRBATTLE = 'kcsapi/api_req_sortie/ld_airbattle'
    SORTIE_LD_SHOOTING = 'kcsapi/api_req_sortie/ld_shooting'
    SORTIE_N2D = 'kcsapi/api_req_sortie/night_to_day'
    SORTIE_NIGHT_ONLY = 'kcsapi/api_req_battle_midnight/sp_midnight'
    SORTIE_RESULT = 'kcsapi/api_req_sortie/battleresult'
    # enemy combined fleet combat endpoints
    SORTIE_ECF_BATTLE = 'kcsapi/api_req_combined_battle/ec_battle'
    SORTIE_ECF_NIGHTBATTLE = (
        'kcsapi/api_req_combined_battle/ec_midnight_battle')
    # combined fleet combat endpoints
    SORTIE_CF_BATTLE = 'kcsapi/api_req_combined_battle/battle'
    SORTIE_CF_NIGHTBATTLE = 'kcsapi/api_req_combined_battle/midnight_battle'
    SORTIE_CF_AIRBATTLE = 'kcsapi/api_req_combined_battle/airbattle'
    SORTIE_CF_WATERBATTLE = 'kcsapi/api_req_combined_battle/battle_water'
    SORTIE_CF_LD_AIRBATTLE = 'kcsapi/api_req_combined_battle/ld_airbattle'
    SORTIE_CF_LD_SHOOTING = 'kcsapi/api_req_combined_battle/ld_shooting'
    SORTIE_CF_N2D = 'kcsapi/api_req_combined_battle/ec_night_to_day'
    SORTIE_CF_NIGHT_ONLY = 'kcsapi/api_req_combined_battle/sp_midnight'
    SORTIE_CF_EACH_NIGHT_ONLY = (
        'kcsapi/api_req_combined_battle/each_sp_midnight')
    SORTIE_CF_ECF_BATTLE = 'kcsapi/api_req_combined_battle/each_battle'
    SORTIE_CF_ECF_AIRBATTLE = 'kcsapi/api_req_combined_battle/each_airbattle'
    SORTIE_CF_ECF_WATERBATTLE = (
        'kcsapi/api_req_combined_battle/each_battle_water')
    SORTIE_CF_ECF_LD_AIRBATTLE = (
        'kcsapi/api_req_combined_battle/each_ld_airbattle')
    SORTIE_CF_ECF_LD_SHOOTING = (
        'kcsapi/api_req_combined_battle/each_ld_shooting')
    SORTIE_CF_RESULT = 'kcsapi/api_req_combined_battle/battleresult'
    # pvp
    PVP_ENEMY_INFO = 'kcsapi/api_req_member/get_practice_enemyinfo'
    PVP_RESULTS = 'kcsapi/api_req_practice/battle_result'
    EXPEDITION_START = 'kcsapi/api_req_mission/start'
