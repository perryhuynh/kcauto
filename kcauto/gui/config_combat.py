import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from gui.config_combat_fleet_preset_popup import (
    ConfigCombatFleetPresetPopupLayout)
from gui.config_combat_node_select_popup import (
    ConfigCombatNodeSelectPopupLayout)
from gui.config_combat_retreat_node_popup import (
    ConfigCombatRetreatNodePopupLayout)
from gui.config_combat_push_node_popup import ConfigCombatPushNodePopupLayout
from gui.config_combat_node_nb_popup import ConfigCombatNodeNBPopupLayout
from gui.config_combat_node_formation_popup import (
    ConfigCombatNodeFormationPopupLayout)
from kca_enums.maps import MapEnum
from kca_enums.fleet_modes import FleetModeEnum
from kca_enums.damage_states import DamageStateEnum
from kca_enums.nodes import NamedNodeEnum


class ConfigCombatLayout(LayoutBase):
    MIN_TIME_LIMIT_HOURS = 0
    MAX_TIME_LIMIT_HOURS = 99
    MIN_TIME_LIMIT_MINUTES = 0
    MAX_TIME_LIMIT_MINUTES = 59
    VALID_DAMAGE_STATES = (
        DamageStateEnum.HEAVY, DamageStateEnum.MODERATE, DamageStateEnum.MINOR,
        DamageStateEnum.SCRATCH)

    @classmethod
    def lbas_group_node_line_generator(cls, group_id):
        return [
            sg.Text(f'LBAS Group {group_id}', **cls.LABEL_SETTINGS),
            sg.Checkbox(
                'Enabled',
                key=f'combat.lbas_group_{group_id}.enabled',
                font=cls.FONT_10,
                enable_events=True),
            sg.Combo(
                [''] + [x.display_name for x in NamedNodeEnum],
                key=f'combat.lbas_group_{group_id}_node_1',
                font=cls.FONT_10,
                size=(4, 1)),
            sg.Combo(
                [''] + [x.display_name for x in NamedNodeEnum],
                key=f'combat.lbas_group_{group_id}_node_2',
                font=cls.FONT_10,
                size=(4, 1)),
            cls.generate_clear_btn(
                f'combat.lbas_group_{group_id}_nodes')]

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('Combat Module', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled', key='combat.enabled', enable_events=True)
                ],
                [
                    sg.Text('Map', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [x.display_name for x in MapEnum],
                        key='combat.sortie_map',
                        font=cls.FONT_10,
                        size=(4, 1),
                        enable_events=True)
                ],
                [
                    sg.Text('Fleet Mode', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [x.display_name for x in FleetModeEnum],
                        key='combat.fleet_mode',
                        font=cls.FONT_10,
                        size=(8, 1),
                        enable_events=True)
                ],
                [
                    sg.Text('Fleet Presets', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        key='combat.fleet_presets',
                        font=cls.FONT_10,
                        size=(30, 1),
                        disabled=True),
                    cls.generate_edit_btn('combat.fleet_presets'),
                    cls.generate_clear_btn('combat.fleet_presets')
                ],
                [
                    sg.Text('Node Selects', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        key='combat.node_selects',
                        font=cls.FONT_10,
                        size=(30, 1),
                        disabled=True),
                    cls.generate_edit_btn('combat.node_selects'),
                    cls.generate_clear_btn('combat.node_selects')
                ],
                [
                    sg.Text('Retreat Points', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        key='combat.retreat_points',
                        font=cls.FONT_10,
                        size=(30, 1),
                        disabled=True),
                    cls.generate_edit_btn('combat.retreat_points'),
                    cls.generate_clear_btn('combat.retreat_points')
                ],
                [
                    sg.Text('Push Nodes', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        key='combat.push_nodes',
                        font=cls.FONT_10,
                        size=(30, 1),
                        disabled=True),
                    cls.generate_edit_btn('combat.push_nodes'),
                    cls.generate_clear_btn('combat.push_nodes')
                ],
                [
                    sg.Text('Node Formations', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        key='combat.node_formations',
                        font=cls.FONT_10,
                        size=(30, 1),
                        disabled=True),
                    cls.generate_edit_btn('combat.node_formations'),
                    cls.generate_clear_btn('combat.node_formations')
                ],
                [
                    sg.Text('Node Night Battles', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        key='combat.node_night_battles',
                        font=cls.FONT_10,
                        size=(30, 1),
                        disabled=True),
                    cls.generate_edit_btn('combat.node_night_battles'),
                    cls.generate_clear_btn('combat.node_night_battles')
                ],
                [
                    sg.Text('Retreat Limit', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [
                            x.display_name for x in DamageStateEnum
                            if x in cls.VALID_DAMAGE_STATES],
                        default_value=DamageStateEnum.HEAVY.display_name,
                        key='combat.retreat_limit',
                        font=cls.FONT_10,
                        size=(8, 1))
                ],
                [
                    sg.Text('Repair Limit', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [
                            x.display_name for x in DamageStateEnum
                            if x in cls.VALID_DAMAGE_STATES],
                        default_value=DamageStateEnum.MODERATE.display_name,
                        key='combat.repair_limit',
                        font=cls.FONT_10,
                        size=(8, 1))
                ],
                [
                    sg.Text('Repair Time Limit', **cls.LABEL_SETTINGS),
                    sg.Spin(
                        [x for x in range(
                            cls.MIN_TIME_LIMIT_HOURS,
                            cls.MAX_TIME_LIMIT_HOURS + 1)],
                        0,
                        key='combat.repair_timelimit_hours',
                        font=cls.FONT_10,
                        size=(2, 1),
                        enable_events=True),
                    sg.Text('hr:', font=cls.FONT_10),
                    sg.Spin(
                        [x for x in range(
                            cls.MIN_TIME_LIMIT_MINUTES,
                            cls.MAX_TIME_LIMIT_MINUTES + 1)],
                        0,
                        key='combat.repair_timelimit_minutes',
                        font=cls.FONT_10,
                        size=(2, 1),
                        enable_events=True),
                    sg.Text('mins', font=cls.FONT_10)
                ],
                cls.lbas_group_node_line_generator(1),
                cls.lbas_group_node_line_generator(2),
                cls.lbas_group_node_line_generator(3),
                [
                    sg.Text('Misc Options', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Check Fatigue',
                        key='combat.check_fatigue',
                        font=cls.FONT_10),
                    sg.Checkbox(
                        'Check LBAS Fatigue',
                        key='combat.check_lbas_fatigue',
                        font=cls.FONT_10)
                ],
                [
                    sg.Text('', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Reserve Repair Dock',
                        key='combat.reserve_repair_dock',
                        font=cls.FONT_10),
                    sg.Checkbox(
                        'Port Check',
                        key='combat.port_check',
                        font=cls.FONT_10),
                ],
                [
                    sg.Text('', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Clear Stop',
                        key='combat.clear_stop',
                        font=cls.FONT_10)
                ]
            ],
            key='config_combat_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = (
            'combat.sortie_map', 'combat.fleet_mode',
            'combat.node_selects.edit', 'combat.node_selects.clear',
            'combat.retreat_points.edit', 'combat.retreat_points.clear',
            'combat.push_nodes.edit', 'combat.push_nodes.clear',
            'combat.node_formations.edit', 'combat.node_formations.clear',
            'combat.node_night_battles.edit',
            'combat.node_night_battles.clear',
            'combat.retreat_limit', 'combat.repair_limit',
            'combat.repair_timelimit_hours', 'combat.repair_timelimit_minutes',
            'combat.lbas_group_1.enabled', 'combat.lbas_group_2.enabled',
            'combat.lbas_group_3.enabled',
            'combat.check_fatigue', 'combat.check_lbas_fatigue',
            'combat.reserve_repair_dock', 'combat.port_check',
            'combat.clear_stop',
        )
        fleet_preset_elements = (
            'combat.fleet_presets.edit', 'combat.fleet_presets.clear',
        )
        lbas_group_1_elements = (
            'combat.lbas_group_1_node_1', 'combat.lbas_group_1_node_2',
            'combat.lbas_group_1_nodes.clear',
        )
        lbas_group_2_elements = (
            'combat.lbas_group_2_node_1', 'combat.lbas_group_2_node_2',
            'combat.lbas_group_2_nodes.clear',
        )
        lbas_group_3_elements = (
            'combat.lbas_group_3_node_1', 'combat.lbas_group_3_node_2',
            'combat.lbas_group_3_nodes.clear',
        )
        if values['combat.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
            fleet_mode = values['combat.fleet_mode']
            fleet_preset_button_state = (
                window['combat.fleet_presets.edit'].TKButton.cget('state'))

            if fleet_mode != FleetModeEnum.STANDARD.display_name:
                window['combat.fleet_presets'].Update('')
                cls.update_window_elements(
                    window, fleet_preset_elements, {'disabled': True})
            else:
                if fleet_preset_button_state == 'disabled':
                    cls.update_window_elements(
                        window, fleet_preset_elements, {'disabled': False})

            if values['combat.lbas_group_1.enabled'] is True:
                cls.update_window_elements(
                    window, lbas_group_1_elements, {'disabled': False})
            else:
                cls.update_window_elements(
                    window, lbas_group_1_elements, {'disabled': True})
            if values['combat.lbas_group_2.enabled'] is True:
                cls.update_window_elements(
                    window, lbas_group_2_elements, {'disabled': False})
            else:
                cls.update_window_elements(
                    window, lbas_group_2_elements, {'disabled': True})
            if values['combat.lbas_group_3.enabled'] is True:
                cls.update_window_elements(
                    window, lbas_group_3_elements, {'disabled': False})
            else:
                cls.update_window_elements(
                    window, lbas_group_3_elements, {'disabled': True})
            if True not in (
                    values['combat.lbas_group_1.enabled'],
                    values['combat.lbas_group_2.enabled'],
                    values['combat.lbas_group_3.enabled']):
                window['combat.check_lbas_fatigue'].Update(
                    False, disabled=True)
        else:
            cls.update_window_elements(
                window,
                (
                    elements + fleet_preset_elements + lbas_group_1_elements
                    + lbas_group_2_elements + lbas_group_3_elements),
                {'disabled': True})

        cls.correct_to_value_range(
            window, values, 'combat.repair_timelimit_hours',
            cls.MIN_TIME_LIMIT_HOURS, cls.MAX_TIME_LIMIT_HOURS, 0)
        cls.correct_to_value_range(
            window, values, 'combat.repair_timelimit_minutes',
            cls.MIN_TIME_LIMIT_MINUTES, cls.MAX_TIME_LIMIT_MINUTES, 0)

        cls.check_popup_related_events(
            window, event, values, 'combat.fleet_presets',
            ConfigCombatFleetPresetPopupLayout)
        cls.check_popup_related_events(
            window, event, values, 'combat.node_selects',
            ConfigCombatNodeSelectPopupLayout)
        cls.check_popup_related_events(
            window, event, values, 'combat.retreat_points',
            ConfigCombatRetreatNodePopupLayout)
        cls.check_popup_related_events(
            window, event, values, 'combat.push_nodes',
            ConfigCombatPushNodePopupLayout)
        cls.check_popup_related_events(
            window, event, values, 'combat.node_formations',
            ConfigCombatNodeFormationPopupLayout)
        cls.check_popup_related_events(
            window, event, values, 'combat.node_night_battles',
            ConfigCombatNodeNBPopupLayout)

        if event == 'combat.lbas_group_1_nodes.clear':
            window['combat.lbas_group_1_node_1'].Update('')
            window['combat.lbas_group_1_node_2'].Update('')
        if event == 'combat.lbas_group_2_nodes.clear':
            window['combat.lbas_group_2_node_1'].Update('')
            window['combat.lbas_group_2_node_2'].Update('')
        if event == 'combat.lbas_group_3_nodes.clear':
            window['combat.lbas_group_3_node_1'].Update('')
            window['combat.lbas_group_3_node_2'].Update('')
