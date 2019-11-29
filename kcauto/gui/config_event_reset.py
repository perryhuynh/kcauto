import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.event_difficulties import EventDifficultyEnum


class ConfigEventResetLayout(LayoutBase):
    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('Event Reset Module', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled',
                        key='event_reset.enabled',
                        enable_events=True)
                ],
                [
                    sg.Text('Reset Frequency', **cls.LABEL_SETTINGS),
                    sg.Spin(
                        [x for x in range(1, 11)],
                        2,
                        key='event_reset.frequency',
                        font=cls.FONT_10,
                        size=(4, 1))
                ],
                [
                    sg.Text('Reset Difficulty', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [
                            x.display_name for x in EventDifficultyEnum
                            if x is not EventDifficultyEnum.NONE],
                        default_value=EventDifficultyEnum.NORMAL.display_name,
                        key='event_reset.reset_difficulty',
                        font=cls.FONT_10,
                        size=(8, 1))
                ],
                [
                    sg.Text('Farm Difficulty', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [
                            x.display_name for x in EventDifficultyEnum
                            if x is not EventDifficultyEnum.NONE],
                        default_value=EventDifficultyEnum.EASY.display_name,
                        key='event_reset.farm_difficulty',
                        font=cls.FONT_10,
                        size=(8, 1))
                ]
            ],
            key='config_event_reset_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = (
            'event_reset.frequency', 'event_reset.reset_difficulty',
            'event_reset.farm_difficulty',
        )

        if values['event_reset.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
        else:
            cls.update_window_elements(window, elements, {'disabled': True})

        if (
                values['combat.enabled'] is True
                and values['combat.sortie_map'][0] == 'E'):
            window['event_reset.enabled'].Update(disabled=False)
        else:
            window['event_reset.enabled'].Update(False, disabled=True)
            cls.update_window_elements(window, elements, {'disabled': True})
