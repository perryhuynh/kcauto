import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.damage_states import DamageStateEnum


class ConfigPassiveRepairLayout(LayoutBase):
    MIN_SLOTS_RESERVED = 0
    MAX_SLOTS_RESERVED = 3
    VALID_DAMAGE_STATES = (
        DamageStateEnum.HEAVY, DamageStateEnum.MODERATE, DamageStateEnum.MINOR,
        DamageStateEnum.SCRATCH)

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('Passive Repair', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled',
                        key='passive_repair.enabled',
                        enable_events=True)
                ],
                [
                    sg.Text('Repair Threshold', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [
                            x.display_name for x in DamageStateEnum
                            if x in cls.VALID_DAMAGE_STATES],
                        default_value=DamageStateEnum.SCRATCH.display_name,
                        key='passive_repair.repair_threshold',
                        font=cls.FONT_10,
                        size=(13, 1))
                ],
                [
                    sg.Text('Slots to Reserve', **cls.LABEL_SETTINGS),
                    sg.Spin(
                        [x for x in range(
                            cls.MIN_SLOTS_RESERVED,
                            cls.MAX_SLOTS_RESERVED + 1)],
                        0,
                        key='passive_repair.slots_to_reserve',
                        font=cls.FONT_10,
                        size=(5, 1))
                ]
            ],
            key='config_passive_repair_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = (
            'passive_repair.repair_threshold',
            'passive_repair.slots_to_reserve')
        if values['passive_repair.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
        else:
            cls.update_window_elements(window, elements, {'disabled': True})

        cls.correct_to_value_range(
            window, values, 'passive_repair.slots_to_reserve',
            cls.MIN_SLOTS_RESERVED, cls.MAX_SLOTS_RESERVED, 0)
