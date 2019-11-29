import PySimpleGUI as sg

from gui.layout_base import LayoutBase


class KcautoControls(LayoutBase):

    @classmethod
    def get_layout(cls):
        return [sg.Column(
            [[
                sg.Button(
                    'run chrome',
                    key='run_chrome',
                    font=cls.FONT_12,
                    pad=cls.PAD_BUTTON_CONTROLS),
                sg.Button(
                    'run kcauto',
                    key='run_kcauto',
                    font=cls.FONT_12,
                    pad=cls.PAD_BUTTON_CONTROLS),
                sg.Button(
                    'stop [Esc]',
                    key='stop_kcauto',
                    font=cls.FONT_12,
                    button_color=cls.COLORS_ALERT_BUTTON_DISABLED,
                    pad=cls.PAD_BUTTON_CONTROLS,
                    disabled=True),
            ]],
            pad=((0, 0), (5, 0)),
            justification='center')
        ]

    def initial_run_chrome_state(window, values):
        if (
                not values['gui.chrome_path']
                or not values['general.chrome_dev_port']):
            window['run_chrome'].Update(disabled=True)
        else:
            window['run_chrome'].Update(disabled=False)

    @classmethod
    def update_gui(cls, window, event, values):
        cls.initial_run_chrome_state(window, values)
