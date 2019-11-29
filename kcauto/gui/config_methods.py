from kca_enums.interaction_modes import InteractionModeEnum
from kca_enums.expeditions import ExpeditionEnum
from kca_enums.maps import MapEnum
from kca_enums.fleet_modes import FleetModeEnum
from kca_enums.event_difficulties import EventDifficultyEnum
from kca_enums.damage_states import DamageStateEnum


class ConfigMethods(object):
    @classmethod
    def generate_config_dict(cls, window, values):
        cfg = {}
        cfg['general.jst_offset'] = int(values['general.jst_offset'])
        cfg['general.interaction_mode'] = (
            InteractionModeEnum.display_name_to_value(
                values['general.interaction_mode']))
        cfg['general.chrome_dev_port'] = values['general.chrome_dev_port']
        cfg['general.paused'] = False
        cfg['expedition.enabled'] = values['expedition.enabled']
        cfg['expedition.fleet_2'] = cls._generate_value_list(
            values['expedition.fleet_2'], ExpeditionEnum)
        cfg['expedition.fleet_3'] = cls._generate_value_list(
            values['expedition.fleet_3'], ExpeditionEnum)
        cfg['expedition.fleet_4'] = cls._generate_value_list(
            values['expedition.fleet_4'], ExpeditionEnum)
        cfg['pvp.enabled'] = values['pvp.enabled']
        cfg['pvp.fleet_preset'] = (
            values['pvp.fleet_preset'] if values['pvp.fleet_preset'] else None)
        cfg['combat.enabled'] = values['combat.enabled']
        cfg['combat.sortie_map'] = MapEnum.display_name_to_value(
            values['combat.sortie_map'])
        cfg['combat.fleet_mode'] = FleetModeEnum.display_name_to_value(
            values['combat.fleet_mode'])
        cfg['combat.fleet_presets'] = ([
            int(fp) for fp in
            values['combat.fleet_presets'].split(',')
            if fp != ''])
        cfg['combat.node_selects'] = (
            values['combat.node_selects'].split(',')
            if values['combat.node_selects'] else [])
        cfg['combat.retreat_points'] = ([
            int(x) if x.isdigit() else x for x in
            (
                values['combat.retreat_points'].split(',')
                if values['combat.retreat_points'] else [])])
        cfg['combat.push_nodes'] = (
            values['combat.push_nodes'].split(',')
            if values['combat.push_nodes'] else [])
        cfg['combat.node_formations'] = (
            values['combat.node_formations'].split(',')
            if values['combat.node_formations'] else [])
        cfg['combat.node_night_battles'] = (
            values['combat.node_night_battles'].split(',')
            if values['combat.node_night_battles'] else [])
        cfg['combat.retreat_limit'] = DamageStateEnum.display_name_to_value(
            values['combat.retreat_limit'])
        cfg['combat.repair_limit'] = DamageStateEnum.display_name_to_value(
            values['combat.repair_limit'])
        cfg['combat.repair_timelimit_hours'] = values[
            'combat.repair_timelimit_hours']
        cfg['combat.repair_timelimit_minutes'] = values[
            'combat.repair_timelimit_minutes']
        lbas_groups = []
        if values['combat.lbas_group_1.enabled']:
            lbas_groups.append(1)
        if values['combat.lbas_group_2.enabled']:
            lbas_groups.append(2)
        if values['combat.lbas_group_3.enabled']:
            lbas_groups.append(3)
        cfg['combat.lbas_groups'] = lbas_groups
        cfg['combat.lbas_group_1_nodes'] = cls._generate_lbas_nodes(
            values['combat.lbas_group_1_node_1'],
            values['combat.lbas_group_1_node_2'])
        cfg['combat.lbas_group_2_nodes'] = cls._generate_lbas_nodes(
            values['combat.lbas_group_2_node_1'],
            values['combat.lbas_group_2_node_2'])
        cfg['combat.lbas_group_3_nodes'] = cls._generate_lbas_nodes(
            values['combat.lbas_group_3_node_1'],
            values['combat.lbas_group_3_node_2'])
        cfg['combat.check_fatigue'] = values['combat.check_fatigue']
        cfg['combat.check_lbas_fatigue'] = values['combat.check_lbas_fatigue']
        cfg['combat.reserve_repair_dock'] = values[
            'combat.reserve_repair_dock']
        cfg['combat.port_check'] = values['combat.port_check']
        cfg['combat.clear_stop'] = values['combat.clear_stop']
        cfg['event_reset.enabled'] = values['event_reset.enabled']
        cfg['event_reset.frequency'] = values['event_reset.frequency']
        cfg['event_reset.reset_difficulty'] = (
            EventDifficultyEnum.display_name_to_value(
                values['event_reset.reset_difficulty']))
        cfg['event_reset.farm_difficulty'] = (
            EventDifficultyEnum.display_name_to_value(
                values['event_reset.farm_difficulty']))
        cfg['ship_switcher.enabled'] = values['ship_switcher.enabled']
        slot_rules = {}
        for slot_id in range(1, 7):
            if values[f'ship_switcher.slot_{slot_id}_rule']:
                slot_rules[slot_id] = values[
                    f'ship_switcher.slot_{slot_id}_rule']
        cfg['ship_switcher.slots'] = slot_rules
        cfg['passive_repair.enabled'] = values['passive_repair.enabled']
        cfg['passive_repair.repair_threshold'] = (
            DamageStateEnum.display_name_to_value(
                values['passive_repair.repair_threshold']))
        cfg['passive_repair.slots_to_reserve'] = values[
            'passive_repair.slots_to_reserve']
        cfg['quest.enabled'] = values['quest.enabled']
        cfg['quest.quests'] = (
            values['quest.quests'].strip().split(',')
            if values['quest.quests'].strip() else [])
        cfg['scheduler.enabled'] = values['scheduler.enabled']
        cfg['scheduler.rules'] = window['scheduler.rules'].Values
        return cfg

    @classmethod
    def unpack_config_dict(cls, window, cfg):
        window['general.jst_offset'].Update(cfg['general.jst_offset'])
        window['general.interaction_mode'].Update(
            InteractionModeEnum(cfg['general.interaction_mode']).display_name)
        window['general.chrome_dev_port'].Update(
            cfg['general.chrome_dev_port'])
        # window['general.paused'].Update(cfg['general.paused'])
        window['expedition.enabled'].Update(cfg['expedition.enabled'])
        for fleet_id in range(2, 5):
            window[f'expedition.fleet_{fleet_id}'].Update(','.join([
                ExpeditionEnum(x).display_name
                for x in cfg[f'expedition.fleet_{fleet_id}']]))
        window['pvp.enabled'].Update(cfg['pvp.enabled'])
        window['pvp.fleet_preset'].Update(cfg['pvp.fleet_preset'])
        window['combat.enabled'].Update(cfg['combat.enabled'])
        window['combat.sortie_map'].Update(
            MapEnum(cfg['combat.sortie_map']).display_name)
        window['combat.fleet_mode'].Update(
            FleetModeEnum(cfg['combat.fleet_mode']).display_name)
        if (
                cfg['combat.fleet_presets']
                and len(cfg['combat.fleet_presets']) > 0):
            window['combat.fleet_presets'].Update(
                ','.join([str(fp) for fp in cfg['combat.fleet_presets']]))
        else:
            window['combat.fleet_presets'].Update('')
        window['combat.node_selects'].Update(
            ','.join(cfg['combat.node_selects']))
        window['combat.retreat_points'].Update(
            ','.join([str(x) for x in cfg['combat.retreat_points']]))
        window['combat.push_nodes'].Update(
            ','.join(cfg['combat.push_nodes']))
        window['combat.node_formations'].Update(
            ','.join(cfg['combat.node_formations']))
        window['combat.node_night_battles'].Update(
            ','.join(cfg['combat.node_night_battles']))
        window['combat.retreat_limit'].Update(
            DamageStateEnum(cfg['combat.retreat_limit']).display_name)
        window['combat.repair_limit'].Update(
            DamageStateEnum(cfg['combat.repair_limit']).display_name)
        window['combat.repair_timelimit_hours'].Update(
            cfg['combat.repair_timelimit_hours'])
        window['combat.repair_timelimit_minutes'].Update(
            cfg['combat.repair_timelimit_minutes'])
        for group_id in range(1, 4):
            if len(cfg[f'combat.lbas_group_{group_id}_nodes']) == 2:
                node_1 = cfg[f'combat.lbas_group_{group_id}_nodes'][0]
                node_2 = cfg[f'combat.lbas_group_{group_id}_nodes'][1]
            else:
                node_1 = ''
                node_2 = ''
            window[f'combat.lbas_group_{group_id}_node_1'].Update(node_1)
            window[f'combat.lbas_group_{group_id}_node_2'].Update(node_2)
            window[f'combat.lbas_group_{group_id}.enabled'].Update(
                group_id in cfg['combat.lbas_groups'])
        window['combat.check_fatigue'].Update(cfg['combat.check_fatigue'])
        window['combat.check_lbas_fatigue'].Update(
            cfg['combat.check_lbas_fatigue'])
        window['combat.reserve_repair_dock'].Update(
            cfg['combat.reserve_repair_dock'])
        window['combat.port_check'].Update(cfg['combat.port_check'])
        window['combat.clear_stop'].Update(cfg['combat.clear_stop'])
        window['event_reset.enabled'].Update(cfg['event_reset.enabled'])
        window['event_reset.frequency'].Update(cfg['event_reset.frequency'])
        window['event_reset.reset_difficulty'].Update(EventDifficultyEnum(
            cfg['event_reset.reset_difficulty']).display_name)
        window['event_reset.farm_difficulty'].Update(EventDifficultyEnum(
            cfg['event_reset.farm_difficulty']).display_name)
        window['ship_switcher.enabled'].Update(cfg['ship_switcher.enabled'])
        for slot_id in range(1, 7):
            if str(slot_id) in cfg['ship_switcher.slots']:
                window[f'ship_switcher.slot_{slot_id}_rule'].Update(
                    cfg['ship_switcher.slots'][str(slot_id)])
        window['passive_repair.enabled'].Update(cfg['passive_repair.enabled'])
        window['passive_repair.repair_threshold'].Update(DamageStateEnum(
            cfg['passive_repair.repair_threshold']).display_name)
        window['passive_repair.slots_to_reserve'].Update(
            cfg['passive_repair.slots_to_reserve'])
        window['quest.enabled'].Update(cfg['quest.enabled'])
        window['quest.quests'].Update(','.join(cfg['quest.quests']))
        window['scheduler.enabled'].Update(cfg['scheduler.enabled'])
        window['scheduler.rules'].Update(values=cfg['scheduler.rules'])

    @staticmethod
    def _generate_value_list(display_name_list, enum):
        if not display_name_list:
            return []
        value_list = []
        display_split = display_name_list.split(',')
        for display_value in display_split:
            value_list.append(enum.display_name_to_value(display_value))
        return value_list

    @staticmethod
    def _generate_lbas_nodes(node_1, node_2):
        return [node_1, node_2] if node_1 and node_2 else []
