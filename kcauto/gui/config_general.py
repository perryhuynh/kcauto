import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.interaction_modes import InteractionModeEnum
from constants import (
    DEFAULT_CHROME_DEV_PORT, MIN_JST_OFFSET, MAX_JST_OFFSET, MIN_PORT,
    MAX_PORT)


class ConfigGeneralLayout(LayoutBase):
    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('JST Offset', **cls.LABEL_SETTINGS),
                    sg.Spin(
                        [x for x in range(MIN_JST_OFFSET, MAX_JST_OFFSET + 1)],
                        0,
                        key='general.jst_offset',
                        font=cls.FONT_10,
                        size=(3, 1),
                        enable_events=True)
                ],
                [
                    sg.Text('Interaction Mode', **cls.LABEL_SETTINGS),
                    sg.Combo(
                        [x.display_name for x in InteractionModeEnum],
                        key='general.interaction_mode',
                        font=cls.FONT_10,
                        size=(13, 1))
                ],
                [
                    sg.Text('Chrome Dev Port', **cls.LABEL_SETTINGS),
                    sg.Spin(
                        [x for x in range(MIN_PORT, MAX_PORT + 1)],
                        DEFAULT_CHROME_DEV_PORT,
                        key='general.chrome_dev_port',
                        font=cls.FONT_10,
                        size=(5, 1),
                        enable_events=True)
                ]
            ],
            key='config_general_col',
            visible=True)

    @classmethod
    def update_gui(cls, window, event, values):
        cls.correct_to_value_range(
            window, values, 'general.jst_offset', MIN_JST_OFFSET,
            MAX_JST_OFFSET, 0)
        cls.correct_to_value_range(
            window, values, 'general.chrome_dev_port', MIN_PORT, MAX_PORT,
            DEFAULT_CHROME_DEV_PORT)
