import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.fleet_modes import FleetModeEnum
from constants import MAX_FLEET_PRESETS


class ConfigPvPLayout(LayoutBase):
    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('PvP Module', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled',
                        key='pvp.enabled',
                        enable_events=True)
                ],
                [
                    sg.Text('Fleet Preset', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [''] + [x for x in range(1, MAX_FLEET_PRESETS + 1)],
                        key='pvp.fleet_preset',
                        font=cls.FONT_10,
                        size=(13, 1))
                ]
            ],
            key='config_pvp_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = ('pvp.fleet_preset', )
        if values['pvp.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
        else:
            cls.update_window_elements(window, elements, {'disabled': True})

        if values['combat.enabled'] is True:
            fleet_mode = values['combat.fleet_mode']
            if fleet_mode != FleetModeEnum.STANDARD.display_name:
                window['pvp.enabled'].Update(False, disabled=True)
                cls.update_window_elements(
                    window, elements, {'disabled': True})
            else:
                window['pvp.enabled'].Update(disabled=False)
        else:
            window['pvp.enabled'].Update(disabled=False)
