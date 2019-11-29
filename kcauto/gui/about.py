import PySimpleGUI as sg
import webbrowser

from gui.layout_base import LayoutBase
from version import __version__


class About(LayoutBase):
    TITLE_FONT = ('Helvetica', 24, 'bold')

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [sg.Column([[]], size=(cls.PRIMARY_COL_TAB_SIZE[0], 1))],
                [sg.Text("kcauto", font=cls.TITLE_FONT, pad=(0, (140, 0)))],
                [sg.Text(f"v{__version__}", font=cls.FONT_9)],
                [sg.Text(
                    "github",
                    key='link_github',
                    font=cls.FONT_10 + ('bold', ),
                    text_color='blue',
                    enable_events=True
                )],
                [
                    sg.Text(
                        "brought to you by",
                        font=cls.FONT_10,
                        pad=(0, (30, 0))),
                    sg.Text(
                        "mrmin123",
                        font=cls.FONT_10 + ('bold', ),
                        pad=(0, (30, 0))),
                ],
                [sg.Text(
                    "support on patreon",
                    key='link_patreon',
                    font=cls.FONT_10 + ('bold', ),
                    text_color='blue',
                    enable_events=True
                )],
            ],
            key='gui_tab_about',
            visible=False,
            size=cls.PRIMARY_COL_TAB_SIZE,
            element_justification='center',
            justification='center'
        )

    @classmethod
    def update_gui(cls, window, event, values):
        if event == 'link_github':
            webbrowser.open('https://github.com/mrmin123/kcauto')
        if event == 'link_patreon':
            webbrowser.open('https://www.patreon.com/mrmin123')
