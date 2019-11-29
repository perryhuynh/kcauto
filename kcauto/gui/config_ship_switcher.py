import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from gui.config_ship_switcher_popup import ConfigShipSwitcherPopupLayout


class ConfigShipSwitcherLayout(LayoutBase):
    @classmethod
    def ship_switcher_slot_generator(cls, slot_id):
        return [
            sg.Text(f'Slot {slot_id} Rules', **cls.LABEL_SETTINGS),
            sg.InputText(
                key=f'ship_switcher.slot_{slot_id}_rule',
                font=cls.FONT_10,
                size=(30, 1),
                disabled=True),
            cls.generate_edit_btn(
                f'ship_switcher.slot_{slot_id}_rule'),
            cls.generate_clear_btn(
                f'ship_switcher.slot_{slot_id}_rule')
        ]

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('Ship Switcher Module', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled',
                        key='ship_switcher.enabled',
                        enable_events=True)
                ],
                cls.ship_switcher_slot_generator(1),
                cls.ship_switcher_slot_generator(2),
                cls.ship_switcher_slot_generator(3),
                cls.ship_switcher_slot_generator(4),
                cls.ship_switcher_slot_generator(5),
                cls.ship_switcher_slot_generator(6),
            ],
            key='config_ship_switcher_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = (
            'ship_switcher.slot_1_rule.edit',
            'ship_switcher.slot_1_rule.clear',
            'ship_switcher.slot_2_rule.edit',
            'ship_switcher.slot_2_rule.clear',
            'ship_switcher.slot_3_rule.edit',
            'ship_switcher.slot_3_rule.clear',
            'ship_switcher.slot_4_rule.edit',
            'ship_switcher.slot_4_rule.clear',
            'ship_switcher.slot_5_rule.edit',
            'ship_switcher.slot_5_rule.clear',
            'ship_switcher.slot_6_rule.edit',
            'ship_switcher.slot_6_rule.clear',
        )

        if values['ship_switcher.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
        else:
            cls.update_window_elements(window, elements, {'disabled': True})

        if values['combat.enabled'] is True:
            window['ship_switcher.enabled'].Update(disabled=False)
        else:
            window['ship_switcher.enabled'].Update(False, disabled=True)
            cls.update_window_elements(window, elements, {'disabled': True})

        if event.startswith('ship_switcher.slot_') and event.endswith('edit'):
            slot_id = event[19]
            window.Hide()
            new_values = ConfigShipSwitcherPopupLayout.update_gui(
                slot_id, values[f'ship_switcher.slot_{slot_id}_rule'])
            window[f'ship_switcher.slot_{slot_id}_rule'].Update(new_values)
            window.UnHide()
        if event.startswith('ship_switcher.slot_') and event.endswith('clear'):
            slot_id = event[19]
            window[f'ship_switcher.slot_{slot_id}_rule'].Update('')
