import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from gui.config_expedition_popup import ConfigExpeditionPopupLayout
from kca_enums.fleet_modes import FleetModeEnum


class ConfigExpeditionLayout(LayoutBase):
    @classmethod
    def expedition_line_generator(cls, fleet_id):
        return [
            sg.Text(f'Fleet {fleet_id}', **cls.LABEL_SETTINGS),
            sg.InputText(
                key=f'expedition.fleet_{fleet_id}',
                font=cls.FONT_10,
                size=(30, 1),
                disabled=True),
            cls.generate_edit_btn(f'expedition.fleet_{fleet_id}'),
            cls.generate_clear_btn(f'expedition.fleet_{fleet_id}')
        ]

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('Expedition Module', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled',
                        key='expedition.enabled',
                        enable_events=True)
                ],
                cls.expedition_line_generator(2),
                cls.expedition_line_generator(3),
                cls.expedition_line_generator(4),
            ],
            key='config_expedition_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        fleet_2_elements = (
            'expedition.fleet_2.edit', 'expedition.fleet_2.clear',
        )
        fleet_3_elements = (
            'expedition.fleet_3.edit', 'expedition.fleet_3.clear',
        )
        elements = (
            'expedition.fleet_4.edit', 'expedition.fleet_4.clear',
        )

        if values['expedition.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})

            fleet_mode = values['combat.fleet_mode']
            exp_2_button_state = (window['expedition.fleet_2.edit'].TKButton.cget('state'))
            exp_3_button_state = (window['expedition.fleet_3.edit'].TKButton.cget('state'))
            if values['combat.enabled'] is True:
                if fleet_mode != FleetModeEnum.STANDARD.display_name and fleet_mode != FleetModeEnum.STRIKE.display_name:
                    window['expedition.fleet_2'].Update('')
                    cls.update_window_elements(
                        window, fleet_2_elements, {'disabled': True})
                else:
                    if exp_2_button_state == 'disabled':
                        cls.update_window_elements(
                            window, fleet_2_elements, {'disabled': False})
                if fleet_mode == FleetModeEnum.STRIKE.display_name:
                    window['expedition.fleet_3'].Update('')
                    cls.update_window_elements(
                        window, fleet_3_elements, {'disabled': True})
                else:
                    if exp_3_button_state == 'disabled':
                        cls.update_window_elements(
                            window, fleet_3_elements, {'disabled': False})
            else:
                if exp_2_button_state == 'disabled':
                    cls.update_window_elements(
                        window, fleet_2_elements, {'disabled': False})
                if exp_3_button_state == 'disabled':
                    cls.update_window_elements(
                        window, fleet_3_elements, {'disabled': False})
        else:
            cls.update_window_elements(
                window, fleet_2_elements + fleet_3_elements + elements, {'disabled': True})

        if event.startswith('expedition.fleet_') and event.endswith('edit'):
            fleet_id = event[17]
            other_expeditions = ''
            if fleet_id == '2':
                other_expeditions = (
                    f"{values['expedition.fleet_3']},"
                    f"{values['expedition.fleet_4']}")
            elif fleet_id == '3':
                other_expeditions = (
                    f"{values['expedition.fleet_2']},"
                    f"{values['expedition.fleet_4']}")
            elif fleet_id == '4':
                other_expeditions = (
                    f"{values['expedition.fleet_2']},"
                    f"{values['expedition.fleet_3']}")
            window.Hide()
            new_values = ConfigExpeditionPopupLayout.update_gui(
                fleet_id, values[f'expedition.fleet_{fleet_id}'],
                other_expeditions)
            window[f'expedition.fleet_{fleet_id}'].Update(new_values)
            window.UnHide()
        if event.startswith('expedition.fleet_') and event.endswith('clear'):
            fleet_id = event[17]
            window[f'expedition.fleet_{fleet_id}'].Update('')